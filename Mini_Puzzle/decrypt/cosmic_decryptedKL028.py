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

# 1. THE JOIN (1jon)
raw_a_hex = "8badeb454dbeb5d2263d8774b8b24f1b"
raw_tx_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"
joined_int = int(raw_a_hex + raw_tx_hex, 16)

# 2. THE FUNDING (Pre-processing)
# Apply the 1106 Satoshis to the base identity
funded_int = (joined_int + 1106) % N

# 3. THE DUALITY SPLIT MIRROR
# Split the funded scalar and mirror only the first half
funded_hex = hex(funded_int)[2:].zfill(64)
part1 = int(funded_hex[:32], 16) ^ (2**128 - 1)
part2 = int(funded_hex[32:], 16)
mirrored_joined = int(hex(part1)[2:].zfill(32) + hex(part2)[2:].zfill(32), 16)

# 4. THE FINAL SHIFT
# Apply the logical shift to the mirrored/funded result
final_int = mirrored_joined >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Pre-Funded Split WIF: {base58_check_encode(compressed_payload)}")