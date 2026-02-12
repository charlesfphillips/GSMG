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
# Your 32-byte key from the AES-256-CBC decryption
decrypted_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
decrypted_int = int(decrypted_key_hex, 16)

# 2. THE ARCHITECT MIRROR (Confirmed Signal)
# Flip the bits of the entire 256-bit scalar
mirrored_int = decrypted_int ^ (2**256 - 1)

# 3. THE LOGICAL SHIFT (Halving / 1G Target)
# Applying the shift that produced 1Acjc and 1GQ4
final_int = mirrored_int >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Final Architect WIF: {base58_check_encode(compressed_payload)}")