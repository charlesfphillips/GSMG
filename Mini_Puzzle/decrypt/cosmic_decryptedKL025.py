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

# 1. THE JOIN (Fragment + TXID)
raw_a_hex = "8badeb454dbeb5d2263d8774b8b24f1b"
raw_tx_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"
joined_int = int(raw_a_hex + raw_tx_hex, 16)

# 2. THE MIRROR (Alignment confirmed by 1Acjc)
mirrored_int = joined_int ^ (2**256 - 1)

# 3. THE LOGICAL SHIFT (Halving confirmed by 1G/1Acjc)
shifted_int = mirrored_int >> 1

# 4. LITTLE-ENDIAN FUNDING (The Correction)
# 1106 (0x0452) in 8-byte Little-Endian is 5204000000000000
le_funds = int.from_bytes(binascii.unhexlify("5204000000000000"), byteorder='big')
final_int = (shifted_int + le_funds) % N
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Corrected LE-Funded WIF: {base58_check_encode(compressed_payload)}")