"""Verify any graph in this repository.

    python verify.py edges2251.json

Re-derives every fact from Parts's published coordinates and the edge list.
Nothing is taken on trust from the search that produced the graph.
"""
import sys, json, time, collections
import mq
from loadvtx import load_exact
from pysat.solvers import Cadical153

path = sys.argv[1] if len(sys.argv) > 1 else 'edges2251.json'
L, V = load_exact('v509e2442.vtx')
E = [tuple(sorted(e)) for e in json.load(open(path))]
PARTS = {tuple(sorted(e)) for e in json.load(open('parts_edges2442.json'))} \
    if __import__('os').path.exists('parts_edges2442.json') else None

print(f"verifying {path}")
print("=" * 60)

ok = True

print(f"[1] edges                  : {len(E)}")
dups = len(E) - len(set(E)); loops = sum(1 for a, b in E if a == b)
print(f"    duplicates / self-loops: {dups} / {loops}")
ok &= (dups == 0 and loops == 0)

target = tuple([L * L] + [0] * 7)
bad = 0
for a, b in E:
    dx = tuple(p - q for p, q in zip(V[a][:8], V[b][:8]))
    dy = tuple(p - q for p, q in zip(V[a][8:], V[b][8:]))
    if tuple(p + q for p, q in zip(mq.mul(dx, dx), mq.mul(dy, dy))) != target:
        bad += 1
print(f"[2] exact unit distance    : {len(E)-bad}/{len(E)}   (integer arithmetic, "
      f"coordinates at denominator {L})")
ok &= (bad == 0)

if PARTS is not None:
    sub = set(E) <= PARTS
    print(f"[3] subgraph of Parts 2442 : {sub}")
    ok &= sub

deg = collections.Counter()
for a, b in E:
    deg[a] += 1; deg[b] += 1
print(f"[4] vertices / min degree  : {len(deg)} / {min(deg.values())}")
ok &= (min(deg.values()) >= 4)

n = 1 + max(max(e) for e in E)
ES = set(E)
A = collections.defaultdict(set)
for a, b in E:
    A[a].add(b); A[b].add(a)
tri = next(((a, b, min(A[a] & A[b])) for a, b in E if A[a] & A[b]), None)
tri_ok = tri and all(tuple(sorted(p)) in ES for p in
                     ((tri[0], tri[1]), (tri[0], tri[2]), (tri[1], tri[2])))


def colour(k, pin=None):
    X = lambda v, c: 1 + k * v + c
    cls = [[X(v, c) for c in range(k)] for v in range(n)]
    for a, b in E:
        for c in range(k):
            cls.append([-X(a, c), -X(b, c)])
    if pin:
        for t, v in enumerate(pin):
            cls.append([X(v, t)])
    S = Cadical153(bootstrap_with=cls)
    t = time.time(); r = S.solve(); el = time.time() - t
    m = S.get_model() if r else None
    S.delete()
    return r, el, m


r4p, t4p, _ = colour(4, pin=tri)
print(f"[5] pin triangle           : {tri}, all three edges present: {tri_ok}")
print(f"[6] 4-colourable (pinned)  : {r4p}   ({t4p:.0f}s)")
ok &= (r4p is False and tri_ok)

if '--full' in sys.argv:
    r4, t4, _ = colour(4)
    print(f"[7] 4-colourable (no pin)  : {r4}   ({t4:.0f}s)")
    ok &= (r4 is False)
else:
    print("[7] 4-colourable (no pin)  : skipped, pass --full (can take 20+ min)")

r5, t5, m5 = colour(5)
mono = None
if r5:
    X = lambda v, c: 1 + 5 * v + c
    mm = set(l for l in m5 if l > 0)
    cols = {v: [c for c in range(5) if X(v, c) in mm][0] for v in range(n)}
    mono = sum(1 for a, b in E if cols[a] == cols[b])
print(f"[8] 5-colourable           : {r5}   ({t5:.0f}s), monochromatic edges: {mono}")
ok &= (r5 and mono == 0)

print("=" * 60)
print("VERDICT:", f"VERIFIED - {len(E)} edges, chi = 5" if ok else "FAILED")
