from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sympy.ntheory import discrete_log
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1] :]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]

    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode("ascii")
    return plaintext.decode("ascii")


# MITM downgrade used:
#   Alice -> Bob: {"supported": ["DH64"]}
#   Bob   -> Alice: {"chosen": "DH64"}
p = int("0xde26ab651b92a129", 16)
g = int("0x2", 16)
A = int("0xbabe3d9e44b869e6", 16)
B = int("0x3d62f40e780ecb7d", 16)

iv = "0da9a243151ab654b035350fc9258d56"
ciphertext = "107b05beef7b1d3e58bbde80e2212d8133bd70ac34e148995401fa2c8682393b"

a = discrete_log(p, A % p, g)
shared_secret = pow(B, a, p)

print(f"a = {a}")
print(f"shared_secret = {shared_secret}")
print(decrypt_flag(shared_secret, iv, ciphertext))
