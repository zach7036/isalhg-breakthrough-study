# Round-Trip Fidelity and Canonical Completeness of IsalHG

## Abstract

Pascual-Gonzalez and Lopez-Rubio introduced IsalHG, an executable string language for finite connected bounded-arity hypergraphs, and left two central properties explicitly open: round-trip fidelity (Conjecture 3.7) and canonical completeness (Conjecture 3.8). This study proves both conjectures for the literal written C1–C5 formal algorithm in arXiv:2607.10194v1. It also identifies two specification defects: Proposition 3.1 (closure) is false under the paper's own minimum-edge-size definition because the legal one-token string `C_1` creates a singleton hyperedge, and the published Fano-plane canonical string violates the written C1 displacement tie-break. Independent executable validation found zero failures across 12,069 rooted round trips over all connected labelled simple hypergraphs through four vertices for fixed `k=2,3,4`, 6,285 explicit canonical relabellings covering 278 casewise isomorphism classes, plus 975 rooted round trips and 1,500 relabellings on 150 deterministic random 5–8 vertex hypergraphs. The result is scoped to the written formalism and has not undergone external peer review.

## 1. Research target

The source preprint *Instruction Set and Language for Hypergraphs* (arXiv:2607.10194v1) defines a machine with a circular doubly linked list and `k` traversal pointers. Hypergraphs are encoded as instruction strings and decoded by executing those instructions from a one-vertex initial state.

Two properties are central to the method:

- **Conjecture 3.7 — round-trip fidelity:** encoding a connected bounded-arity hypergraph and decoding the resulting string returns an isomorphic hypergraph.
- **Conjecture 3.8 — canonical completeness:** two such hypergraphs are isomorphic if and only if their canonical IsalHG strings are equal.

Before this study, both were supported empirically but not formally proved in the source paper.

## 2. Breakthrough criterion

Before selecting the final target, the threshold was fixed as follows. A result would count as a minor breakthrough only if it resolved or decisively refuted an explicit open question central to a current method for the full stated object class; changed the formal status of that method; admitted independent verification by proof and executable checks; and survived a post-discovery novelty search. Merely extending finite computations, reproducing existing experiments, or obtaining a modest speed improvement would not qualify.

## 3. Formal setting

Fix `k >= 2`. The stated input class consists of finite, connected, undirected, duplicate-free hypergraphs `H=(V,E)` satisfying

`2 <= |e| <= k`

for every hyperedge `e`.

The machine state is a hypergraph under construction, a circular doubly linked list containing the machine vertices, and pointers `p_1,...,p_k` into that list. Execution begins with one vertex `u0`, the one-element circular list `[u0]`, and every pointer at `u0`.

Relevant token families are:

- `P_i`, `N_i`: move pointer `p_i` one list position forward/backward;
- `V_{i,j}`: create `j` fresh vertices and insert the hyperedge formed from those fresh vertices plus the distinct values under the leading `i` pointers;
- `C_i`: insert the set of distinct values under the leading `i` pointers unless already present;
- `W`: no operation.

The encoder repeatedly chooses an insertable waiting edge. If `S` is the set of materialised input vertices and `e` is the next edge, define `A=e∩S`, `B=e\S`, `i=|A|`, and `j=|B|`. It positions the leading `i` pointers onto the machine images of `A`, then emits `V_{i,j}` if `j>0` and `C_i` if `j=0`.

The written selection cascade first minimises pointer movement (C1), then prefers `V` over `C` (C2), minimises token parameters (C3), minimises a structural invariant tuple (C4), and exhaustively branches over unresolved ties (C5), keeping the lexicographically smallest completed string.

## 4. Result 1 — round-trip fidelity

### Theorem

For every finite connected duplicate-free hypergraph with edge arity at most fixed `k`, and every permitted starting vertex, every completed branch of the formal H2S encoder decodes to a hypergraph isomorphic to the input.

### Proof structure

The proof maintains a bijection between materialised input vertices and machine vertices. Three coupled invariants are preserved after every emitted prefix:

1. executing the emitted token prefix reproduces the encoder's simulated machine state;
2. the current input-to-machine correspondence is bijective on the materialised vertices; and
3. every processed input edge has been inserted exactly once with exactly the support determined by the vertex correspondence.

Progress follows from connectedness: as long as unprocessed vertices or edges remain, at least one waiting edge intersects the materialised set and is therefore insertable. When a `V_{i,j}` token is emitted, the `j` newly materialised input vertices are bijected with the `j` fresh machine vertices. When a `C_i` token is emitted, all vertices of the edge are already materialised and pointer injectivity over the selected support ensures the intended edge is inserted. Induction over processed edges yields an isomorphism between the decoded hypergraph and the input.

Therefore Conjecture 3.7 holds for the literal written algorithm.

## 5. Result 2 — canonical completeness

### Theorem

For connected bounded-arity hypergraphs evaluated with the same pointer count `k`,

`H1 ≅ H2  <=>  w*(H1) = w*(H2)`.

### Forward direction

Let `φ:H1→H2` be a hypergraph isomorphism and choose corresponding roots. The complete C5 backtracking trees of the two rooted inputs admit a token-preserving correspondence. All quantities inspected by C1–C4 are invariant under `φ`: pointer-distance costs, token family, token parameters, and the structural tuple used in C4. Whenever C5 branches over surviving ties, `φ` induces a bijection between corresponding branches, including assignments of newly materialised vertices to newly created machine positions.

Hence corresponding rooted search trees have the same set of completed token strings. Their lexicographic minima are equal. The outer root-selection rule is itself isomorphism-invariant, so the canonical strings coincide.

### Reverse direction

If two canonical strings are equal, decode that common string. By round-trip fidelity, each input hypergraph is isomorphic to the decoded machine-generated hypergraph. Therefore the two inputs are isomorphic to one another.

Thus Conjecture 3.8 holds for the written formalism.

## 6. Result 3 — counterexample to closure

The source paper defines hyperedges to have size at least two, yet `C_i` inserts the set of **distinct** values under the first `i` pointers.

Initially all pointers alias `u0`. Therefore the syntactically legal one-token string

`C_1`

creates the edge

`{u0}`.

That edge has cardinality one and is outside the paper's declared object class. This is a direct counterexample to Proposition 3.1 as written.

A minimal repair is to make `C_i` a no-op whenever the set of distinct pointer values has size below two. Because encoder-generated `C_i` tokens correspond to valid input hyperedges of size at least two, this guard does not alter valid encoder outputs on the stated input class.

## 7. Result 4 — Fano-plane C1 discrepancy

After the first three `V_1,2` instructions in the paper's Fano-plane example, the published next pointer displacement is

`(-3,-1,+1)`

with written C1 key

`(5 ; (3,1,1) ; (-3,-1,1))`.

For the same intended support, another feasible pointer assignment has displacement

`(-1,+1,-3)`

and key

`(5 ; (1,1,3) ; (-1,1,-3))`.

Both have total movement cost five, but `(1,1,3)` is lexicographically smaller than `(3,1,1)`. Therefore the published movement cannot be selected by the written C1 rule. This proves a specification/example or specification/implementation mismatch; it does not by itself determine which version was intended.

## 8. Computational validation

### Exhaustive audit

All connected labelled simple hypergraphs on at most four vertices were enumerated separately for fixed `k=2,3,4`.

| Validation target | Completed checks | Failures |
|---|---:|---:|
| Connected labelled hypergraph cases | 3,028 | 0 |
| Casewise isomorphism classes | 278 | 0 |
| Rooted encode/decode round trips | 12,069 | 0 |
| Explicit canonical relabellings | 6,285 | 0 |

No cross-class canonical-string collision occurred among the 278 casewise isomorphism classes.

### Larger deterministic stress audit

A second deterministic audit generated 150 connected random simple hypergraphs on 5–8 vertices with `k∈{3,4}` using seed `20260807`.

| Validation target | Checks | Failures |
|---|---:|---:|
| Rooted round trips | 975 | 0 |
| Canonical relabellings | 1,500 | 0 |

Round-trip outputs in this audit were independently checked through coloured Levi-graph isomorphism using NetworkX.

## 9. Verification and falsification attempts

The candidate results were treated as potentially wrong and attacked in several ways:

- exhaustive enumeration of every connected labelled input through four vertices for multiple fixed pointer bounds;
- every possible root in the exhaustive round-trip test;
- every relabelling of each small isomorphism-class representative;
- explicit cross-class collision testing;
- deterministic larger random stress testing;
- independent Levi-graph isomorphism checks for the larger cases;
- direct one-token execution of the closure counterexample;
- enumeration of all feasible pointer assignments for the Fano C1 certificate;
- rerunning the full automated suite before repository publication.

All reported theorem-validation checks reproduced with zero failures, and both specification certificates reproduced exactly.

## 10. Frontier comparison

**Previously:** Conjectures 3.7 and 3.8 were explicitly open in the source preprint and supported empirically rather than proved; closure was asserted as a proposition; the Fano string was presented as canonical.

**Now:** the two conjectures are proved for the literal written formalism; the closure proposition has a shortest one-token counterexample plus a minimal repair; and the Fano example has an explicit local certificate showing violation of the written C1 rule.

The advance is therefore qualitative rather than merely larger-scale computation: two central open correctness questions change from conjecture to theorem, while two specification claims require correction.

## 11. Post-discovery novelty review

A dated search on August 7, 2026 used exact-title, conjecture-number, arXiv, general-web, and GitHub-targeted formulations. It found the original v1 preprint, mirrors, summaries, and unrelated hypergraph material, but no independent proof of either conjecture, no v2 or erratum, and no prior report of the singleton-closure or Fano C1 discrepancy.

This is evidence of novelty, not a guarantee; unpublished or unindexed work may exist. See `novelty_search_log.md`.

## 12. Why the result meets the predefined threshold

The predefined minor-breakthrough threshold required resolution of a central explicit open question for the full stated class, a material change in formal status, independent verification, and no located prior report. The study satisfies that threshold by resolving both central conjectures globally for the written algorithm and simultaneously correcting two specification claims. The classification is deliberately narrow: **minor breakthrough in the IsalHG research line**, subject to independent mathematical review, not a broad breakthrough in graph theory or hypergraph isomorphism generally.

## 13. Limitations

1. The study has not undergone external peer review.
2. The theorem claims apply to the literal written C1–C5 algorithm in arXiv:2607.10194v1, not to unavailable software.
3. The Fano discrepancy indicates that prose, example, and implementation may not be identical.
4. The proofs cover finite connected undirected duplicate-free hypergraphs with edge sizes between two and fixed `k`; extensions require separate proofs.
5. Canonical correctness does not imply computational efficiency; exhaustive C5 branching may remain expensive.
6. Exhaustive computational validation stops at four vertices and is evidence supporting the implementation and proof audit, not the logical basis of the global theorems.
7. Novelty searches cannot rule out unpublished or unindexed prior work.

## 14. Scientific implications

The correctness question for the literal formalism is separated from the performance question. Future work can focus on symmetry pruning, stronger invariant cascades, memoisation, and branch reduction without needing to re-establish the basic equivalence between canonical-string equality and isomorphism, provided those optimisations preserve the search-tree equivariance used in the proof.

The closure defect also illustrates a general design lesson for generative instruction languages: total executability is not enough; every reachable state must still satisfy the semantic definition of the target object class.

Finally, the Fano discrepancy shows the value of publishing intermediate-state and tie-break certificates alongside worked canonical examples, so examples function as executable conformance tests rather than illustrations only.

## 15. Reproducibility

The reported reference environment was Python 3.13.5, NetworkX 3.6.1, Linux x86_64. The deterministic stress seed is `20260807`.

Expected exhaustive totals are:

- connected labelled hypergraph cases: 3,028
- casewise isomorphism classes: 278
- rooted round trips: 12,069
- canonical relabellings: 6,285
- failures: 0

Expected deterministic stress totals are:

- instances: 150
- rooted round trips: 975
- canonical relabellings: 1,500
- failures: 0

Machine-readable retained results are under `results/`.

## 16. Conclusion

Before this investigation, IsalHG's round-trip fidelity and canonical completeness were explicit central conjectures, while closure was presented as proved and the Fano-plane string was presented as canonical. This study establishes round-trip fidelity and canonical completeness for the literal formal algorithm, refutes closure as stated with a one-token counterexample, and identifies an explicit violation of the written C1 rule in the published Fano example.

Subject to independent review, the scientifically defensible conclusion is that the two central IsalHG conjectures are resolved for the written formalism and two published specification claims require correction.

## Reference

Mario Pascual-Gonzalez and Ezequiel Lopez-Rubio, *Instruction Set and Language for Hypergraphs*, arXiv:2607.10194v1, July 11, 2026.
