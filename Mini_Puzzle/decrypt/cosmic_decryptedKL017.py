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

# 1. Beginning: Your first 16 bytes
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1b"
raw_a = binascii.unhexlify(half_a_hex)

# 2. End: The LUV 1106 TXID first 16 bytes
txid_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"
raw_tx = binascii.unhexlify(txid_hex)

# 3. DUALITY: XOR the two halves together to create the "Better Half"
xor_half = bytes([a ^ b for a, b in zip(raw_a, raw_tx)])

# 4. NEED FUNDS TO LIVE: Pad the result with the 1106 Satoshis (0452)
# We use the 1106 as the final 16-byte "Life" tail
tail = binascii.unhexlify("00000000000000000000000000000452")
final_key = xor_half + tail

# 5. Generate Compressed WIF
compressed_payload = '80' + final_key.hex() + '01'
print(f"XOR Hybrid WIF: {base58_check_encode(compressed_payload)}")