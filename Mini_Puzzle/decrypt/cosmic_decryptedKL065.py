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

# 1. THE DECRYPTED PASSWORD
# This is the 32-byte output you decrypted successfully
decrypted_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
raw_bytes = binascii.unhexlify(decrypted_key_hex)

# 2. THE FINAL HASH (The 'Agreement' realization)
# Hashing the decrypted result to generate the true 256-bit scalar
final_seed = hashlib.sha256(raw_bytes).hexdigest()
final_seed_int = int(final_seed, 16)

# 3. THE ARCHITECT MIRROR
# Bitwise flip to align with the 1G vanity target
mirrored_int = final_seed_int ^ (2**256 - 1)

# 4. THE 1106 FUNDING
# Adding the final offset
final_int = (mirrored_int + 1106)
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Hashed Architect WIF: {base58_check_encode(compressed_payload)}")