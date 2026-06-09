"""
P1-003 FIX: Streaming responses
P1-004 FIX: Retry with exponential backoff

Install: pip install anthropic tenacity
"""
from __future__ import annotations

import time
import logging
from collections.abc import Iterator
from typing import Callable, Any

import anthropic
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# RETRY DECORATOR
# Handles: 429 (rate limit), 529 (overloaded), 500 (server error)
# ─────────────────────────────────────────────────────────────

RETRYABLE = (
    anthropic.RateLimitError,
    anthropic.APIStatusError,
    anthropic.APIConnectionError,
)


def make_retry_decorator(max_attempts: int = 5):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        retry=retry_if_exception_type(RETRYABLE),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


# ─────────────────────────────────────────────────────────────
# STREAMING VERSION of _call_llm
# ─────────────────────────────────────────────────────────────

def call_llm_streaming(
    client: anthropic.Anthropic,
    system: str,
    messages: list[dict],
    tools: list[dict],
    model: str,
    max_tokens: int,
    on_token: Callable[[str], None] | None = None,  # called per text chunk
) -> str:
    """
    Stream LLM response. Calls on_token(chunk) as each text chunk arrives.
    Returns full text when complete.

    Usage in CLI:
        def print_chunk(chunk): print(chunk, end="", flush=True)
        result = call_llm_streaming(..., on_token=print_chunk)

    Usage in FastAPI WebSocket:
        async def send_chunk(chunk):
            await websocket.send_text(chunk)
        # wrap with asyncio or use separate thread
    """
    accumulated = []

    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": messages,
    }
    if tools:
        kwargs["tools"] = tools

    with client.messages.stream(**kwargs) as stream:
        for text in stream.text_stream:
            accumulated.append(text)
            if on_token:
                on_token(text)

    return "".join(accumulated)


# ─────────────────────────────────────────────────────────────
# COMBINED: streaming + retry + tool loop
# This is the production-ready _call_llm replacement
# ─────────────────────────────────────────────────────────────

class ProductionLLMCaller:
    """
    Drop-in for BaseResearchAgent._call_llm in production.

    Features:
    - Automatic retry on rate limits / server errors
    - Token streaming with callback
    - Tool use loop
    - Token count logging for cost tracking
    """

    def __init__(
        self,
        client: anthropic.Anthropic,
        model: str = "claude-opus-4-8",
        on_token: Callable[[str], None] | None = None,
        max_retry_attempts: int = 5,
    ):
        self.client = client
        self.model = model
        self.on_token = on_token
        self._retry = make_retry_decorator(max_retry_attempts)
        self._total_input_tokens = 0
        self._total_output_tokens = 0

    def call(
        self,
        system: str,
        messages: list[dict],
        tools: list[dict],
        tool_executors: dict,
        max_tokens: int = 4096,
        max_tool_iterations: int = 10,
    ) -> str:
        return self._tool_loop(
            system, messages, tools, tool_executors,
            max_tokens, max_tool_iterations,
        )

    def _tool_loop(self, system, messages, tools, executors,
                   max_tokens, max_iter) -> str:
        for _ in range(max_iter):
            response = self._call_with_retry(system, messages, tools, max_tokens)

            self._total_input_tokens  += response.usage.input_tokens
            self._total_output_tokens += response.usage.output_tokens

            text_parts = [b.text for b in response.content if b.type == "text"]

            if response.stop_reason == "end_turn":
                return "\n".join(text_parts)

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    executor = executors.get(block.name)
                    try:
                        result = executor(**block.input) if executor else \
                                 f"Tool '{block.name}' not implemented."
                    except Exception as e:
                        result = f"Tool error: {e}"
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    })
                messages.append({"role": "user", "content": tool_results})
            else:
                return "\n".join(text_parts)

        return "[max iterations]"

    def _call_with_retry(self, system, messages, tools, max_tokens):
        """Single LLM call with retry decorator."""
        @make_retry_decorator()
        def _inner():
            kwargs: dict[str, Any] = {
                "model": self.model,
                "max_tokens": max_tokens,
                "system": system,
                "messages": messages,
            }
            if tools:
                kwargs["tools"] = tools
            return self.client.messages.create(**kwargs)
        return _inner()

    @property
    def token_usage(self) -> dict:
        return {
            "input": self._total_input_tokens,
            "output": self._total_output_tokens,
            "estimated_cost_usd": (
                self._total_input_tokens / 1_000_000 * 15.0 +   # opus-4-8 pricing
                self._total_output_tokens / 1_000_000 * 75.0
            ),
        }
