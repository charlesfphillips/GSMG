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

# 2. THE FUNDING
# Adding the 1106 Satoshis as the final scalar adjustment
funded_int = joined_int + 1106

# 3. THE LOGICAL HALVING
# Literal bit-shift to align with the 1Ghe results
final_int = funded_int >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Shifted Join WIF: {base58_check_encode(compressed_payload)}")