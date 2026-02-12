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

# 1. THE DECRYPTED SOURCE
decrypted_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
dec_int = int(decrypted_key_hex, 16)

# 2. THE MULTIPLIER (Causality Transcended)
# Converting the OP_RETURN hex to an integer
multiplier_hex = "844e86a69a04eea672049e0e0e8612"
multiplier_int = int(multiplier_hex, 16)

# 3. THE TURING TRANSFORMATION
# Multiply and apply the 666 Twist
transformed = (dec_int * multiplier_int) % N
transformed = transformed ^ 666

# 4. THE ♀ (12) ROTATION & HALVING
# Circular Right Shift (ROR) by 12 bits
final_int = ((transformed >> 12) | (transformed << (256 - 12))) & (2**256 - 1)
final_int = (final_int + 553) % N

final_hex = hex(final_int)[2:].zfill(64)
print(f"Treasury Scalar: {final_hex}")
print("-" * 30)
print(f"Compressed WIF: {base58_check_encode('80' + final_hex + '01')}")
print(f"Uncompressed WIF: {base58_check_encode('80' + final_hex)}")