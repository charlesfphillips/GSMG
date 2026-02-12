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

# 1. THE AGREEMENT (XOR Duality)
# XOR the 16-byte fragment and 16-byte TXID
frag_bytes = binascii.unhexlify("8badeb454dbeb5d2263d8774b8b24f1b")
txid_bytes = binascii.unhexlify("a798905f53fdcadcbd2e2a1e61d23ba6")
xor_bytes = bytes([a ^ b for a, b in zip(frag_bytes, txid_bytes)])

# 2. THE EXPANSION
# Form the 32-byte (256-bit) key by using the XORed result + the 1106 Satoshis
# (This follows the 1jon 'Join' structure seen in your logs)
joined_hex = xor_bytes.hex() + "00000000000000000000000000000452"
joined_int = int(joined_hex, 16)

# 3. THE ARCHITECT MIRROR & SHIFT
# Flip the bits and apply the logical halving (>> 1)
mirrored_int = joined_int ^ (2**256 - 1)
final_int = mirrored_int >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Duality Agreement WIF: {base58_check_encode(compressed_payload)}")