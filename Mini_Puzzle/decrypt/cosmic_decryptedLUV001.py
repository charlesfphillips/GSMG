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

# Half A (The key you just posted)
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# The Command String + the LUV 1106 Salt
# Note: The puzzle often requires the command exactly as it appears in the hint
cmd_string = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin1106"

# Generate the "Better Half"
better_half = hashlib.sha256(cmd_string.encode('utf-8')).hexdigest()

# Perform the XOR Duality
raw_a = binascii.unhexlify(half_a_hex)
raw_b = binascii.unhexlify(better_half)
merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

print(f"Final WIF (Uncompressed): {base58_check_encode('80' + merged)}")
print(f"Final WIF (Compressed):   {base58_check_encode('80' + merged + '01')}")