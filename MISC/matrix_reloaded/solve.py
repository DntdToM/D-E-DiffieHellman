#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

P = 13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471


def load_matrix(path):
    return [[int(x) % P for x in line.split()] for line in Path(path).read_text().splitlines() if line.strip()]


def matvec(M, v):
    return [sum((a * b) % P for a, b in zip(row, v)) % P for row in M]


def solve(A, b):
    A = [row[:] for row in A]
    b = b[:]
    n = len(A)
    row = 0
    for col in range(n):
        piv = next((r for r in range(row, n) if A[r][col]), None)
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        b[row], b[piv] = b[piv], b[row]
        inv = pow(A[row][col], -1, P)
        A[row] = [(x * inv) % P for x in A[row]]
        b[row] = (b[row] * inv) % P
        for r in range(n):
            if r != row and A[r][col]:
                k = A[r][col]
                A[r] = [(x - k * y) % P for x, y in zip(A[r], A[row])]
                b[r] = (b[r] - k * b[row]) % P
        row += 1
    return b


def trim(f):
    while f and f[-1] == 0:
        f.pop()
    return f or [0]


def divmod_poly(a, b):
    a = a[:]
    q = [0] * max(0, len(a) - len(b) + 1)
    inv = pow(b[-1], -1, P)
    while len(a) >= len(b) and a != [0]:
        k = a[-1] * inv % P
        i = len(a) - len(b)
        q[i] = k
        for j, x in enumerate(b):
            a[i + j] = (a[i + j] - k * x) % P
        trim(a)
    return trim(q), trim(a)


def gcd_poly(a, b):
    a, b = trim(a[:]), trim(b[:])
    while b != [0]:
        _, r = divmod_poly(a, b)
        a, b = b, r
    inv = pow(a[-1], -1, P)
    return [(x * inv) % P for x in a]


def eval_poly(f, x):
    y = 0
    for c in reversed(f):
        y = (y * x + c) % P
    return y


G = load_matrix("generator.txt")
out = json.loads(Path("output.txt").read_text())
enc = json.loads(Path("flag.enc").read_text())
v, w = out["v"], out["w"]
N = len(G)

basis = []
cur = v
for _ in range(N):
    basis.append(cur)
    cur = matvec(G, cur)

K = [list(row) for row in zip(*basis)]
rel = solve(K, cur)
q = solve(K, w)

m = [(-x) % P for x in rel] + [1]
dm = [(i * m[i]) % P for i in range(1, len(m))]
g = gcd_poly(m, dm)
lam = (-g[0] * pow(g[1], -1, P)) % P

secret = eval_poly([(i * q[i]) % P for i in range(1, len(q))], lam)
secret = secret * lam * pow(eval_poly(q, lam), -1, P) % P

key = hashlib.sha256(str(secret).encode()).digest()
decryptor = Cipher(algorithms.AES(key), modes.CBC(bytes.fromhex(enc["iv"]))).decryptor()
pt = decryptor.update(bytes.fromhex(enc["ciphertext"])) + decryptor.finalize()
print(pt[:-pt[-1]].decode())
