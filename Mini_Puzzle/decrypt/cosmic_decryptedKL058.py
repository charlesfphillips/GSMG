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
decrypted_int = int(decrypted_key_hex, 16)

# 2. THE ROTATION (The Handshake)
# Circular Left Shift (ROL) by 1 bit
rotated_int = ((decrypted_int << 1) | (decrypted_int >> 255)) & (2**256 - 1)

# 3. THE MODULAR FUNDING (The Agreement)
# Apply the 1106 offset within the field of the curve
funded_int = (rotated_int + 1106) % N

# 4. THE ARCHITECT MIRROR
# Final bitwise flip to reach the 1G vanity target
final_int = funded_int ^ (2**256 - 1)
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
# (Prefix 80 + 32-byte key + 01 for compressed)
compressed_payload = '80' + final_hex + '01'
print(f"Final Handshake WIF: {base58_check_encode(compressed_payload)}")