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

# 2. Better Half: SHA256 of the successful decryption command
cmd = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin"
cmd_hash = hashlib.sha256(cmd.encode('utf-8')).hexdigest()

# 3. Apply LUV 1106: XOR the hash with the salt 1106 (hex 0452)
# In these puzzles, LUV usually means XORing the last bytes
int_hash = int(cmd_hash, 16)
int_luv = 1106
salted_better_half = hex(int_hash ^ int_luv)[2:].zfill(64)

# 4. Final Duality XOR
raw_a = binascii.unhexlify(half_a_hex)
raw_b = binascii.unhexlify(salted_better_half)
merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

print(f"Final WIF (Uncompressed): {base58_check_encode('80' + merged)}")
print(f"Final WIF (Compressed):   {base58_check_encode('80' + merged + '01')}")