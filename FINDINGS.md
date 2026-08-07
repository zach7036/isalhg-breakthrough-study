# Findings

This file summarizes the central claims and validation of the accompanying study **“Round-Trip Fidelity and Canonical Completeness of IsalHG.”** For proofs, definitions, limitations, and literature review, see [`paper.md`](paper.md) or the rendered [`IsalHG_Breakthrough_Study.pdf`](IsalHG_Breakthrough_Study.pdf).

## Research target

The source preprint *Instruction Set and Language for Hypergraphs* (arXiv:2607.10194v1) introduced IsalHG and left two properties explicitly open:

- **Conjecture 3.7 — round-trip fidelity:** encoding and then decoding a connected bounded-arity hypergraph returns an isomorphic hypergraph.
- **Conjecture 3.8 — canonical completeness:** two such hypergraphs are isomorphic if and only if their canonical IsalHG strings are equal.

Those properties are central to using IsalHG as an exact hypergraph representation and isomorphism invariant.

## Result 1 — round-trip fidelity

For every finite connected duplicate-free hypergraph with edge arity at most a fixed `k`, and every permitted starting vertex, every completed branch of the formal H2S encoder decodes to a hypergraph isomorphic to the input.

The proof establishes:

1. a bijection between materialized input vertices and machine vertices;
2. a simulation invariant between the encoder state and execution of the emitted token prefix;
3. progress from connectedness, ensuring an insertable waiting edge exists until completion; and
4. exact one-time insertion of every processed input edge with the intended support.

This resolves Conjecture 3.7 **for the written formal algorithm**.

## Result 2 — canonical completeness

For connected bounded-arity hypergraphs evaluated with the same pointer count `k`,

\[
H_1 \cong H_2 \quad\Longleftrightarrow\quad w^*_{H_1}=w^*_{H_2}.
\]

The forward direction is proved by constructing a token-preserving correspondence between the complete C5 backtracking trees of corresponding rooted isomorphic inputs. Every quantity inspected by C1–C4 is preserved under isomorphism, so corresponding unresolved C5 branches yield the same completed token strings.

The reverse direction follows from round-trip fidelity: equal canonical strings decode to the same machine-generated hypergraph, to which both inputs are isomorphic.

This resolves Conjecture 3.8 **for the written formal algorithm**.

## Result 3 — one-token counterexample to closure

The source paper defines every hyperedge as having at least two vertices. Its `C_i` instruction, however, inserts the set of **distinct** values beneath the leading pointers.

Initially every pointer aliases the same machine vertex `u0`. Therefore the syntactically legal one-token program

```text
C_1
```

creates the singleton hyperedge

```text
{u0}
```

whose size is one. Under the source paper's stated object definition, this is a direct counterexample to Proposition 3.1 (closure).

A minimal repair is to make `C_i` a no-op whenever the support contains fewer than two distinct pointer values. Because encoder-produced `C_i` operations correspond to valid input hyperedges, this guard does not alter valid encoder outputs on the stated input class.

The machine-readable certificate is retained in [`results/isalhg_specification_audit.json`](results/isalhg_specification_audit.json).

## Result 4 — Fano-plane C1 discrepancy

After the first three `V_1,2` tokens in the Fano-plane example, the published next pointer displacement is

\[
(-3,-1,+1),
\]

with C1 key

\[
\bigl(5;(3,1,1);(-3,-1,1)\bigr).
\]

For the same intended support, another feasible pointer assignment has displacement

\[
(-1,+1,-3),
\]

with C1 key

\[
\bigl(5;(1,1,3);(-1,1,-3)\bigr).
\]

Both total movement costs equal five, but `(1,1,3)` is lexicographically smaller than `(3,1,1)`. Therefore the published movement cannot be chosen by the written C1 tie-break.

This does **not** by itself identify whether the prose rule, the displayed Fano example, or an unavailable implementation is the intended authority. It establishes a concrete mismatch among those possibilities.

## Validation and falsification attempts

### Exhaustive audit

All connected labelled simple hypergraphs on at most four vertices were enumerated separately for fixed `k = 2, 3, 4`.

| Validation target | Completed checks | Failures |
|---|---:|---:|
| Connected labelled hypergraph cases | 3,028 | 0 |
| Casewise isomorphism classes | 278 | 0 |
| Rooted encode/decode round trips | 12,069 | 0 |
| Explicit canonical relabellings | 6,285 | 0 |

No cross-class canonical-string collision occurred among the 278 casewise isomorphism classes.

### Larger deterministic stress audit

A second deterministic audit generated 150 connected random simple hypergraphs on 5–8 vertices with `k ∈ {3,4}` using seed `20260807`.

| Validation target | Checks | Failures |
|---|---:|---:|
| Rooted round trips | 975 | 0 |
| Canonical relabellings | 1,500 | 0 |

Round-trip outputs in this audit were checked independently through colored Levi-graph isomorphism using NetworkX.

### Re-run in this repository package

Before repository publication, the exhaustive suite was rerun and reproduced:

- 3,028 connected labelled cases;
- 278 casewise isomorphism classes;
- 12,069 rooted round trips;
- 6,285 canonical relabellings; and
- zero failures.

The deterministic stress audit was rerun independently and reproduced 150 instances, 975 rooted round trips, 1,500 relabellings, and zero failures. The specification-defect audit also reproduced both certificates.

## Frontier change claimed by the study

**Previously:** Conjectures 3.7 and 3.8 were explicitly open in version 1 of the IsalHG preprint and supported empirically rather than proved.

**This study reports:** complete proofs of both conjectures for the written formalism, plus a shortest one-token counterexample to the stated closure proposition and an explicit certificate showing that the printed Fano-plane string violates the written C1 rule.

The paper classifies this as a **minor breakthrough in the narrowly defined IsalHG research line**, subject to independent mathematical review. It does not claim a broad breakthrough in graph theory or hypergraph isomorphism generally.
