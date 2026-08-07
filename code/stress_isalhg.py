#!/usr/bin/env python3
"""Deterministic larger-instance stress test for the formal IsalHG model."""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
import json, random, time
import networkx as nx
from isalhg_reference import (
    encode_rooted, canonical_string, decode, relabel_edges, token_text,
)


def levi_graph(n, edges):
    g = nx.Graph()
    for v in range(n):
        g.add_node((0, v), side=0)
    for i, edge in enumerate(edges):
        g.add_node((1, i), side=1)
        for v in edge:
            g.add_edge((0, v), (1, i))
    return g


def isomorphic(n1, e1, n2, e2):
    if n1 != n2 or len(e1) != len(e2):
        return False
    g1, g2 = levi_graph(n1, e1), levi_graph(n2, e2)
    nm = nx.algorithms.isomorphism.categorical_node_match("side", -1)
    return nx.is_isomorphic(g1, g2, node_match=nm)


def random_connected_hypergraph(rng, n, k):
    edges = set()
    order = list(range(n)); rng.shuffle(order)
    for idx in range(1, n):
        parent = order[rng.randrange(idx)]
        edges.add(frozenset((order[idx], parent)))
    possible = [frozenset(c) for r in range(2, k + 1) for c in combinations(range(n), r)]
    target = rng.randint(n, min(len(possible), n + 5))
    while len(edges) < target:
        edges.add(rng.choice(possible))
    return tuple(sorted(edges, key=lambda e: tuple(sorted(e))))


def main():
    rng = random.Random(20260807)
    report = {
        "seed": 20260807,
        "scope": "150 deterministic connected random simple hypergraphs on 5-8 vertices, k in {3,4}; every root and ten random relabellings per instance.",
        "instances": 0,
        "rooted_roundtrips": 0,
        "canonical_relabellings": 0,
        "cross_instance_equal_string_checks": 0,
        "failures": [],
    }
    seen = {}
    t0 = time.time()
    for case in range(150):
        n = rng.randint(5, 8)
        k = rng.choice((3, 4))
        edges = random_connected_hypergraph(rng, n, k)
        report["instances"] += 1

        for start in range(n):
            s = encode_rooted(n, edges, k, start)
            dn, de = decode(s, k)
            if not isomorphic(n, edges, dn, de):
                report["failures"].append({
                    "type": "roundtrip", "case": case, "n": n, "k": k,
                    "start": start, "edges": repr(edges),
                    "string": token_text(s), "decoded": repr(de),
                })
            report["rooted_roundtrips"] += 1

        canon = canonical_string(n, edges, k)
        key = (k, canon)
        if key in seen:
            report["cross_instance_equal_string_checks"] += 1
            old_n, old_edges = seen[key]
            if not isomorphic(old_n, old_edges, n, edges):
                report["failures"].append({
                    "type": "collision", "case": case, "n": n, "k": k,
                    "string": token_text(canon),
                })
        else:
            seen[key] = (n, edges)

        for _ in range(10):
            p = list(range(n)); rng.shuffle(p)
            ep = relabel_edges(edges, tuple(p))
            cp = canonical_string(n, ep, k)
            if cp != canon:
                report["failures"].append({
                    "type": "relabel", "case": case, "n": n, "k": k,
                    "perm": p, "canon": token_text(canon),
                    "relabelled": token_text(cp),
                })
            report["canonical_relabellings"] += 1

    report["failure_count"] = len(report["failures"])
    report["elapsed_seconds"] = time.time() - t0
    out = Path(__file__).resolve().parents[1] / "results" / "isalhg_random_stress.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k != 'failures'}, indent=2))


if __name__ == "__main__":
    main()
