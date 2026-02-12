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

# 2. CLEAR THE DEBT (Modular Subtraction)
# Subtracting 1106 before the transformation
cleared_int = (decrypted_int - 1106) % N

# 3. THE ROTATION
# Circular Left Shift (ROL) by 1 bit
rotated_int = ((cleared_int << 1) | (cleared_int >> 255)) & (2**256 - 1)

# 4. THE ARCHITECT MIRROR
final_int = rotated_int ^ (2**256 - 1)
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Debt Clearance WIF: {base58_check_encode(compressed_payload)}")