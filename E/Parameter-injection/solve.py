from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
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


# MITM attack used:
# Send to Bob:   A = 0x1
# Send to Alice: B = 0x1
# => shared secret = 1 for both sides.
shared_secret = 1
iv = "26718389691bd171cea4b369d8d9a974"
ciphertext = "c4d7e9b8bf38b69bcd2cee6a71bd5d84ce9a1eead27244b2ca08419cea28dcbf"

print(decrypt_flag(shared_secret, iv, ciphertext))
