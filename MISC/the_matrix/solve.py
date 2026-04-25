#!/usr/bin/env python3
import re

N = 50
E = 31337


def mul(a, b):
    cols = [sum(((row >> j) & 1) << i for i, row in enumerate(b)) for j in range(N)]
    return [sum((((row & col).bit_count() & 1) << j) for j, col in enumerate(cols)) for row in a]


def mpow(mat, exp):
    out = [1 << i for i in range(N)]
    while exp:
        if exp & 1:
            out = mul(out, mat)
        mat = mul(mat, mat)
        exp >>= 1
    return out


c = [sum((x == "1") << i for i, x in enumerate(line.strip())) for line in open("flag.enc") if line.strip()]
order = 1
for i in range(N):
    order *= (1 << N) - (1 << i)

m = mpow(c, pow(E, -1, order))
bits = "".join(str((m[i] >> j) & 1) for j in range(N) for i in range(N))
data = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) - 7, 8))
print(re.search(rb"crypto\{[^}]+\}", data).group().decode())
