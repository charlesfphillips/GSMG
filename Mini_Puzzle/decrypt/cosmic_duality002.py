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

# THE 1.25 BTC CANDIDATE SCALAR
scalar_hex = "9e8f98df796506eb629d9511aa942c25dc0388e80a4df289895728da63acc66c"
val = int(scalar_hex, 16)

# THE "ANSWER IS WOMEN" (12) ROTATION
# Circular Right Shift (ROR) by 12 bits
rotated_int = ((val >> 12) | (val << (256 - 12))) & (2**256 - 1)
rotated_hex = hex(rotated_int)[2:].zfill(64)

print(f"Rotated Scalar: {rotated_hex}")
print("-" * 30)
print(f"Compressed WIF: {base58_check_encode('80' + rotated_hex + '01')}")
print(f"Uncompressed WIF: {base58_check_encode('80' + rotated_hex)}")