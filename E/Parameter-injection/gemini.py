from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# LƯU Ý: Phải lấy IV và Ciphertext MỚI từ session bạn đã gửi 0x01
iv_hex = "6265a63eda023fee5805fd55530e5ba9" 
ciphertext_hex = "94607144d168309bfef7f9d745e89fad4d98e6cac9b2e81ad8925d7d4a148fbb"

# Shared secret bây giờ chắc chắn là 1
shared_secret = 1

# Tạo khóa AES từ shared_secret = 1
sha1 = hashlib.sha1()
sha1.update(str(shared_secret).encode('ascii'))
key = sha1.digest()[:16]

# Giải mã
iv = bytes.fromhex(iv_hex)
ciphertext = bytes.fromhex(ciphertext_hex)
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext)

try:
    # Sử dụng lại logic kiểm tra padding từ bài cũ cho chắc chắn
    padding_len = plaintext[-1]
    if padding_len < 16:
        print("Flag:", unpad(plaintext, 16).decode())
    else:
        print("Plaintext (không padding):", plaintext.decode())
except Exception as e:
    print("Lỗi giải mã:", e)
    print("Dữ liệu thô (có thể sai khóa):", plaintext)