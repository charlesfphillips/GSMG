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

# 1. THE JOIN
raw_a_hex = "8badeb454dbeb5d2263d8774b8b24f1b"
raw_tx_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"
joined_int = int(raw_a_hex + raw_tx_hex, 16)

# 2. THE MIRROR (Duality / 1Azt / 1AT9 signals)
mirrored_int = joined_int ^ (2**256 - 1)

# 3. THE HALVING (The logical shift required for 1G prefixes)
# We apply the shift to the mirrored/funded result
final_int = (mirrored_int ^ 1106) >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Final Mirrored Halved WIF: {base58_check_encode(compressed_payload)}")