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

# 1. Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. HALVED LUV: (1106 / 2) = 553 
# 553 in hex is 0229. We'll use this as the "Living" displacement.
halved_salt = "00000229" # Padded to 8 hex chars (4 bytes)

# 3. Displace the very end of Half A
# Keep first 56 chars, swap last 8 for the halved funds
final_hex = half_a_hex[:56] + halved_salt

# 4. Generate Compressed K/L WIF
compressed_payload = '80' + final_hex + '01'

print(f"Halved LUV WIF: {base58_check_encode(compressed_payload)}")