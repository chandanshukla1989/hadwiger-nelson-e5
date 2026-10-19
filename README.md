# e5 <= 2258: a 5-chromatic unit-distance graph in the plane with 2258 edges

This repository contains a 509-vertex, 2258-edge unit-distance graph in the
Euclidean plane with chromatic number 5, together with everything needed to
verify that claim independently.

It improves the previous best bound of **2259** edges (md-amer, 2026) by one
edge, and the published bound of **2406** edges (de Grey and Parts, 2022) by
148 edges.

## Records for 5-chromatic unit-distance graphs in the plane

| | vertices | edges |
|---|---|---|
| de Grey (2018), first such graph | 1581 | 7877 |
| Parts (2020), vertex-minimal | **509** | 2442 |
| de Grey & Parts (2022), published e5 bound | 509 | 2406 |
| md-amer (2026), submitted to Geombinatorics | 509 | 2259 |
| **this graph** | 509 | **2258** |

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

So this graph differs from `G*` in exactly three edges.

**The point worth taking away is methodological: edge-criticality is not
optimality.** A graph can be edge-critical and a core fixpoint and still not be
edge-minimal. Searches that stop at the first critical graph stop too early.

## Verification

Every check re-derives its facts from Parts's published coordinates and the
edge list in this repository; nothing is taken on trust from the search.

| # | check | result |
|---|---|---|
| 1 | 2258 edges, no duplicates, no self-loops | OK |
| 2 | every edge at **exact** unit distance in Q(sqrt3, sqrt5, sqrt11) | OK, 2258/2258 |
| 3 | subgraph of Parts's published 2442-edge graph | OK |
| 4 | 509 vertices, minimum degree 4 (so no vertex is removable) | OK |
| 5 | distinct from `G*`: neither a subset nor a superset | OK, 3 edges differ |
| 6 | chi >= 5: UNSAT with triangle (0,149,152) pinned to colours 0,1,2 | OK, 7s |
| 7 | chi >= 5: UNSAT with **no** pin and no symmetry breaking at all | OK, 337s |
| 8 | 5-colourable, so chi is exactly 5 | OK, 0 monochromatic edges |
| 9 | DRAT refutation checked by **drat-trim** | **s VERIFIED**, 4.6s |

Check 2 is integer arithmetic over the 8-dimensional basis of
Q(sqrt3, sqrt5, sqrt11) with all coordinates at denominator 96 - no floating
point and no tolerance anywhere.  Check 9 is the one that matters to a third
party, since drat-trim is not our code: it re-derived the refutation
independently, reporting 8636 of 9544 clauses and 89090 of 161594 lemmas in the
core over 5,401,810 resolution steps, with 0 RAT lemmas.

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

- `edges2258.json` - the graph, as vertex-index pairs into `v509e2442.vtx`
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
