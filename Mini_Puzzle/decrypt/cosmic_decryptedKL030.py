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

# 1. THE JOIN (Confirmed Duality)
raw_a_hex = "8badeb454dbeb5d2263d8774b8b24f1b"
raw_tx_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"
joined_int = int(raw_a_hex + raw_tx_hex, 16)

# 2. MODULAR INVERSE FUNDING
# Subtracting 1106 to reverse the funding offset
funded_int = (joined_int - 1106) % N

# 3. THE FULL MIRROR (1Acjc / 1Azt alignment)
mirrored_int = funded_int ^ (2**256 - 1)

# 4. THE FINAL SHIFT (1G-Range Halving)
final_int = mirrored_int >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Mirrored Inverse WIF: {base58_check_encode(compressed_payload)}")