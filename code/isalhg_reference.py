#!/usr/bin/env python3
"""Independent, literal reference model of Algorithms 1--2 in arXiv:2607.10194v1.
Used only for finite verification of the proof; not author code.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations
from typing import Iterable

# Token ordering in Definition 3.5: W < N < P < V < C.
W, N, P, V, C = 0, 1, 2, 3, 4
Token = tuple[int, ...]
Edge = frozenset[int]


def primal_adjacency(n: int, edges: tuple[Edge, ...]) -> list[set[int]]:
    A=[set() for _ in range(n)]
    for e in edges:
        for u,v in combinations(e,2):
            A[u].add(v); A[v].add(u)
    return A


def is_connected(n: int, edges: tuple[Edge,...]) -> bool:
    if n<=1: return True
    A=primal_adjacency(n,edges)
    seen={0}; stack=[0]
    while stack:
        u=stack.pop()
        for v in A[u]-seen: seen.add(v); stack.append(v)
    return len(seen)==n


def xi_tuples(n:int, edges:tuple[Edge,...]) -> tuple[tuple[int,int,int],...]:
    A=primal_adjacency(n,edges); out=[]
    for s in range(n):
        dist=[None]*n; dist[s]=0; q=[s]
        for u in q:
            for v in A[u]:
                if dist[v] is None: dist[v]=dist[u]+1; q.append(v)
        out.append(tuple(sum(d==h for d in dist if d is not None) for h in (1,2,3)))
    return tuple(out)


def eta(edge:Edge, xis:tuple[tuple[int,int,int],...])->tuple[int,int,int]:
    return tuple(sum(xis[v][j] for v in edge) for j in range(3))


def shortest_delta(cdll:tuple[int,...], current:int, target:int)->int:
    L=len(cdll); c=cdll.index(current); t=cdll.index(target)
    f=(t-c)%L
    b=f-L if f else 0
    return min((f,b), key=lambda d:(abs(d),d))


def movement_tokens(delta:tuple[int,...])->tuple[Token,...]:
    out=[]
    # retreats before advances, pointer index ascending
    for i,d in enumerate(delta,1):
        if d<0: out.extend([(N,i)]*(-d))
    for i,d in enumerate(delta,1):
        if d>0: out.extend([(P,i)]*d)
    return tuple(out)


def move_pointers(cdll:tuple[int,...], ptrs:tuple[int,...], delta:tuple[int,...])->tuple[int,...]:
    L=len(cdll); pos={u:i for i,u in enumerate(cdll)}
    return tuple(cdll[(pos[p]+d)%L] for p,d in zip(ptrs,delta))


def insert_after(cdll:tuple[int,...], anchor:int, newnodes:tuple[int,...])->tuple[int,...]:
    i=cdll.index(anchor)
    return cdll[:i+1]+newnodes+cdll[i+1:]


def encode_rooted(n:int, edges:tuple[Edge,...], k:int, start:int)->tuple[Token,...]:
    edges=tuple(sorted(edges,key=lambda e:tuple(sorted(e))))
    xis=xi_tuples(n,edges)
    etas=tuple(eta(e,xis) for e in edges)
    all_wait=(1<<len(edges))-1

    @lru_cache(maxsize=None)
    def rec(cdll:tuple[int,...], ptrs:tuple[int,...], mapping:tuple[int,...], wait:int)->tuple[Token,...]:
        # mapping[machine_node] = input vertex; machine ids are 0..len(mapping)-1.
        if wait==0: return ()
        inv={v:i for i,v in enumerate(mapping)}
        materialized=set(mapping)
        candidates=[]
        for ei,e in enumerate(edges):
            if not (wait>>ei)&1: continue
            me=sorted(e & materialized)
            if not me: continue
            ue=sorted(e-materialized)
            i=len(me); j=len(ue)
            assert i>=1 and i+j==len(e)<=k
            # Find the unique C1-minimal displacement over assignments of members to p1..pi.
            best_delta=None; best_dkey=None
            for assn in permutations(me):
                ds=[]
                for ell in range(k):
                    if ell<i: ds.append(shortest_delta(cdll,ptrs[ell],inv[assn[ell]]))
                    else: ds.append(0)
                ds=tuple(ds)
                dkey=(sum(abs(x) for x in ds),tuple(abs(x) for x in ds),ds)
                if best_dkey is None or dkey<best_dkey:
                    best_dkey=dkey; best_delta=ds
            kind=0 if j else 1 # C2: V before C
            token_key=(i,j) if j else (i,)
            ckey=(best_dkey,kind,token_key,etas[ei])
            candidates.append((ckey,ei,best_delta,tuple(ue),i,j))
        assert candidates, "connectivity/progress invariant failed"
        bestkey=min(c[0] for c in candidates)
        tied=[c for c in candidates if c[0]==bestkey]
        best_string=None
        for _,ei,delta,ue,i,j in tied:
            moved=move_pointers(cdll,ptrs,delta)
            prefix=movement_tokens(delta)
            if j:
                tok=(V,i,j); newids=tuple(range(len(mapping),len(mapping)+j))
                new_cdll=insert_after(cdll,moved[0],newids)
                # C5 branches over all assignments of unmaterialized members to insertion positions.
                for assignment in permutations(ue):
                    newmap=mapping+tuple(assignment)
                    suffix=rec(new_cdll,moved,newmap,wait^(1<<ei))
                    s=prefix+(tok,)+suffix
                    if best_string is None or s<best_string: best_string=s
            else:
                tok=(C,i)
                suffix=rec(cdll,moved,mapping,wait^(1<<ei))
                s=prefix+(tok,)+suffix
                if best_string is None or s<best_string: best_string=s
        assert best_string is not None
        return best_string

    return rec((0,),tuple([0]*k),(start,),all_wait)


def canonical_string(n:int, edges:tuple[Edge,...], k:int)->tuple[Token,...]:
    xis=xi_tuples(n,edges)
    maxxi=max(xis)
    return min(encode_rooted(n,edges,k,v) for v in range(n) if xis[v]==maxxi)


def decode(tokens:tuple[Token,...], k:int)->tuple[int,tuple[Edge,...]]:
    cdll=[0]; ptrs=[0]*k; edges:set[Edge]=set(); nextid=1
    for t in tokens:
        kind=t[0]
        if kind==N or kind==P:
            i=t[1]-1; pos=cdll.index(ptrs[i]); step=-1 if kind==N else 1
            ptrs[i]=cdll[(pos+step)%len(cdll)]
        elif kind==V:
            i,j=t[1],t[2]; new=tuple(range(nextid,nextid+j)); nextid+=j
            pos=cdll.index(ptrs[0]); cdll[pos+1:pos+1]=new
            edges.add(frozenset(ptrs[:i])|frozenset(new))
        elif kind==C:
            i=t[1]; edges.add(frozenset(ptrs[:i]))
        elif kind==W: pass
        else: raise ValueError(t)
    return nextid,tuple(sorted(edges,key=lambda e:tuple(sorted(e))))


def relabel_edges(edges:tuple[Edge,...],perm:tuple[int,...])->tuple[Edge,...]:
    return tuple(sorted((frozenset(perm[v] for v in e) for e in edges),key=lambda e:tuple(sorted(e))))


def brute_iso_key(n:int,edges:tuple[Edge,...])->tuple[tuple[int,...],...]:
    # Canonicalize by applying each vertex permutation exactly once, sorting
    # the vertices inside each edge and then sorting the edge family.
    return min(
        tuple(sorted(tuple(sorted(perm[v] for v in e)) for e in edges))
        for perm in permutations(range(n))
    )


def token_text(s:tuple[Token,...])->str:
    names={W:'W',N:'N',P:'P',V:'V',C:'C'}
    return ' '.join(names[t[0]]+('' if len(t)==1 else '_'+','.join(map(str,t[1:]))) for t in s)
