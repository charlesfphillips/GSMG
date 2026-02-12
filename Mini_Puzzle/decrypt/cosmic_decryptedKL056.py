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
decrypted_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. THE DUALITY SWAP (Little-Endian Conversion)
# Reverse the bytes (every 2 hex characters)
raw_bytes = binascii.unhexlify(decrypted_key_hex)
swapped_bytes = raw_bytes[::-1]
swapped_int = int(swapped_bytes.hex(), 16)

# 3. THE ARCHITECT MIRROR & SHIFT
# Flip the bits and apply the halving shift
mirrored_int = swapped_int ^ (2**256 - 1)
final_int = (mirrored_int >> 1) ^ 1106
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Endian Architect WIF: {base58_check_encode(compressed_payload)}")