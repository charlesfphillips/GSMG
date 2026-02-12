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

# THE COMPONENTS
k1_int = int("8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af", 16)
k2_int = int("a986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2", 16)

# THE SYMMETRY (The Average / Midpoint)
# In a modular field, (a + b) / 2 is (a + b) * modular_inverse(2)
inv_2 = pow(2, -1, N)
midpoint_int = ((k1_int + k2_int) * inv_2) % N

# Apply the 12-bit shift (♀) to the MIDPOINT
final_int = ((midpoint_int >> 12) | (midpoint_int << (256 - 12))) & (2**256 - 1)
final_hex = hex(final_int)[2:].zfill(64)

print(f"Symmetric Treasury Scalar: {final_hex}")
print("-" * 30)
print(f"Uncompressed WIF: {base58_check_encode('80' + final_hex)}")
print(f"Compressed WIF:   {base58_check_encode('80' + final_hex + '01')}")