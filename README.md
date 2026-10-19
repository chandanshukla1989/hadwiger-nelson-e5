# e5 <= 2251: 5-chromatic unit-distance graphs in the plane with few edges

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23462835.svg)](https://doi.org/10.5281/zenodo.23462835)

**Cite as:** Chandan Shukla, *e5 <= 2251: a 509-vertex, 2251-edge 5-chromatic
unit-distance graph*, 2026. DOI: [10.5281/zenodo.23462835](https://doi.org/10.5281/zenodo.23462835)

That DOI is Zenodo's *concept* DOI: it always resolves to the newest version, so
it stays correct as the bound improves.  Each release also has its own version
DOI if you need to pin to one specific graph.

*(The repository is named after the first graph in it.  The current best is
2251 edges; the name is kept so that links already in circulation keep working.)*

---

A 509-vertex unit-distance graph in the Euclidean plane with chromatic number 5
and **2251 edges**, together with everything needed to verify that claim
independently, and the chain of intermediate graphs that led to it.

## Records for 5-chromatic unit-distance graphs in the plane

| | vertices | edges |
|---|---|---|
| de Grey (2018), first such graph | 1581 | 7877 |
| Parts (2020), vertex-minimal | **509** | 2442 |
| de Grey & Parts (2022), published e5 bound | 509 | 2406 |
| md-amer (2026), submitted to Geombinatorics | 509 | 2259 |
| **this repository** | 509 | **2251** |

That is **155 edges** below the published bound and **8** below the previous
best.  The vertex record of 509 (Parts, 2020) is untouched: every graph here
uses exactly Parts's 509 points.

## How it was obtained

md-amer's 2259-edge graph `G*` is **edge-critical**: deleting any single edge
makes it 4-colourable.  Monotonicity then rules out deleting any *set* of edges,
since a subgraph of a 4-colourable graph is 4-colourable.  `G*` is moreover its
own UNSAT core - the refutation needs all 2259 of its edges - so core-guided
reduction cannot shrink it either.  By every standard test it looks final.

It is not.  Those tests do not cover a **plateau move**: add back one of the
edges previously deleted from Parts's graph, delete a *different* edge, and land
on an equal-sized but structurally different graph, which may itself have a
removable edge.  The first one:

```
plateau move : + (16, 202)   -> 2260 edges
               - (16, 167)   -> 2259 edges, a different graph
descent      : - (64, 124)   -> 2258 edges
```

Repeating that gives the chain

```
2259  ->  2258  ->  2257  ->  2256  ->  2255  ->  2253  ->  2252  ->  2251
```

Each graph in the chain was edge-critical when it was reached, and each was
broken the same way.

**The point worth taking away is methodological: edge-criticality is not
edge-minimality.**  A graph can be edge-critical, 2-edge-critical, and an
UNSAT-core fixpoint and still not be edge-minimal.  Searches that stop at the
first critical graph stop too early - which may be why the bound sat at 2406
for four years.

## Verification

```
pip install sympy python-sat[pblib,aiger]
python verify.py edges2251.json          # checks 1-6 and 8
python verify.py edges2251.json --full   # adds the unpinned UNSAT (slow)
```

`verify.py` takes any edge list in this repository and re-derives every fact
from Parts's published coordinates.  It checks, in order:

| # | check | result for `edges2251.json` |
|---|---|---|
| 1 | edge count, no duplicates, no self-loops | OK, 2251 |
| 2 | every edge at **exact** unit distance in Q(sqrt3, sqrt5, sqrt11) | OK, 2251/2251 |
| 3 | subgraph of Parts's published 2442-edge graph | OK |
| 4 | 509 vertices, minimum degree 4 (so no vertex is removable) | OK |
| 5 | the pinned triangle has all three of its edges in the graph | OK |
| 6 | chi >= 5: UNSAT with that triangle pinned to colours 0,1,2 | OK, 6s |
| 7 | chi >= 5: UNSAT with **no** pin and no symmetry breaking | OK |
| 8 | 5-colourable, so chi is exactly 5 | OK, 0 monochromatic edges |

Check 2 is integer arithmetic over the 8-dimensional basis of
Q(sqrt3, sqrt5, sqrt11), all coordinates at denominator 96 - no floating point
and no tolerance anywhere.  Check 6 is already a complete proof of chi >= 5,
since fixing a present triangle's colours is without loss of generality by
colour-permutation symmetry; check 7 removes even that assumption.

Independently of `verify.py`, each graph has a DRAT refutation checked by
**drat-trim**, which is not our code:

```
drat-trim certificates/4col_2251_pinned.cnf certificates/4col_2251_pinned.drat
```

```
s VERIFIED      8641 of 9516 clauses in core
                121016 of 202955 lemmas in core
                8305689 resolution steps, 0 RAT lemmas
```

As a by-product, md-amer's `G*` was itself re-verified here before being used as
a base: exact unit distances, unpinned UNSAT, an explicit 5-colouring, and
exhaustive 1- and 2-edge-criticality over all 2259 single edges and all
2,550,411 edge pairs.

## Files

- `edges2251.json` - the best graph, as vertex-index pairs into `v509e2442.vtx`
- `edges2252.json` ... `edges2258.json` - the intermediate graphs
- `v509e2442.vtx` - Parts's 509 points, algebraic coordinates, unchanged
- `verify.py` - verifies any of the above; trusts nothing from the search
- `mq.py`, `loadvtx.py` - exact arithmetic in Q(sqrt3, sqrt5, sqrt11)
- `shrink2259.py`, `drat2258.py` - the plateau search, and DRAT emission
- `certificates/` - per graph: the DIMACS CNF, the DRAT refutation, the
  drat-trim log, an explicit 5-colouring, and the edge-level diff against the
  graph it came from

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
