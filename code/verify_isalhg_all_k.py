#!/usr/bin/env python3
"""Exhaustive finite audit of the formal IsalHG specification for k=2,3,4.

Round-trip fidelity is checked for every connected labelled input and every root.
Canonical completeness is checked on one representative of every isomorphism
class and every vertex permutation; this covers every labelling without redundant
recomputation of the same class many times.
"""
from itertools import combinations, permutations
from pathlib import Path
import json, time
from isalhg_reference import (
    is_connected, encode_rooted, decode, brute_iso_key, canonical_string,
    relabel_edges, token_text,
)


def all_hypergraphs(n: int, k: int):
    possible = []
    for r in range(2, min(k, n) + 1):
        possible.extend(frozenset(c) for c in combinations(range(n), r))
    for mask in range(1 << len(possible)):
        edges = tuple(possible[i] for i in range(len(possible)) if (mask >> i) & 1)
        if is_connected(n, edges):
            yield edges


def audit_case(k: int, n: int, failures: list[dict]) -> dict:
    labelled = list(all_hypergraphs(n, k))
    reps: dict[tuple, tuple] = {}
    rooted = 0

    # Every labelled hypergraph and every possible start vertex.
    for edges in labelled:
        input_key = brute_iso_key(n, edges)
        reps.setdefault(input_key, edges)
        for start in range(n):
            string = encode_rooted(n, edges, k, start)
            decoded_n, decoded_edges = decode(string, k)
            if decoded_n != n or brute_iso_key(decoded_n, decoded_edges) != input_key:
                failures.append({
                    "type": "roundtrip", "k": k, "n": n,
                    "edges": repr(edges), "start": start,
                    "string": token_text(string), "decoded": repr(decoded_edges),
                })
            rooted += 1

    # One representative per exact isomorphism class, under all n! labellings.
    class_strings: dict[tuple, tuple] = {}
    relabel_checks = 0
    for iso_key, edges in reps.items():
        canon = canonical_string(n, edges, k)
        class_strings[iso_key] = canon
        for perm in permutations(range(n)):
            relabelled = relabel_edges(edges, perm)
            relabelled_canon = canonical_string(n, relabelled, k)
            if relabelled_canon != canon:
                failures.append({
                    "type": "relabel", "k": k, "n": n,
                    "edges": repr(edges), "perm": perm,
                    "canon": token_text(canon),
                    "relabelled_canon": token_text(relabelled_canon),
                })
                break
            relabel_checks += 1

    reverse: dict[tuple, tuple] = {}
    for iso_key, canon in class_strings.items():
        if canon in reverse and reverse[canon] != iso_key:
            failures.append({
                "type": "collision", "k": k, "n": n,
                "string": token_text(canon),
            })
        reverse[canon] = iso_key

    return {
        "connected_labelled_hypergraphs": len(labelled),
        "isomorphism_classes": len(reps),
        "rooted_roundtrips_all_labelled": rooted,
        "canonical_relabellings_of_class_representatives": relabel_checks,
        "distinct_canonical_strings": len(reverse),
    }


def main() -> None:
    report = {
        "scope": (
            "All connected finite simple hypergraphs on n<=4 vertices, "
            "separately for fixed pointer/arity bounds k=2,3,4. Round trips: "
            "every admissible labelled edge set and every root. Canonicality: "
            "one representative of every exact isomorphism class under all n! "
            "vertex permutations, plus cross-class collision testing."
        ),
        "by_k_n": {},
        "failures": [],
    }
    t0 = time.time()
    for k in (2, 3, 4):
        report["by_k_n"][str(k)] = {}
        for n in range(1, 5):
            stats = audit_case(k, n, report["failures"])
            report["by_k_n"][str(k)][str(n)] = stats
            print(f"k={k} n={n}: {stats}", flush=True)

    aggregate = {
        "connected_labelled_hypergraphs": sum(
            report["by_k_n"][str(k)][str(n)]["connected_labelled_hypergraphs"]
            for k in (2, 3, 4) for n in range(1, 5)
        ),
        "casewise_isomorphism_classes": sum(
            report["by_k_n"][str(k)][str(n)]["isomorphism_classes"]
            for k in (2, 3, 4) for n in range(1, 5)
        ),
        "rooted_roundtrips_all_labelled": sum(
            report["by_k_n"][str(k)][str(n)]["rooted_roundtrips_all_labelled"]
            for k in (2, 3, 4) for n in range(1, 5)
        ),
        "canonical_relabellings_of_class_representatives": sum(
            report["by_k_n"][str(k)][str(n)]["canonical_relabellings_of_class_representatives"]
            for k in (2, 3, 4) for n in range(1, 5)
        ),
    }
    report["aggregate"] = aggregate
    report["elapsed_seconds"] = time.time() - t0
    report["failure_count"] = len(report["failures"])

    out = Path(__file__).resolve().parents[1] / "results" / "isalhg_exhaustive_all_k.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str) + "\n")
    print("aggregate", aggregate)
    print("failures", report["failure_count"], "seconds", report["elapsed_seconds"])


if __name__ == "__main__":
    main()
