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
inv2 = pow(2, -1, N)

# 1. Split the Duality
# Beginning: First 16 bytes of fragment
# End: First 16 bytes of 1106 TXID
raw_a = int("8badeb454dbeb5d2263d8774b8b24f1b", 16)
raw_tx = int("a798905f53fdcadcbd2e2a1e61d23ba6", 16)

# 2. Independent Halving
# Halve both components modularly before joining
halved_a = (raw_a * inv2) % (2**128)
halved_tx = (raw_tx * inv2) % (2**128)

# 3. The Final Join (1jon)
# Combine the two halved 128-bit values into one 256-bit key
final_hex = hex(halved_a)[2:].zfill(32) + hex(halved_tx)[2:].zfill(32)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Revelator Split WIF: {base58_check_encode(compressed_payload)}")