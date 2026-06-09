"""
P0-001 FIX: Tool Use Loop
=========================
ปัญหา: _call_llm() ไม่ handle tool_use blocks
เมื่อ LLM เรียก tool → response.content มี tool_use block ไม่ใช่ text block
→ return "" เปล่าๆ แทนที่จะ execute tool แล้ว continue loop

วิธีแก้: แทนที่ _call_llm() ใน BaseResearchAgent ด้วย version นี้
"""
from __future__ import annotations

import json
from typing import Any

import anthropic


def _call_llm_with_tools(
    client: anthropic.Anthropic,
    system: str,
    messages: list[dict],
    tools: list[dict],
    tool_executors: dict,          # {"tool_name": callable}
    model: str = "claude-opus-4-8",
    max_tokens: int = 4096,
    max_iterations: int = 10,
) -> str:
    """
    Proper tool-use agentic loop.

    Loop:
      1. Call LLM with tools
      2. If stop_reason == "tool_use" → execute each tool, append results
      3. Call LLM again with tool results
      4. Repeat until stop_reason == "end_turn" or max_iterations reached
    """
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = client.messages.create(**kwargs)

        # Collect text from this response
        text_parts = [
            block.text
            for block in response.content
            if block.type == "text"
        ]

        # If LLM is done → return all accumulated text
        if response.stop_reason == "end_turn":
            return "\n".join(text_parts)

        # If LLM wants to use a tool
        if response.stop_reason == "tool_use":
            # Append assistant turn (with tool_use blocks)
            messages.append({"role": "assistant", "content": response.content})

            # Execute each tool call and collect results
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_name = block.name
                tool_input = block.input
                tool_use_id = block.id

                executor = tool_executors.get(tool_name)
                if executor:
                    try:
                        result = executor(**tool_input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": str(result),
                        })
                    except Exception as e:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": f"Error executing {tool_name}: {e}",
                            "is_error": True,
                        })
                else:
                    # Tool not implemented — tell LLM
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": f"Tool '{tool_name}' is not yet implemented. Proceed without it.",
                        "is_error": True,
                    })

            # Append tool results as user turn
            messages.append({"role": "user", "content": tool_results})
            # Loop continues — LLM will process tool results

        else:
            # Unexpected stop reason
            return "\n".join(text_parts)

    return "[Max iterations reached — partial result returned]"


# ─────────────────────────────────────────────────────────────
# HOW TO APPLY: replace _call_llm in base_agent.py
# ─────────────────────────────────────────────────────────────

class PatchedBaseAgent:
    """
    Drop-in replacement for the _call_llm method in BaseResearchAgent.
    Copy this method into base_agent.py.
    """

    def _call_llm(self, messages: list[dict], max_tokens: int = 4096) -> str:
        agent_tools = self.tools()

        # Build tool executor map — agents override this method to
        # provide actual implementations
        executors = self._get_tool_executors()

        return _call_llm_with_tools(
            client=self.client,
            system=self.system_prompt,
            messages=messages,
            tools=agent_tools,
            tool_executors=executors,
            model=self.MODEL,
            max_tokens=max_tokens,
        )

    def _get_tool_executors(self) -> dict:
        """
        Override in each agent to provide real tool implementations.
        Return dict: {"tool_name": callable(**input) -> str}

        Example in LiteratureSearchAgent:
            def _get_tool_executors(self):
                return {
                    "database_search": self._exec_database_search,
                    "build_search_string": self._exec_build_search_string,
                }
        """
        return {}   # Default: no executable tools → LLM uses knowledge only
