from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
from sympy.ntheory import discrete_log

# === THAY CÁC GIÁ TRỊ MỚI NHẤT TỪ TERMINAL VÀO ĐÂY ===
p_hex = "0xde26ab651b92a129"
g_hex = "0x2"
A_hex = "0x2d941c9881f7e145"
B_hex = "0x6a4c30e2e630a5d3"
iv_hex = "695dd5be6e08a9768ba61d769f843986"
ciphertext_hex = "b8515597e5b98b3a864e620b2b4643768cfcaf92b38871b8337185faae1b6b4f"
# ===================================================

p = int(p_hex, 16)
g = int(g_hex, 16)
A = int(A_hex, 16)
B = int(B_hex, 16)

print("[+] Đang giải DLP (có thể mất 1-2 phút)...")
# Tìm số mũ bí mật b từ B (g^b = B mod p)
b = discrete_log(p, B, g)
shared_secret = pow(A, b, p)
print(f"[+] Shared Secret tìm thấy: {shared_secret}")

def decrypt(ss, iv_h, ct_h):
    # Thử các kiểu định dạng shared_secret khác nhau
    formats = [
        str(ss).encode(),           # Dạng số thập phân (thường dùng nhất)
        hex(ss).encode(),           # Dạng 0x...
        hex(ss)[2:].encode(),       # Dạng không có 0x
    ]
    
    for data in formats:
        key = hashlib.sha1(data).digest()[:16]
        cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_h))
        plaintext = cipher.decrypt(bytes.fromhex(ct_h))
        
        # Kiểm tra xem kết quả có chứa chữ 'crypto' không
        if b"crypto{" in plaintext:
            try:
                return unpad(plaintext, 16).decode()
            except:
                return plaintext.decode(errors='ignore') # Nếu unpad lỗi nhưng thấy flag
    return None

flag = decrypt(shared_secret, iv_hex, ciphertext_hex)
if flag:
    print(f"--- FLAG CỦA BẠN: {flag} ---")
else:
    print("[-] Vẫn chưa tìm được. Hãy chắc chắn p, g, A, B, IV, CT thuộc cùng một phiên kết nối!")