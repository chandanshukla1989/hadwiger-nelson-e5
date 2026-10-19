"""Full independent verification of the claimed 2258-edge graph.

Trusts nothing from the search: re-derives every fact from Parts's published
coordinates and the claimed edge list.
"""
import json, time, collections
import mq
from loadvtx import load_exact
from pysat.solvers import Cadical153

CLAIM = 'shrink2259_best_2258_s104.json'
print("=" * 64)
print("VERIFYING", CLAIM)
print("=" * 64, flush=True)

L, V = load_exact('v509e2442.vtx')
E = [tuple(sorted(e)) for e in json.load(open(CLAIM))]
E2442 = {tuple(sorted(e)) for e in json.load(open('edges509.json'))}
E2259 = {tuple(sorted(e)) for e in json.load(open('edges2259.json'))}

# 1. basic shape
print(f"\n[1] edges                : {len(E)}")
print(f"    duplicates           : {len(E) - len(set(E))}")
print(f"    self-loops           : {sum(1 for a, b in E if a == b)}")
ok_count = (len(E) == 2258 and len(E) == len(set(E))
            and all(a != b for a, b in E))
print(f"    => {'OK' if ok_count else 'FAIL'}", flush=True)

# 2. every edge is EXACTLY a unit distance in Q(sqrt3,sqrt5,sqrt11)
target = tuple([L * L] + [0] * 7)
bad = []
for a, b in E:
    dx = tuple(p - q for p, q in zip(V[a][:8], V[b][:8]))
    dy = tuple(p - q for p, q in zip(V[a][8:], V[b][8:]))
    s = tuple(p + q for p, q in zip(mq.mul(dx, dx), mq.mul(dy, dy)))
    if s != target:
        bad.append((a, b))
print(f"\n[2] exact unit-distance  : {len(E)-len(bad)}/{len(E)}   (scale L={L})")
print(f"    => {'OK' if not bad else 'FAIL ' + str(bad[:3])}", flush=True)

# 3. subgraph of Parts's published graph
sub = set(E) <= E2442
print(f"\n[3] subgraph of Parts    : {sub}")
print(f"    => {'OK' if sub else 'FAIL'}", flush=True)

# 4. vertices and degrees
deg = collections.Counter()
for a, b in E:
    deg[a] += 1; deg[b] += 1
mind = min(deg.values())
print(f"\n[4] vertices used        : {len(deg)}")
print(f"    min / max degree     : {mind} / {max(deg.values())}")
print(f"    => min degree >= 4: {'OK' if mind >= 4 else 'FAIL (vertex removable!)'}", flush=True)

# 5. relation to md-amer's 2259
print(f"\n[5] vs md-amer 2259      : subset={set(E) <= E2259}  superset={E2259 <= set(E)}")
print(f"    edges differing      : {len(set(E) ^ E2259)}", flush=True)

n = 1 + max(max(e) for e in E)


def colourable(k, pin=None, proof=False):
    X = lambda v, c: 1 + k * v + c
    cls = [[X(v, c) for c in range(k)] for v in range(n)]
    for a, b in E:
        for c in range(k):
            cls.append([-X(a, c), -X(b, c)])
    if pin:
        for t, v in enumerate(pin):
            cls.append([X(v, t)])
    S = Cadical153(bootstrap_with=cls, with_proof=proof)
    t = time.time(); r = S.solve(); el = time.time() - t
    m = S.get_model() if r else None
    pr = S.get_proof() if (proof and r is False) else None
    S.delete()
    return r, el, m, pr, cls


# 6. non-4-colourable with a VALID pin
A = collections.defaultdict(set)
for a, b in E:
    A[a].add(b); A[b].add(a)
ES = set(E)
tri = None
for a, b in E:
    com = A[a] & A[b]
    if com:
        tri = (a, b, min(com)); break
tri_ok = all(tuple(sorted(p)) in ES
             for p in ((tri[0], tri[1]), (tri[0], tri[2]), (tri[1], tri[2])))
r4p, t4p, _, _, _ = colourable(4, pin=tri)
print(f"\n[6] pin triangle         : {tri}   all 3 edges present: {tri_ok}")
print(f"    4-colourable (pinned): {r4p}   ({t4p:.0f}s)")
print(f"    => {'OK (chi >= 5)' if (r4p is False and tri_ok) else 'FAIL'}", flush=True)

# 7. non-4-colourable with NO pin at all
r4, t4, _, pr, cls4 = colourable(4, pin=None, proof=True)
print(f"\n[7] 4-colourable (no pin): {r4}   ({t4:.0f}s)")
print(f"    => {'OK (chi >= 5, unconditional)' if r4 is False else 'FAIL'}", flush=True)

# 8. 5-colourable, so chi is exactly 5
r5, t5, m5, _, _ = colourable(5)
mono = None
if r5:
    X = lambda v, c: 1 + 5 * v + c
    mm = set(l for l in m5 if l > 0)
    cols = {v: [c for c in range(5) if X(v, c) in mm][0] for v in range(n)}
    mono = sum(1 for a, b in E if cols[a] == cols[b])
    json.dump(cols, open('col5_2258.json', 'w'))
print(f"\n[8] 5-colourable         : {r5}   ({t5:.0f}s)   monochromatic edges: {mono}")
print(f"    => {'OK' if (r5 and mono == 0) else 'FAIL'}", flush=True)

# 9. write CNF + DRAT for independent checking
if pr:
    with open('4col_2258.cnf', 'w') as f:
        f.write(f"p cnf {4*n} {len(cls4)}\n")
        for c in cls4:
            f.write(' '.join(map(str, c)) + " 0\n")
    with open('4col_2258.drat', 'w') as f:
        f.write('\n'.join(pr) + '\n')
    print(f"\n[9] DRAT proof written   : {len(pr)} lines -> 4col_2258.drat", flush=True)

print("\n" + "=" * 64)
verdict = (ok_count and not bad and sub and mind >= 4
           and r4p is False and tri_ok and r4 is False and r5 and mono == 0)
print("VERDICT:", "ALL CHECKS PASSED - 2258 edges, chi = 5" if verdict else "FAILED")
print("=" * 64, flush=True)
