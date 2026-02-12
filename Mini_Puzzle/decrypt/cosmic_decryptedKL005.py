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

# 2. THE HALVING: Split the 32 bytes into two 16-byte halves
part1 = raw_a[:16]
part2 = raw_a[16:]

# 3. DUALITY: XOR the two halves together
xor_half = bytes([a ^ b for a, b in zip(part1, part2)])

# 4. NEED FUNDS TO LIVE: Pad the 16-byte result to 32 bytes 
# using the 1106 Satoshis (0452) as the "Living" tail
# We repeat the salt to fill the remaining 16 bytes
salt = binascii.unhexlify("00000452" * 4)
final_key = xor_half + salt

# 5. Generate Compressed K/L WIF
compressed_payload = '80' + final_key.hex() + '01'

print(f"Halved Duality XOR WIF: {base58_check_encode(compressed_payload)}")