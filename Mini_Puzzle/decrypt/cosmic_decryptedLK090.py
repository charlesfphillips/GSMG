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

# FIELD ORDER
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 1. THE DECRYPTED SOURCE
dec_int = int("8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af", 16)

# 2. THE MULTIPLIER MASK
mask_int = int("844e86a69a04eea672049e0e0e8612", 16)

# 3. THE INVERSE TRANSFORMATION (The "Neo" move)
# pow(a, -1, n) calculates the modular multiplicative inverse
try:
    inv_mask = pow(mask_int, -1, N)
    # Apply inverse and the ♀ (12) shift
    final_int = (dec_int * inv_mask) % N
    final_int = (final_int ^ 12) # XOR with the symbol itself
    final_hex = hex(final_int)[2:].zfill(64)

    print(f"Inverse Reward Scalar: {final_hex}")
    print("-" * 30)
    print(f"Compressed WIF: {base58_check_encode('80' + final_hex + '01')}")
    print(f"Uncompressed WIF: {base58_check_encode('80' + final_hex)}")
except ValueError:
    print("Inverse does not exist for this mask.")