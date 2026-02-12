import hashlib
import binascii

# 1. THE WORDLIST (BIP-39 excerpt for the 'Beginning')
# Normally we'd use the full 2048 words, but we can derive the first index
binary_seed = "100010111010110111101011010001010100110110111110101101011101001000100110001111011000011101110100101110001011001001001111000110111010"

# Every 11 bits is a word index
indices = [int(binary_seed[i:i+11], 2) for i in range(0, len(binary_seed)-4, 11)]
print(f"Word Indices: {indices}")

# 2. THE TRANSCENDED KEY (The 'No Spoon' approach)
# Instead of full PBKDF2, the Architect often uses SHA256(Binary + Passphrase)
passphrase = b"BellaCiao"
binary_bytes = int(binary_seed, 2).to_bytes(17, byteorder='big')
combined = binary_bytes + passphrase

# 3. APPLYING THE SYMBOLS
# ♀ (12) - Shift Right by 12
# 666 - The Twist
# 553 - The Halved Fund (1106 / 2)
raw_hash = hashlib.sha256(combined).digest()
raw_int = int.from_bytes(raw_hash, 'big')

# The Final "Bella Ciao" transformation
final_int = (raw_int >> 12) ^ 666
final_int = (final_int + 553) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

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

final_hex = hex(final_int)[2:].zfill(64)
compressed_payload = '80' + final_hex + '01'
print(f"Bella Ciao Seed WIF: {base58_check_encode(compressed_payload)}")