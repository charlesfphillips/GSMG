import hashlib
import binascii

def base58_check_encode(hex_str):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    # Double SHA256 for checksum
    first_sha = hashlib.sha256(binascii.unhexlify(hex_str)).digest()
    second_sha = hashlib.sha256(first_sha).hexdigest()
    raw_hex = hex_str + second_sha[:8]
    
    # Convert to Base58
    num = int(raw_hex, 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# 1. Your Decrypted Half A (from your previous terminal output)
half_a = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. The Better Half (The hash160 of 1Pi36y7LJugXwFNDVjR1p8p5JoB7eN5zSZ)
# Derived from the 'Bella Ciao' clue in transactions.txt
better_half = "f69542a4a75e2f16a13d76e4c34a2c53a812e5c6"

# 3. Perform the 'Cosmic Duality' XOR
# We pad the better_half with zeros or repeat it to match 32 bytes
padded_better = better_half.ljust(64, '0')
raw_a = binascii.unhexlify(half_a)
raw_b = binascii.unhexlify(padded_better)
merged_key = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

# 4. Generate the Final WIF
wif_prefix = "80" + merged_key
print(f"Final WIF Solution: {base58_check_encode(wif_prefix)}")