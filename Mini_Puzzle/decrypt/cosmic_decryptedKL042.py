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

# THE DECRYPTED COSMIC KEY
final_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 1. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Compressed WIF: {base58_check_encode(compressed_payload)}")

# 2. Generate Uncompressed WIF
uncompressed_payload = '80' + final_hex
print(f"Uncompressed WIF: {base58_check_encode(uncompressed_payload)}")