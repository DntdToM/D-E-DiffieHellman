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

param = {"iv": "a4731fd03b3ff072034777768642e479", "encrypted": "39c657f87c5b6e6c78e51507b741a42019984754a23be030992259376204b662c9bcdaec5539db48b6127e80826a4d78"}

shared_secret = 1866315139746740405042453607733878885892569894534085639502013842619714726684470750686617808973865310522974139793153700908263364626103391085173842251176961780884680493723991285298734584179109120096713644317026067967781871957925871657317680186906699952150347952596683372131955188057471074065941784793959412897567099521426092838240329655660083395988104873451180253684765293238565357701754278486145577342897209909441262644611039861294369174922127791404892914024301177
iv = param["iv"]
ciphertext = param["encrypted"]

print(decrypt_flag(shared_secret, iv, ciphertext))
