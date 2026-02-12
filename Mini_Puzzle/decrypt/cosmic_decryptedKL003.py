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

# 2. LUV 1106: The "Funds" as a 32-bit Little Endian salt
# 1106 in hex is 0452 -> LE is 52040000
luv_salt = "52040000"

# 3. Displace the end of Half A with the Funds
# We keep the first 56 chars and swap the last 8 for the salt
final_hex = half_a_hex[:56] + luv_salt

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'

print(f"LUV Displaced WIF: {base58_check_encode(compressed_payload)}")