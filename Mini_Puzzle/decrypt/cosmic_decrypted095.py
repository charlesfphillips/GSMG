import hashlib
import binascii

def base58_check_encode(hex_payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    raw_bin = binascii.unhexlify(hex_payload)
    first_sha = hashlib.sha256(raw_bin).digest()
    second_sha = hashlib.sha256(first_sha).digest()
    final_bin = raw_bin + second_sha[:4]
    num = int(final_bin.hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# 1. Your Decrypted Half A (from your terminal output)
half_a = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. Derive the "Better Half" from the "Last Command"
# Note: Ensure the string matches your command exactly (single spaces, no trailing newline)
last_command = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin"
better_half = hashlib.sha256(last_command.encode('utf-8')).hexdigest()

# 3. Perform the XOR Duality
raw_a = binascii.unhexlify(half_a)
raw_b = binascii.unhexlify(better_half)
merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

# 4. Generate the Final WIF Keys
print(f"Uncompressed WIF: {base58_check_encode('80' + merged)}")
print(f"Compressed WIF: {base58_check_encode('80' + merged + '01')}")