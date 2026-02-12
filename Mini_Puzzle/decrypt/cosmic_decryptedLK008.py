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

# 2. Better Half: RIPEMD-160 of the "Last Command"
cmd = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin"
sha_cmd = hashlib.sha256(cmd.encode('utf-8')).digest()
ripemd_cmd = hashlib.new('ripemd160', sha_cmd).hexdigest()

# 3. LUV 1106 Padding (Filling the 32-byte requirement)
# 1106 in hex is 0452. We repeat it to fill the remaining 12 bytes (24 hex chars)
padding = "0452" * 6 
better_half_32byte = ripemd_cmd + padding

# 4. XOR Duality
raw_b = binascii.unhexlify(better_half_32byte)
merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

print(f"RIPEMD-160 XOR WIF: {base58_check_encode('80' + merged)}")