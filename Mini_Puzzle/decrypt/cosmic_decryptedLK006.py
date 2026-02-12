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

# 1. Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
raw_a = binascii.unhexlify(half_a_hex)

# 2. Plaintext "Last Command"
# We'll use the exact string length of 32 bytes from the start of the command
cmd_plaintext = "openssl enc -aes-256-cbc -d -a " 
raw_b = cmd_plaintext.encode('ascii')

# 3. XOR Duality (Plaintext)
merged_bytes = bytes([a ^ b for a, b in zip(raw_a, raw_b)])

# 4. Apply "LUV 1106" (The Funds to Live)
# We treat the XOR result as an integer and add 1106
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
final_int = (int.from_bytes(merged_bytes, 'big') + 1106) % N
final_hex = hex(final_int)[2:].zfill(64)

print(f"Plaintext XOR WIF: {base58_check_encode('80' + final_hex)}")