import json,time,collections
from pysat.solvers import Cadical153
E=[tuple(sorted(e)) for e in json.load(open('shrink2259_best_2258_s104.json'))]
n=1+max(max(e) for e in E); ES=set(E)
A=collections.defaultdict(set)
for a,b in E: A[a].add(b); A[b].add(a)
tri=None
for a,b in E:
    com=A[a]&A[b]
    if com: tri=(a,b,min(com)); break
ok=all(tuple(sorted(p)) in ES for p in ((tri[0],tri[1]),(tri[0],tri[2]),(tri[1],tri[2])))
print(f"pin triangle {tri}, all 3 edges present: {ok}",flush=True)
assert ok
X=lambda v,c: 1+4*v+c
cls=[[X(v,c) for c in range(4)] for v in range(n)]
for a,b in E:
    for c in range(4): cls.append([-X(a,c),-X(b,c)])
for t,v in enumerate(tri): cls.append([X(v,t)])
with open('4col_2258_pinned.cnf','w') as f:
    f.write(f"p cnf {4*n} {len(cls)}\n")
    for c in cls: f.write(' '.join(map(str,c))+" 0\n")
print(f"CNF: {4*n} vars, {len(cls)} clauses",flush=True)
S=Cadical153(bootstrap_with=cls,with_proof=True)
t=time.time(); r=S.solve(); el=time.time()-t
print(f"solve: {'SAT' if r else 'UNSAT'}  ({el:.0f}s)",flush=True)
assert r is False
pr=S.get_proof()
with open('4col_2258_pinned.drat','w') as f: f.write('\n'.join(pr)+'\n')
print(f"DRAT: {len(pr)} lines",flush=True)
