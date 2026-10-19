"""Shrink md-amer's 2259-edge graph by plateau moves, then descend.

Their graph G is edge-critical, so nothing comes off directly, and monotonicity
kills every k-edge deletion.  What is NOT closed: add one of the 183 edges they
removed back (call it r) and take some OTHER edge e off.  That lands at 2259
again but on a DIFFERENT graph, which may itself have a removable edge.

Each worker samples (r, e) pairs in its own random order, and on a successful
plateau move immediately tries every single-edge deletion from the new graph.
"""
import json, os, random, time, collections
from pysat.solvers import Cadical153

SEED = int(os.environ['SEED']); TAG = os.environ['TAG']
MODE = os.environ.get('MODE', 'random')   # random | greedy

ALL = [tuple(sorted(e)) for e in json.load(open('edges509.json'))]
BASE = {tuple(sorted(e)) for e in json.load(open('edges2259.json'))}
IDX = {e: i for i, e in enumerate(ALL)}
M = len(ALL); n = 1 + max(max(e) for e in ALL)
X = lambda v, c: 1 + 4 * v + c
Se = lambda i: 1 + 4 * n + i
cls = [[X(v, c) for c in range(4)] for v in range(n)]
for i, (a, b) in enumerate(ALL):
    for c in range(4):
        cls.append([-Se(i), -X(a, c), -X(b, c)])
S = Cadical153(bootstrap_with=cls)
rnd = random.Random(SEED)

base = set(IDX[e] for e in BASE)
off = [i for i in range(M) if i not in base]


def pin(s):
    A = collections.defaultdict(set)
    for i in s:
        a, b = ALL[i]; A[a].add(b); A[b].add(a)
    for i in s:
        a, b = ALL[i]; com = A[a] & A[b]
        if com:
            return (a, b, min(com))
    return None


def nocol4(s):
    p = pin(s)
    asm = [Se(i) if i in s else -Se(i) for i in range(M)]
    if p:
        asm += [X(p[0], 0), X(p[1], 1), X(p[2], 2)]
    return S.solve(assumptions=asm) is False


assert nocol4(base), "their 2259 graph is 4-colourable?!"
print(f"[{TAG}] base |E|={len(base)}  add-backs available={len(off)}  mode={MODE}", flush=True)

t0 = time.time(); tested = 0; moves = 0; cur = set(base)
while True:
    r = rnd.choice([i for i in range(M) if i not in cur])
    sup = cur | {r}
    cands = [i for i in cur]
    if MODE == 'greedy':
        deg = collections.Counter()
        for i in cur:
            a, b = ALL[i]; deg[a] += 1; deg[b] += 1
        cands.sort(key=lambda i: -(deg[ALL[i][0]] + deg[ALL[i][1]]))
    else:
        rnd.shuffle(cands)
    hit = None
    for e in cands[:400]:            # bounded probe per r, then pick a new r
        tested += 1
        if nocol4(sup - {e}):
            hit = e; break
        if tested % 200 == 0:
            print(f"[{TAG}] {tested} pairs tested, {moves} plateau moves "
                  f"({time.time()-t0:.0f}s)", flush=True)
    if hit is None:
        continue
    cur = sup - {hit}
    moves += 1
    print(f"[{TAG}] PLATEAU MOVE {moves}: +{r} -{hit}, |E|={len(cur)} "
          f"({time.time()-t0:.0f}s)", flush=True)
    json.dump([list(ALL[i]) for i in sorted(cur)], open(f'shrink2259_{TAG}.json', 'w'))
    # new 2259 graph: can anything come off it now?
    order = list(cur); rnd.shuffle(order)
    for e in order:
        if nocol4(cur - {e}):
            cur = cur - {e}
            print(f"[{TAG}] *** DESCENT: |E|={len(cur)} after {moves} moves "
                  f"({time.time()-t0:.0f}s) ***", flush=True)
            json.dump([list(ALL[i]) for i in sorted(cur)],
                      open(f'shrink2259_best_{len(cur)}_{TAG}.json', 'w'))
            if len(cur) < 2259:
                print(f"[{TAG}] *** BELOW 2259 = RECORD CANDIDATE: {len(cur)} ***", flush=True)
            break
