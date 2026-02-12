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

# THE HEX SCALAR PROVIDED
scalar_hex = "9e8f98df796506eb629d9511aa942c25dc0388e80a4df289895728da63acc66c"

# 1. Generate Compressed WIF (starts with K or L)
compressed_payload = '80' + scalar_hex + '01'
print(f"Compressed WIF: {base58_check_encode(compressed_payload)}")

# 2. Generate Uncompressed WIF (starts with 5)
uncompressed_payload = '80' + scalar_hex
print(f"Uncompressed WIF: {base58_check_encode(uncompressed_payload)}")