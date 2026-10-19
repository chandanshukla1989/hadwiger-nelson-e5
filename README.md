# e5 <= 2251: a 5-chromatic unit-distance graph in the plane with 2255 edges

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23462835.svg)](https://doi.org/10.5281/zenodo.23462835)

This DOI is the Zenodo *concept* DOI: it always resolves to the newest version,
so it stays correct as the bound improves.  Each release also has its own
version DOI if you need to pin to a specific graph.

**Cite as:** Chandan Shukla, *e5 <= 2251: a 509-vertex, 2251-edge 5-chromatic
unit-distance graph*, 2026. DOI: [10.5281/zenodo.23462835](https://doi.org/10.5281/zenodo.23462835)

This repository contains 509-vertex unit-distance graphs in the Euclidean plane
with chromatic number 5 and **2257** and **2258** edges, together with
everything needed to verify those claims independently.

They improve the previous best bound of **2259** edges (md-amer, 2026) by eight
edges, and the published bound of **2406** edges (de Grey and Parts, 2022) by
155 edges.

## Records for 5-chromatic unit-distance graphs in the plane

| | vertices | edges |
|---|---|---|
| de Grey (2018), first such graph | 1581 | 7877 |
| Parts (2020), vertex-minimal | **509** | 2442 |
| de Grey & Parts (2022), published e5 bound | 509 | 2406 |
| md-amer (2026), submitted to Geombinatorics | 509 | 2259 |
| this repository, first graph | 509 | 2258 |
| this repository | 509 | 2257 |
| this repository | 509 | 2256 |
| this repository | 509 | 2255 |
| this repository | 509 | 2253 |
| this repository | 509 | 2252 |
| **this repository, best** | 509 | **2251** |

The vertex record of 509 (Parts, 2020) is untouched - this graph uses exactly
Parts's 509 points.

## How it was obtained

md-amer's 2259-edge graph `G*` is **edge-critical**: deleting any single edge
makes it 4-colourable.  Monotonicity then rules out deleting any *set* of
edges, since a subgraph of a 4-colourable graph is 4-colourable.  `G*` is
moreover its own UNSAT core - the refutation needs every one of its 2259 edges -
so core-guided reduction cannot shrink it either.  By every standard test it
looks final.

It is not.  What those tests do not cover is a **plateau move**: add back one of
the edges previously deleted from Parts's graph, delete a *different* edge, and
land on an equal-sized but structurally different graph, which may itself have a
removable edge.  Here one such move was enough:

```
plateau move : + (16, 202)              -> 2260 edges
               - (16, 167)              -> 2259 edges, a different graph
descent      : - (64, 124)              -> 2258 edges
```

So the 2258-edge graph differs from `G*` in exactly three edges.

Repeating the same move on the 2258-edge graph gives one more edge:

```
plateau move : + (41, 263)              -> 2259 edges
               - (49, 56)               -> 2258 edges, a different graph
descent      : - (76, 197)              -> 2257 edges
```

The 2257-edge graph therefore differs from `G*` in six edges.  That the move
worked twice, on two graphs that each passed every criticality test available,
is the substance of the observation below.

**The point worth taking away is methodological: edge-criticality is not
optimality.** A graph can be edge-critical and a core fixpoint and still not be
edge-minimal. Searches that stop at the first critical graph stop too early.

## Verification

Every check re-derives its facts from Parts's published coordinates and the
edge list in this repository; nothing is taken on trust from the search.

| # | check | result |
|---|---|---|
Both graphs pass the same nine checks; the figures below are for the 2257-edge
graph, with the 2258-edge graph's certificates alongside in `certificates/`.

| # | check | result |
|---|---|---|
| 1 | 2257 edges, no duplicates, no self-loops | OK |
| 2 | every edge at **exact** unit distance in Q(sqrt3, sqrt5, sqrt11) | OK, 2257/2257 |
| 3 | subgraph of Parts's published 2442-edge graph | OK |
| 4 | 509 vertices, minimum degree 4 (so no vertex is removable) | OK |
| 5 | distinct from `G*`: neither a subset nor a superset | OK, 6 edges differ |
| 6 | chi >= 5: UNSAT with a pinned triangle (all three of its edges present) | OK, 8s |
| 7 | chi >= 5: UNSAT with **no** pin and no symmetry breaking at all | OK, 1259s (2257: 379s, 2258: 337s) |
| 8 | 5-colourable, so chi is exactly 5 | OK, 0 monochromatic edges |

Four independent search workers reached 2257 edges from 2258 by the same kind of
plateau move, so that descent is reproducible rather than a single lucky run.
| 9 | DRAT refutation checked by **drat-trim** | **s VERIFIED**, 5.8s |

Check 2 is integer arithmetic over the 8-dimensional basis of
Q(sqrt3, sqrt5, sqrt11) with all coordinates at denominator 96 - no floating
point and no tolerance anywhere.  Check 9 is the one that matters to a third
party, since drat-trim is not our code: it re-derived the refutation
independently, reporting 8637 of 9540 clauses and 99931 of 182297 lemmas in the
core over 6,573,273 resolution steps, with 0 RAT lemmas (and 5,401,810 steps
for the 2258-edge graph).

As a by-product, md-amer's `G*` was itself re-verified here before being used as
a base: exact unit distances, unpinned UNSAT, an explicit 5-colouring, and
exhaustive 1- and 2-edge-criticality (all 2259 single edges and all 2,550,411
edge pairs).

## Reproducing the verification

```
pip install sympy python-sat[pblib,aiger]
python verify2258.py          # checks 1-6, and 7-8 unpinned
python drat2258.py            # writes the CNF and a DRAT refutation
drat-trim certificates/4col_2258_pinned.cnf certificates/4col_2258_pinned.drat
```

## Files

- `edges2251.json` - the best graph
- `edges2252.json` - the 2252-edge graph
- `edges2253.json` - the 2253-edge graph
- `edges2255.json` - the 2255-edge graph, as vertex-index pairs into `v509e2442.vtx`
- `edges2256.json` - the 2256-edge graph
- `edges2257.json` - the 2257-edge graph
- `edges2258.json` - the intermediate 2258-edge graph
- `v509e2442.vtx` - Parts's 509 points, algebraic coordinates, unchanged
- `verify2258.py` - checks 1-8; trusts nothing from the search
- `drat2258.py` - emits the DIMACS CNF and the DRAT refutation
- `shrink2259.py` - the plateau-move search that found this graph
- `mq.py`, `loadvtx.py` - exact arithmetic in Q(sqrt3, sqrt5, sqrt11)
- `certificates/`
  - `4col_2258_pinned.cnf` - "is this graph 4-colourable?" in DIMACS
  - `4col_2258_pinned.drat` - DRAT refutation (31 MB)
  - `drattrim_2258.log` - drat-trim output, `s VERIFIED`
  - `col5_2258.json` - an explicit proper 5-colouring
  - `diff_vs_2259.json` - the three edges that differ from `G*`

## References

- A. D. N. J. de Grey, "The chromatic number of the plane is at least 5",
  Geombinatorics 28 (2018), 18-31. arXiv:1804.02385
- J. Parts, "Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane", Geombinatorics 29(4) (2020), 137-166.
  arXiv:2010.12665
- A. D. N. J. de Grey and J. Parts, "On lower bounds of the order of
  k-chromatic unit distance graphs", Geombinatorics 32(2) (2022), 72-74.
  (e5 <= 2406, footnote 2)
- md-amer, "A 5-chromatic unit-distance graph in the plane with 2259 edges",
  submitted to Geombinatorics (2026).
  https://github.com/md-amer/hadwiger-nelson-e5
  commit 6d5ac08491f7cadbebd7d5b79e3f825d08eedf7b
