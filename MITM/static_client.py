from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

def solve():
    # A = g^a mod p
    # B = g^b mod p
    # S = A^b mod p = B^a mod p = g^(ab) mod p

    # para = {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0xcc552aeafb984c4b7ae7d436b27641100331dd414b591b1917eb6ba44434460421557aa330d5263d8992d68fc5ca5d95495e57b1f43913c5a0bcde17ec94001588eddec1fd518285a835715462879457b2fc3bd888c0a40ef2bd8bb3b12adf7cd406ae756901ca848c053cae3c27e567bf36ff5d33b52a9397e87b85ac6ac3fdf13bc7cda4848315144c35f8477aa52e4d7cc5d003c59af6501ee8da2d60b4682242ff18c31b6f6a1cd476f037ed4ca3a11238b12da31efb3856029aaf3df189", "A": "0x1"}

    # p = int(para["p"], 16)
    # g = int(para["g"], 16)
    # A = int(para["A"], 16)

    # param_Bob = {"iv": "cbc8e6fca4b3541c2411bfc6cfd8e835", "encrypted": "0600c7c3a697ec78606e2ccf6985f0b8632564e36986a622693480d47dbf787b266d6ecef5bf3351e50988717632f9b7e5ba09630bd97961ae69298df8b5ae9d299022f493f060da11af2ea10e3388bd"}

    # shared_secret = 1
    # iv = param_Bob["iv"]
    # ciphertext = param_Bob["encrypted"]

    # print(decrypt_flag(shared_secret, iv, ciphertext))
    # # -> Hey, what's up. I got bored generating random numbers did you see?

    S = 0x6fae4067aa94db99517ad1990ba9fecf58388cdbb7bbb0c2a6454202b6959b16652f563e4bc7daae7fe0a1d47398a4de73e1ed09260de86f8b7416569d1c49dabd2be6c778c7d8b6c606cb4ea582e197269fb53429b35fad7e3b6a70c5c424980e18e8c92d4b8efe3435f69e55cac552771ab8d05a5f07709eda9b61fc313cc3d2b738726e620c74b5da76698d562fcb66630cebe8f47e4865ea5ff09a7aedf2a6aa9c2e74b4b8d4ad60ec90a43bfc9bd13647af527085262369922172b87001

    param_Alice = {"iv": "d3d765a3ef663b20f4f48cb4dc2886c3", "encrypted": "855e94bc29d68dcf548911053bdfd1cc22ba1b1d719d8e90748fdee57c431421"}

    iv = param_Alice["iv"]
    ciphertext = param_Alice["encrypted"]

    print(decrypt_flag(S, iv, ciphertext))

if __name__ == "__main__":
    solve()