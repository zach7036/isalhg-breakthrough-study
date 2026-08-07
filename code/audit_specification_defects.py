#!/usr/bin/env python3
"""Machine-checkable certificates for two specification defects in arXiv:2607.10194v1."""
from __future__ import annotations
from itertools import permutations
from pathlib import Path
import json
from isalhg_reference import C, N, P, V, decode, shortest_delta, movement_tokens, token_text, canonical_string


def parse(text: str):
    names = {"N": N, "P": P, "V": V, "C": C}
    out = []
    for atom in text.split():
        name, *rest = atom.split("_")
        params = tuple(map(int, rest[0].split(","))) if rest else ()
        out.append((names[name],) + params)
    return tuple(out)


def state_after(tokens, k):
    cdll = [0]
    ptrs = [0] * k
    edges = set()
    next_id = 1
    for t in tokens:
        if t[0] in (N, P):
            idx = t[1] - 1
            pos = cdll.index(ptrs[idx])
            ptrs[idx] = cdll[(pos + (-1 if t[0] == N else 1)) % len(cdll)]
        elif t[0] == V:
            i, j = t[1], t[2]
            new = list(range(next_id, next_id + j)); next_id += j
            pos = cdll.index(ptrs[0]); cdll[pos + 1:pos + 1] = new
            edges.add(frozenset(ptrs[:i]) | frozenset(new))
        elif t[0] == C:
            edges.add(frozenset(ptrs[:t[1]]))
    return cdll, ptrs, edges, next_id


def c1_key(delta):
    return (sum(abs(x) for x in delta), tuple(abs(x) for x in delta), tuple(delta))


def main():
    report = {}

    n, edges = decode(((C, 1),), 3)
    report["closure_counterexample"] = {
        "k": 3,
        "string": "C_1",
        "decoded_vertex_count": n,
        "decoded_edges": [sorted(e) for e in edges],
        "minimum_edge_size": min(map(len, edges)),
        "conflict": "The paper defines every hyperedge to have size at least 2.",
        "repair": "Make C_i a no-op whenever the set of distinct pointer values has size < 2 (or enlarge the object class to permit singleton edges).",
    }

    published_text = (
        "V_1,2 V_1,2 V_1,2 "
        "N_1 N_1 N_1 N_2 P_3 C_3 "
        "N_1 N_2 C_3 P_1 P_3 C_3 N_1 P_2 C_3"
    )
    published = parse(published_text)
    prefix = published[:3]
    movement = published[3:8]
    insertion = published[8]
    cdll, ptrs, _, _ = state_after(prefix, 3)
    _, moved_ptrs, _, _ = state_after(prefix + movement, 3)
    support = tuple(moved_ptrs[:insertion[1]])

    feasible = []
    for assignment in permutations(support):
        delta = tuple(shortest_delta(tuple(cdll), ptrs[i], assignment[i]) for i in range(3))
        feasible.append({
            "assignment_to_p1_p2_p3": list(assignment),
            "delta": list(delta),
            "C1_key": [c1_key(delta)[0], list(c1_key(delta)[1]), list(c1_key(delta)[2])],
            "movement_tokens": token_text(movement_tokens(delta)),
        })
    feasible.sort(key=lambda x: (x["C1_key"][0], tuple(x["C1_key"][1]), tuple(x["C1_key"][2])))

    published_delta = (-3, -1, 1)
    fano_edges = tuple(map(frozenset, [
        (0, 1, 2), (0, 3, 4), (0, 5, 6),
        (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5),
    ]))
    formal_canon = canonical_string(7, fano_edges, 3)

    report["fano_example_c1_certificate"] = {
        "published_string": published_text,
        "formal_canonical_string_under_written_C1": token_text(formal_canon),
        "state_after_first_three_tokens": {"cdll": cdll, "pointers": ptrs},
        "published_next_movement": token_text(movement),
        "published_delta": list(published_delta),
        "published_C1_key": [c1_key(published_delta)[0], list(c1_key(published_delta)[1]), list(c1_key(published_delta)[2])],
        "next_inserted_support": list(support),
        "C1_minimizer_for_same_support": feasible[0],
        "all_feasible_assignments": feasible,
        "conclusion": (
            "The published displacement and the minimizer have equal total cost 5, "
            "but the minimizer has absolute-displacement tuple (1,1,3), which is "
            "lexicographically smaller than the published (3,1,1). Therefore the "
            "displayed string cannot be produced by the written C1 rule."
        ),
    }

    out = Path(__file__).resolve().parents[1] / "results" / "isalhg_specification_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
