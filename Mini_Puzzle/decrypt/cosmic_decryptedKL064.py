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

# 1. THE DECRYPTED SOURCE
full_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. THE DUALITY SWAP (128-bit Half-Swap)
# Swapping the high 16 bytes with the low 16 bytes
high_half = full_key_hex[:32]
low_half = full_key_hex[32:]
swapped_key_hex = low_half + high_half
swapped_int = int(swapped_key_hex, 16)

# 3. THE ARCHITECT MIRROR
# Bitwise flip of the swapped key
mirrored_int = swapped_int ^ (2**256 - 1)

# 4. THE 1106 AGREEMENT
# Applying the fund offset as a final bitmask
final_int = mirrored_int ^ 1106
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Split Duality WIF: {base58_check_encode(compressed_payload)}")