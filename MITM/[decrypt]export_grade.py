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

param = {"iv": "921ab909e073a5a949bfaf03026b74a0", "encrypted": "ec6efd132f62bc02c42bcf677c9c04f6a83222b6efa4a3a37aa71612e5db4840276d30d3db689af53d119e93ad114ce7111c42815bf9962b60b70af62b85059a36d2c785e4498575802c0e64ed2ca7b5"}

shared_secret = 1
iv = param["iv"]
ciphertext = param["encrypted"]

print(decrypt_flag(shared_secret, iv, ciphertext))
