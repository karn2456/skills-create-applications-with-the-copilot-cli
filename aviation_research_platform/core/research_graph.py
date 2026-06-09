"""
Research Knowledge Graph — connects papers, hypotheses, findings, and dead-ends
into a queryable graph structure.

Inspired by Orchestra's "Total Recall" that surfaces hidden connections between
ideas the researcher didn't know existed.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


NodeKind = Literal["paper", "hypothesis", "finding", "gap", "experiment", "dead_end"]
EdgeKind = Literal["supports", "contradicts", "extends", "derived_from",
                   "addresses_gap", "informs", "refutes"]


@dataclass
class GraphNode:
    node_id: str
    kind: NodeKind
    label: str
    summary: str
    metadata: dict = field(default_factory=dict)

    def short(self) -> str:
        return f"[{self.kind}] {self.label}"


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    kind: EdgeKind
    weight: float = 1.0
    note: str = ""


class ResearchGraph:
    """
    Directed knowledge graph for a research project.
    Nodes = papers / hypotheses / findings / gaps / experiments
    Edges = semantic relationships between them
    """

    def __init__(self):
        self._nodes: dict[str, GraphNode] = {}
        self._edges: list[GraphEdge] = []

    # ── Mutations ────────────────────────────────────────────────────────────

    def add_node(self, node_id: str, kind: NodeKind, label: str,
                 summary: str, **meta) -> GraphNode:
        node = GraphNode(node_id=node_id, kind=kind,
                         label=label, summary=summary, metadata=meta)
        self._nodes[node_id] = node
        return node

    def add_edge(self, source_id: str, target_id: str,
                 kind: EdgeKind, note: str = "") -> None:
        if source_id in self._nodes and target_id in self._nodes:
            self._edges.append(GraphEdge(source_id, target_id, kind, note=note))

    # ── Queries ──────────────────────────────────────────────────────────────

    def neighbors(self, node_id: str, edge_kind: EdgeKind | None = None) -> list[GraphNode]:
        targets = [
            e.target_id for e in self._edges
            if e.source_id == node_id and (edge_kind is None or e.kind == edge_kind)
        ]
        return [self._nodes[t] for t in targets if t in self._nodes]

    def find_by_kind(self, kind: NodeKind) -> list[GraphNode]:
        return [n for n in self._nodes.values() if n.kind == kind]

    def find_gaps(self) -> list[GraphNode]:
        return self.find_by_kind("gap")

    def find_contradictions(self) -> list[tuple[GraphNode, GraphNode]]:
        return [
            (self._nodes[e.source_id], self._nodes[e.target_id])
            for e in self._edges if e.kind == "contradicts"
            if e.source_id in self._nodes and e.target_id in self._nodes
        ]

    def path_exists(self, from_id: str, to_id: str) -> bool:
        """BFS to check if a path exists between two nodes."""
        visited, queue = set(), [from_id]
        while queue:
            current = queue.pop(0)
            if current == to_id:
                return True
            if current in visited:
                continue
            visited.add(current)
            queue.extend(n.node_id for n in self.neighbors(current))
        return False

    def summary(self) -> str:
        counts: dict[str, int] = {}
        for n in self._nodes.values():
            counts[n.kind] = counts.get(n.kind, 0) + 1
        edge_counts: dict[str, int] = {}
        for e in self._edges:
            edge_counts[e.kind] = edge_counts.get(e.kind, 0) + 1
        lines = ["=== Research Knowledge Graph ==="]
        for kind, cnt in sorted(counts.items()):
            lines.append(f"  {kind}: {cnt} nodes")
        for kind, cnt in sorted(edge_counts.items()):
            lines.append(f"  {kind}: {cnt} edges")
        contradictions = self.find_contradictions()
        if contradictions:
            lines.append(f"  ⚠ Contradictions found: {len(contradictions)}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "nodes": [vars(n) for n in self._nodes.values()],
            "edges": [vars(e) for e in self._edges],
        }

    def save(self, path: str) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: str) -> "ResearchGraph":
        data = json.loads(Path(path).read_text())
        g = cls()
        for n in data.get("nodes", []):
            g._nodes[n["node_id"]] = GraphNode(**n)
        for e in data.get("edges", []):
            g._edges.append(GraphEdge(**e))
        return g
