# Round-Trip Fidelity and Canonical Completeness of IsalHG

**Proofs of Conjectures 3.7 and 3.8, a counterexample to closure, and a reproducible specification audit**

This repository contains a completed mathematical and computational study of **IsalHG**, the hypergraph instruction language introduced by Mario Pascual-Gonzalez and Ezequiel Lopez-Rubio in *Instruction Set and Language for Hypergraphs* (arXiv:2607.10194v1).

> **Status:** preprint-style independent AI-assisted research report prepared for Zach Waddle, August 7, 2026. The work has **not** undergone external peer review. The theorem claims apply to the **literal written C1–C5 formal specification in version 1 of the source preprint**, not to any unavailable implementation.

## Read the study

- **[Full paper (PDF)](IsalHG_Breakthrough_Study.pdf)**
- **[Paper source (Markdown)](paper.md)**
- **[Paper source (LaTeX)](paper.tex)**
- **[Detailed findings](FINDINGS.md)**
- **[Novelty-search log](novelty_search_log.md)**

## Main findings

The study reports four results for the written formal algorithm:

1. **Round-trip fidelity is proved.** Every completed H2S encoder branch decodes to a hypergraph isomorphic to the input, resolving the source paper's **Conjecture 3.7** for its stated finite connected duplicate-free bounded-arity input class.
2. **Canonical completeness is proved.** For hypergraphs computed with the same pointer count \(k\), two inputs are isomorphic exactly when their canonical IsalHG strings are equal, resolving **Conjecture 3.8** for the written formalism.
3. **Closure Proposition 3.1 has a one-token counterexample.** From the initial aliased-pointer state, the legal string `C_1` creates the singleton hyperedge `{u0}`, contradicting the paper's stated requirement that every hyperedge have size at least two. A support-size guard repairs the issue without changing encoder outputs on the stated input class.
4. **The published Fano-plane canonical string violates the written C1 tie-break.** An equal-cost pointer assignment has a lexicographically smaller absolute-displacement vector, so the displayed string cannot be selected by the written C1 rule. This establishes a specification/example or specification/implementation mismatch.

See **[FINDINGS.md](FINDINGS.md)** for the exact theorem statements, counterexample certificate, validation totals, and interpretation.

## Independent executable validation

The repository includes an independent literal Python implementation and three audit programs.

| Check | Total | Failures |
|---|---:|---:|
| Connected labelled hypergraph cases (≤4 vertices; fixed `k=2,3,4`) | 3,028 | 0 |
| Casewise isomorphism classes | 278 | 0 |
| Rooted encode/decode round trips | 12,069 | 0 |
| Explicit canonical relabellings | 6,285 | 0 |
| Deterministic random instances (5–8 vertices) | 150 | 0 |
| Larger-instance rooted round trips | 975 | 0 |
| Larger-instance relabellings | 1,500 | 0 |

The deterministic stress-test seed is `20260807`.

## Reproduce the checks

Tested with Python 3.13.5 and NetworkX 3.6.1 on Linux x86_64.

```bash
python -m pip install -r requirements.txt
bash code/run_all.sh
```

Expected aggregate exhaustive output includes:

```text
connected labelled hypergraphs: 3028
casewise isomorphism classes: 278
rooted round trips: 12069
canonical relabellings: 6285
failures: 0
```

Expected deterministic stress output includes:

```text
instances: 150
rooted round trips: 975
canonical relabellings: 1500
failures: 0
```

GitHub Actions also runs the complete reproducibility suite on every push and pull request.

## Repository layout

```text
.
├── IsalHG_Breakthrough_Study.pdf    # rendered paper
├── paper.md                         # Markdown paper source
├── paper.tex                        # LaTeX paper source
├── FINDINGS.md                      # concise result summary and certificates
├── novelty_search_log.md            # dated post-discovery novelty review
├── code/
│   ├── isalhg_reference.py          # literal independent reference model
│   ├── verify_isalhg_all_k.py       # exhaustive ≤4-vertex audit
│   ├── stress_isalhg.py             # deterministic 5–8-vertex stress audit
│   ├── audit_specification_defects.py
│   └── run_all.sh
├── results/
│   ├── isalhg_exhaustive_all_k.json
│   ├── isalhg_random_stress.json
│   └── isalhg_specification_audit.json
├── requirements.txt
├── environment.txt
└── SHA256SUMS
```

## What the study does—and does not—establish

The **global claims are proof-based**. The exhaustive and random computations are validation and falsification attempts, not substitutes for the proofs.

The results are intentionally scoped to the formal algorithm as written in arXiv:2607.10194v1. In particular, the Fano-plane discrepancy is evidence that the paper's prose, displayed example, or implementation may not be identical. This repository therefore does **not** claim to certify software that was unavailable for inspection.

The post-discovery novelty search recorded in [`novelty_search_log.md`](novelty_search_log.md) found no prior proof, erratum, or report of the two specification defects as of August 7, 2026. That finding cannot rule out unpublished or unindexed work.

## Source investigated

Mario Pascual-Gonzalez and Ezequiel Lopez-Rubio, **“Instruction Set and Language for Hypergraphs,”** arXiv:2607.10194v1, submitted July 11, 2026.

## Integrity

`SHA256SUMS` contains hashes for the repository's retained study artifacts and reproducibility files. Recompute with:

```bash
find . -type f \
  ! -path './.git/*' \
  ! -path './SHA256SUMS' \
  -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
```
