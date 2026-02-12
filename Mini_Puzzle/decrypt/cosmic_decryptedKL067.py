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
decrypted_int = int(decrypted_key_hex, 16)

# 2. THE ARCHITECT MIRROR
# This is the "Duality" of the bits
mirrored_int = decrypted_int ^ (2**256 - 1)

# 3. THE "AGREEMENT" MASK
# Converting 1106 to hex (0x0452) and applying it to both ends of the scalar
# This aligns the "Beginning" and "End" as per the clue
mask = (0x04 << 248) | 0x52
final_int = mirrored_int ^ mask
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Final Duality WIF: {base58_check_encode(compressed_payload)}")