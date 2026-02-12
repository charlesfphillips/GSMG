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

# 1. THE DECRYPTED SOURCE (The "Beginning")
decrypted_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. THE OP_RETURN MASK (The "End")
# Using the hex string from the transaction file
op_return_hex = "844e86a69a04eea672049e0e0e8612"

# 3. TRANSCENDING CAUSALITY (The XOR Handshake)
# We XOR the OP_RETURN into the START of the decrypted key
# This "bends" the reality of the key without a "spoon" (complex math)
decrypted_int = int(decrypted_key_hex, 16)
mask_int = int(op_return_hex.ljust(64, '0'), 16) # Pad to 32 bytes

final_int = (decrypted_int ^ mask_int)

# 4. THE 1106 FUNDING (The only thing that remains)
final_int = (final_int + 1106) % N
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"No Spoon WIF: {base58_check_encode(compressed_payload)}")