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

# THE FIELD ORDER (secp256k1)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 1. THE DECRYPTED SOURCE
# This is the "Beginning" entropy derived from Bella Ciao
decrypted_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
dec_int = int(decrypted_key_hex, 16)

# 2. THE CAUSALITY MULTIPLIER (OP_RETURN)
# 844e86a69a04eea672049e0e0e8612
mask_hex = "844e86a69a04eea672049e0e0e8612"
mask_int = int(mask_hex, 16)

# 3. THE "NO SPOON" FINAL SCALAR
# Shift by 12 (♀) and the 666 Twist
# Applying modular addition to move the key along the curve
final_int = (dec_int + (mask_int * 12) + 666) % N
final_hex = hex(final_int)[2:].zfill(64)

print(f"Final Reward Scalar: {final_hex}")
print("-" * 30)
# Testing Uncompressed as it matches the 19Av3 signpost format
print(f"Uncompressed WIF: {base58_check_encode('80' + final_hex)}")
print(f"Compressed WIF: {base58_check_encode('80' + final_hex + '01')}")