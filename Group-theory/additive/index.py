def solve():
    # Multiplicative group:
    # A = g^a mod p
    # B = g^b mod p
    # S = A^b mod p = B^a mod p = g^(ab) mod p
    
    # Additive group:
    # A = g * a mod p
    # B = g * b mod p
    # S = A * b mod p = B * a mod p = g * a * b mod p
    
    param = {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0xff78b9638492818126dde76ae32827348cc0adce4cc361d95102685eb70c713471da431f5aef249e5b97aa663562d163b03756b00cb9bf0e54e51c59c73d8e81906b534471625d76d73925caf04653a79de8c458a3c1e005c086890d47c04909671f7b2ab15ec59a81e7395253f8d6ad24aba52653fecd0ca9620c7892d8e6cd221632e0b8934adae4799c91848777e1b5e1a6a1e84929b1e0cda830a469f9bdf85efd16c49bac87133f85799cd72ea968798cb11b266ba6ee36c3f71a79dc6c", "B": "0xe921b81c97193fe83e35f55aba668cf616db5330b44add857784b1e60af87cbc65e3993fa2f7be4361c458b74a150788a9e5a8a41f4cfbe642e87ce73f3a32f19d91b34186c3bf98c6ba052c440880dccd42b1e4865df29626b8ee39a813cf75d06a3710ad677a665425af5ce8d5abb69c303c976dcbf6f24851c5d15a404a8e31966b442f59acd5cd95da028dbd793139ebe708ae9fc16f8d41df63f588bf5aa590572c068597b374e31f8141098ae8158a27f59459977d8043f032ccd4c55b"}

    p = int(param["p"], 16)
    g = int(param["g"], 16)
    A = int(param["A"], 16)
    B = int(param["B"], 16)

    a = (A * pow(g, -1, p)) % p
    S = (a * B) % p

    print(S)

if __name__ == "__main__":
    solve()