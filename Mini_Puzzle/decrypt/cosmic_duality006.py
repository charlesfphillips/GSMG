import hashlib
import binascii
from Crypto.Cipher import AES

def base58_check_encode(hex_payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    raw_bin = binascii.unhexlify(hex_payload)
    digest1 = hashlib.sha256(raw_bin).digest()
    digest2 = hashlib.sha256(digest1).digest()
    final_bin = raw_bin + digest2[:4]
    num = int(final_bin.hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# 1. THE ARCHITECT'S KEY (From OP_RETURN)
password = b"844e86a69a04eea672049e0e0e8612"
key = hashlib.sha256(password).digest()

# 2. THE DATA (Your original decrypted key)
data_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
encrypted_bytes = binascii.unhexlify(data_hex)

# 3. THE FINAL DECRYPTION (Electronic Codebook Mode - No IV required)
cipher = AES.new(key, AES.MODE_ECB)
decrypted = cipher.decrypt(encrypted_bytes)
final_hex = decrypted.hex()

print(f"Final Treasury Scalar: {final_hex}")
print("-" * 30)
# Testing uncompressed as 19Av3 showed the 1106 fund signpost
print(f"Uncompressed WIF: {base58_check_encode('80' + final_hex)}")
print(f"Compressed WIF: {base58_check_encode('80' + final_hex + '01')}")