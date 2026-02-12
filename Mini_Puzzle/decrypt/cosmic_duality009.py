import hashlib
import binascii

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

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 1. THE DECRYPTED SOURCE (256 bits)
decrypted_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
dec_int = int(decrypted_key_hex, 16)

# 2. THE CAUSALITY DEBT (OP_RETURN as an integer)
# 844e86a69a04eea672049e0e0e8612
mask_hex = "844e86a69a04eea672049e0e0e8612"
mask_int = int(mask_hex, 16)

# 3. THE SUBTRACTION (Debt of the Matrix)
# We subtract the mask and apply the 666 Twist (The Devil is in the details)
treasury_int = (dec_int - mask_int) ^ 666

# 4. THE ♀ (12) ROTATION
# Circular Right Shift (ROR) by 12 bits
final_int = ((treasury_int >> 12) | (treasury_int << (244))) & (2**256 - 1)
final_hex = hex(final_int % N)[2:].zfill(64)

print(f"Final Debt Scalar: {final_hex}")
print("-" * 30)
print(f"Compressed WIF: {base58_check_encode('80' + final_hex + '01')}")
print(f"Uncompressed WIF: {base58_check_encode('80' + final_hex)}")