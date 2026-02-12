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
    # Handle leading zeros for Base58
    pad = 0
    for byte in raw_bin:
        if byte == 0: pad += 1
        else: break
    return (alphabet[0] * pad) + res

# 1. Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. Better Half: SHA256 of your Last Command
cmd = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin"
better_half = hashlib.sha256(cmd.encode('utf-8')).hexdigest()

# 3. Apply LUV 1106 XOR Duality
int_a = int(half_a_hex, 16)
int_b = int(better_half, 16)
xor_result = int_a ^ int_b

# 4. Reconfigure for Compressed WIF (The 'K' or 'L' key)
# Append '01' to the hex before Base58Check encoding
merged_hex = hex(xor_result)[2:].zfill(64)
compressed_payload = '80' + merged_hex + '01'

print(f"Compressed WIF (The K/L Key): {base58_check_encode(compressed_payload)}")