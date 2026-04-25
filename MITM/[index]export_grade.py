from sympy.ntheory import discrete_log

def solve():

    param = {"p": "0xde26ab651b92a129", "g": "0x2", "A": "0x919fdc86161171eb", "B": "0x633ddd7f4d81e1f7"}

    # A = g^a mod p
    # B = g^b mod p
    # S = A^b mod p = B^a mod p = g^(ab) mod p

    A = int(param["A"], 16)
    B = int(param["B"], 16)
    p = int(param["p"], 16)
    g = int(param["g"], 16)

    a = discrete_log(p, A % p, g)
    # b = discrete_log(p, B % p, g)

    print(a)
    # print(b)

    S = pow(B, a , p)
    # S = pow(A, b , p)
    # S = pow(g, a * b, p)

    print(S)

if __name__ == "__main__":
    solve()