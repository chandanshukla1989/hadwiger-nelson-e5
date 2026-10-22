# e5 <= 2243: 5-chromatic unit-distance graphs in the plane with few edges

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23462835.svg)](https://doi.org/10.5281/zenodo.23462835)

**Cite as:** Chandan Shukla, *e5 <= 2243: a 509-vertex, 2243-edge 5-chromatic
unit-distance graph*, 2026. DOI: [10.5281/zenodo.23462835](https://doi.org/10.5281/zenodo.23462835)

That DOI is Zenodo's *concept* DOI: it always resolves to the newest version, so
it stays correct as the bound improves.  To pin to this exact graph instead, use
the version DOI of release v1.11, shown on the Zenodo record the badge
above links to.

*(This repository was briefly named `hadwiger-nelson-e5-2258`; GitHub redirects
that URL here, so older links still work.)*

---

A 509-vertex unit-distance graph in the Euclidean plane with chromatic number 5
and **2243 edges**, together with everything needed to verify that claim
independently.

## Records for 5-chromatic unit-distance graphs in the plane

| | vertices | edges |
|---|---|---|
| de Grey (2018), first such graph | 1581 | 7877 |
| Parts (2020), vertex-minimal | **509** | 2442 |
| de Grey & Parts (2022), published e5 bound | 509 | 2406 |
| md-amer (2026), submitted to Geombinatorics | 509 | 2259 |
| **this repository** | 509 | **2243** |

That is **163 edges** below the published bound and **16** below the previous
best.  The vertex record of 509 (Parts, 2020) is untouched: every graph here
uses exactly Parts's 509 points.

## How it was obtained

The construction method, and the intermediate graphs it passed through, are
withheld pending publication.

This does not affect checking the result.  `verify.py` re-derives every claim
from Parts's published coordinates using exact integer arithmetic, and the DRAT
refutation can be regenerated from the graph alone by any SAT solver that emits
proofs.  None of that needs the method.

## Verification

```
pip install sympy python-sat[pblib,aiger]
python verify.py edges2243.json          # checks 1-6 and 8
python verify.py edges2243.json --full   # adds the unpinned UNSAT (slow)
```

`verify.py` re-derives every fact from Parts's published coordinates:

| # | check | result |
|---|---|---|
| 1 | edge count, no duplicates, no self-loops | OK, 2243 |
| 2 | every edge at **exact** unit distance in Q(sqrt3, sqrt5, sqrt11) | OK, 2243/2243 |
| 3 | subgraph of Parts's published 2442-edge graph | OK |
| 4 | 509 vertices, minimum degree 4 (so no vertex is removable) | OK |
| 5 | the pinned triangle has all three of its edges in the graph | OK |
| 6 | chi >= 5: UNSAT with that triangle pinned to colours 0,1,2 | OK, 9s |
| 8 | 5-colourable, so chi is exactly 5 | OK, 0 monochromatic edges |

Check 2 is integer arithmetic over the 8-dimensional basis of
Q(sqrt3, sqrt5, sqrt11), all coordinates at denominator 96 - no floating point
and no tolerance anywhere.  Check 6 is a complete proof of chi >= 5, since
fixing a present triangle's colours is without loss of generality by
colour-permutation symmetry.

The DRAT refutation itself was checked with drat-trim (`s VERIFIED`, 10,323,668
resolution steps, 150,322 of 236,737 lemmas in core); the proof files are large
and are not kept in the repository for now.  They can be regenerated from `edges2243.json` by any SAT solver that
emits DRAT.

## Files

- `edges2243.json` - the graph, as vertex-index pairs into `v509e2442.vtx`
- `v509e2442.vtx` - Parts's 509 points, algebraic coordinates, unchanged
- `parts_edges2442.json` - Parts's published 2442 edges, unchanged (for check 3)
- `verify.py` - verifies any of the above; trusts nothing from the search
- `mq.py`, `loadvtx.py` - exact arithmetic in Q(sqrt3, sqrt5, sqrt11)


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
