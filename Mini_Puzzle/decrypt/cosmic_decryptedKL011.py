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
inv2 = pow(2, -1, N)

# 1. Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
int_a = int(half_a_hex, 16)

# 2. HALVING DUALITY: Split the 1106 funds (553 + 553)
# Apply first half, then modular halving, then second half
first_half_funds = 553
second_half_funds = 553

final_int = (((int_a + first_half_funds) * inv2) + second_half_funds) % N
final_hex = hex(final_int)[2:].zfill(64)

# 3. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Double-Funded WIF: {base58_check_encode(compressed_payload)}")