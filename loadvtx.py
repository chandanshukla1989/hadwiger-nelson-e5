"""Correct .vtx loader: compute the REAL common denominator per file and assert
exactness, instead of hardcoding L=96 (which silently truncated 553/610/633)."""
import math
from fractions import Fraction as F
import mq

def load_exact(path):
    P=mq.parse_vtx(path)
    L=1
    for x,y in P:
        for c in x+y:
            L = L*c.denominator//math.gcd(L, c.denominator)
    V=[]
    for x,y in P:
        row=[]
        for c in x+y:
            v=c*L
            assert v.denominator==1, f"scaling failed: {c} * {L}"
            row.append(int(v))
        V.append(tuple(row))
    return L, V

MULT,XOR=mq.MULT,mq.XOR
def imul(a,b):
    out=[0]*8
    for i in range(8):
        ai=a[i]
        if not ai: continue
        Mi,Xi=MULT[i],XOR[i]
        for j in range(8):
            if b[j]: out[Xi[j]]+=ai*b[j]*Mi[j]
    return out

def ud_edges(L, V):
    UNIT=tuple([L*L]+[0]*7); n=len(V); E=[]
    for i in range(n):
        xi,yi=V[i][:8],V[i][8:]
        for j in range(i+1,n):
            xj,yj=V[j][:8],V[j][8:]
            dx=tuple(a-b for a,b in zip(xi,xj)); dy=tuple(a-b for a,b in zip(yi,yj))
            if tuple(a+b for a,b in zip(imul(dx,dx),imul(dy,dy)))==UNIT: E.append((i,j))
    return E

if __name__=='__main__':
    import sys
    for name in ['510','517','529','553','610','633']:
        try:
            L,V = load_exact(f'heule/{name}.vtx')
            E = ud_edges(L,V)
            # compare with Heule's own edge file if present
            import os
            ref=None
            p=f'heule/{name}.edge'
            if os.path.exists(p):
                ref=int(open(p).readline().split()[3])
            print(f"{name}: L={L:5d}  {len(V)} v, {len(E)} exact edges" + (f"   Heule's file: {ref}  -> {'MATCH' if ref==len(E) else 'MISMATCH'}" if ref else ""), flush=True)
        except Exception as e:
            print(f"{name}: FAILED {type(e).__name__}: {e}", flush=True)
