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

# SECP256K1 Order (The Matrix Boundaries)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 1. Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
int_a = int(half_a_hex, 16)

# 2. THE HALVING: Modular Inverse Division
# Dividing by 2 in ECC is multiplying by (N+1)/2
halved_int = (int_a * pow(2, -1, N)) % N

# 3. NEED FUNDS TO LIVE: Apply the 1106 LUV offset
# We test both XOR and Addition for the final "Life" spark
final_int = (halved_int + 1106) % N
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed K/L WIF
compressed_payload = '80' + final_hex + '01'

print(f"Halved Scalar WIF: {base58_check_encode(compressed_payload)}")