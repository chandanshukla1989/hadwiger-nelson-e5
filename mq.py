"""Exact arithmetic in the multiquadratic field Q(sqrt3, sqrt5, sqrt11).
Basis indexed by 3-bit masks over primes (3,5,11): bit0=3, bit1=5, bit2=11."""
from fractions import Fraction as F
import re, sympy as sp
from functools import lru_cache

PRIMES = (3, 5, 11)
N = 8

def prod_mask(m):
    p = 1
    for b in range(3):
        if m >> b & 1: p *= PRIMES[b]
    return p

BASIS_SYM = {m: sp.sqrt(prod_mask(m)) for m in range(N)}
SYM_TO_MASK = {sp.sqrt(prod_mask(m)): m for m in range(N)}
SYM_TO_MASK[sp.Integer(1)] = 0
MULT = [[prod_mask(i & j) for j in range(N)] for i in range(N)]
XOR  = [[i ^ j for j in range(N)] for i in range(N)]

ZERO = (F(0),)*N
def one():
    v = [F(0)]*N; v[0] = F(1); return tuple(v)
ONE = one()

def mul(a, b):
    out = [F(0)]*N
    for i in range(N):
        ai = a[i]
        if not ai: continue
        Mi, Xi = MULT[i], XOR[i]
        for j in range(N):
            bj = b[j]
            if not bj: continue
            out[Xi[j]] += ai * bj * Mi[j]
    return tuple(out)

def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def add(a, b): return tuple(x + y for x, y in zip(a, b))

def to_vec(expr):
    e = sp.expand(sp.radsimp(sp.sqrtdenest(sp.expand(expr))))
    d = sp.expand(e).as_coefficients_dict()
    out = [F(0)] * N
    for k, v in d.items():
        k = sp.sympify(k); v = sp.Rational(v)
        if k not in SYM_TO_MASK:
            raise ValueError(f"basis element {k} outside Q(sqrt3,sqrt5,sqrt11)  [{expr}]")
        out[SYM_TO_MASK[k]] += F(v.p, v.q)
    return tuple(out)

def to_sym(v):
    return sum(sp.Rational(c.numerator, c.denominator) * BASIS_SYM[m]
               for m, c in enumerate(v) if c)

def parse_vtx(path):
    txt = open(path).read()
    pts, depth, buf = [], 0, ""
    # brace-aware split (coordinates contain nested Sqrt[...] but braces only at top level)
    for m in re.finditer(r"\{(.*)\}", txt):
        body = m.group(1)
        body = re.sub(r"Sqrt\[", "SQ(", body)
        # convert matching ] of SQ( to )
        out, stack = [], []
        for ch in body:
            if ch == "(": stack.append("("); out.append(ch)
            elif ch == "[": stack.append("["); out.append("(")
            elif ch == "]":
                stack.pop(); out.append(")")
            elif ch == ")":
                stack.pop(); out.append(ch)
            else: out.append(ch)
        body = "".join(out).replace("SQ(", "sqrt(")
        # top-level comma split
        d, cur, parts = 0, "", []
        for ch in body:
            if ch == "(": d += 1
            elif ch == ")": d -= 1
            if ch == "," and d == 0:
                parts.append(cur); cur = ""
            else: cur += ch
        parts.append(cur)
        assert len(parts) == 2, parts
        x, y = (sp.sympify(p.strip()) for p in parts)
        pts.append((to_vec(x), to_vec(y)))
    return pts
