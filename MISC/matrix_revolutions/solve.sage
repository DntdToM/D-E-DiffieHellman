import hashlib
import json
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

F = GF(2)
R.<x> = PolynomialRing(F)
N = 150

f61 = x^61 + x^57 + x^55 + x^53 + x^51 + x^50 + x^47 + x^46 + x^45 + x^44 + x^43 + x^40 + x^34 + x^32 + x^31 + x^30 + x^28 + x^23 + x^21 + x^19 + x^13 + x^12 + x^11 + x^7 + x^4 + x^3 + x^2 + x + 1
f89 = x^89 + x^84 + x^82 + x^80 + x^77 + x^76 + x^75 + x^74 + x^68 + x^67 + x^66 + x^64 + x^63 + x^62 + x^57 + x^53 + x^52 + x^51 + x^50 + x^43 + x^40 + x^39 + x^38 + x^36 + x^34 + x^33 + x^32 + x^31 + x^27 + x^24 + x^18 + x^17 + x^16 + x^14 + x^13 + x^12 + x^10 + x^9 + x^8 + x^7 + x^4 + x^3 + 1
m = f61 * f89


def load_matrix(path):
    rows = [[int(c) for c in line.strip()] for line in Path(path).read_text().splitlines() if line.strip()]
    return matrix(F, rows)


def poly_from_vector(v):
    return sum(int(v[i]) * x^i for i in range(len(v)))


def eval_poly_on_matrix(poly, mat):
    out = zero_matrix(F, mat.nrows(), mat.ncols())
    for c in reversed(poly.list()):
        out = out * mat
        if c:
            out += identity_matrix(F, mat.nrows())
    return out


def field_elem(K, poly):
    poly = poly % K.modulus()
    return sum(int(c) * K.gen()^i for i, c in enumerate(poly.list()))


def lift_elem(elem):
    return sum(int(c) * x^i for i, c in enumerate(elem.polynomial().list()))


G = load_matrix("generator.txt")
A = load_matrix("alice.pub")
B = load_matrix("bob.pub")
enc = json.loads(Path("flag.enc").read_text())

e0 = vector(F, [1] + [0] * (N - 1))
basis = []
cur = e0
for _ in range(N):
    basis.append(cur)
    cur = G * cur

K = matrix(F, N, N)
for j, v in enumerate(basis):
    K.set_column(j, v)

qa = poly_from_vector(K.solve_right(A.column(0))) % m
qb = poly_from_vector(K.solve_right(B.column(0))) % m

K61.<a61> = GF(2^61, modulus=f61)
K89.<a89> = GF(2^89, modulus=f89)

ga = K61.gen()
gb = K89.gen()

qa61 = field_elem(K61, qa)
qb61 = field_elem(K61, qb)
qa89 = field_elem(K89, qa)
qb89 = field_elem(K89, qb)

ord61 = 2^61 - 1
ord89 = 2^89 - 1

apriv61 = qa61.log(ga)
bpriv61 = qb61.log(ga)
apriv89 = qa89.log(gb)
bpriv89 = qb89.log(gb)

shared61 = ga^((apriv61 * bpriv61) % ord61)
shared89 = gb^((apriv89 * bpriv89) % ord89)

r61 = lift_elem(shared61)
r89 = lift_elem(shared89)
shared_poly = (r61 * f89 * inverse_mod(f89, f61) + r89 * f61 * inverse_mod(f61, f89)) % m
shared = eval_poly_on_matrix(shared_poly, G)

mat_str = "".join(str(int(x)) for row in shared.rows() for x in row)
key = hashlib.sha256(mat_str.encode()).digest()

decryptor = Cipher(algorithms.AES(key), modes.CBC(bytes.fromhex(enc["iv"]))).decryptor()
pt = decryptor.update(bytes.fromhex(enc["ciphertext"])) + decryptor.finalize()
print(pt[:-pt[-1]].decode())
