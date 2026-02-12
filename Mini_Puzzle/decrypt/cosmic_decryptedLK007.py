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

# 2. Plaintext "Last Command" (First 32 chars)
cmd_plaintext = "openssl enc -aes-256-cbc -d -a " 
# Ensure it is exactly 32 bytes for the XOR
cmd_padded = cmd_plaintext.ljust(32, ' ')

# 3. Apply the "LUV 1106" Rotation
# We rotate the bytes of the command by 1106 % length
shift = 1106 % 32
rotated_cmd = cmd_padded[shift:] + cmd_padded[:shift]
raw_b = rotated_cmd.encode('ascii')

# 4. XOR Duality
merged_bytes = bytes([a ^ b for a, b in zip(raw_a, raw_b)])
final_hex = merged_bytes.hex()

print(f"Rotated Plaintext WIF: {base58_check_encode('80' + final_hex)}")