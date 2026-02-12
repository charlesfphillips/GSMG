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

# 2. THE DUALITY SWAP (Little-Endian)
# Reverse the bytes to change the orientation
raw_bytes = binascii.unhexlify(decrypted_key_hex)
swapped_bytes = raw_bytes[::-1]
swapped_int = int(swapped_bytes.hex(), 16)

# 3. THE ROTATION
# Circular Left Shift (ROL) by 1 bit
rotated_int = ((swapped_int << 1) | (swapped_int >> 255)) & (2**256 - 1)

# 4. THE FUNDED XOR (The Agreement)
# Using 1106 (0x452) as a bitmask
funded_int = rotated_int ^ 1106

# 5. THE ARCHITECT MIRROR
final_int = funded_int ^ (2**256 - 1)
final_hex = hex(final_int)[2:].zfill(64)

# 6. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Little-Endian Agreement WIF: {base58_check_encode(compressed_payload)}")