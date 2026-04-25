from Crypto.Util.number import long_to_bytes

def load_matrix(fname):
    with open(fname, 'r') as f:
        data = f.read().strip()
    rows = [list(map(int, row)) for row in data.splitlines()]
    return Matrix(GF(2), rows)

C = load_matrix('flag.enc')
E = 31337
N = 50

M = C^(1/E)

msg_bits = [0] * (N * N)
for i in range(N):
    for j in range(N):
        msg_bits[i + j*N] = int(M[i, j])

bin_str = "".join(map(str, msg_bits))
flag_int = int(bin_str, 2)
flag_bytes = []
for i in range(0, len(bin_str), 8):
    byte = bin_str[i:i+8]
    if len(byte) == 8:
        flag_bytes.append(int(byte, 2))

print("-" * 30)
print(f"FLAG: {bytes(flag_bytes)}")
print("-" * 30)