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

# 1. THE JOIN (From your 1jon breadcrumb)
# Beginning: First 16 bytes of fragment
# End: First 16 bytes of 1106 TXID
raw_a_hex = "8badeb454dbeb5d2263d8774b8b24f1b"
raw_tx_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"
joined_hex = raw_a_hex + raw_tx_hex
joined_int = int(joined_hex, 16)

# 2. NEED FUNDS TO LIVE (Add 1106 to the joined scalar)
funded_int = (joined_int + 1106) % N

# 3. THE HALVING (Modularly halve the funded result)
final_int = (funded_int * inv2) % N
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Funded Join WIF: {base58_check_encode(compressed_payload)}")