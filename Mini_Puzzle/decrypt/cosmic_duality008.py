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

# 1. THE "END" (The second 128 bits of your original decrypted source)
# Original: 8badeb454dbeb5d2263d8774b8b24f1b | d14fd658bc7635cab922f80d5a7b54af
entropy_end_hex = "d14fd658bc7635cab922f80d5a7b54af"

# 2. TRANSCENDING CAUSALITY
# We apply the 844e86... mask to this half
mask_hex = "844e86a69a04eea672049e0e0e8612"
mask_int = int(mask_hex.ljust(32, '0'), 16)
end_int = int(entropy_end_hex, 16)

# XOR the End with the Mask
final_entropy_int = end_int ^ mask_int
final_entropy_hex = hex(final_entropy_int)[2:].zfill(32)

# 3. DERIVE THE KEY
# We use SHA256(Entropy + "BellaCiao") to find the Treasury
passphrase = b"BellaCiao"
combined = binascii.unhexlify(final_entropy_hex) + passphrase
final_key_hex = hashlib.sha256(combined).hexdigest()

print(f"Treasury Scalar: {final_key_hex}")
print("-" * 30)
print(f"Compressed WIF: {base58_check_encode('80' + final_key_hex + '01')}")
print(f"Uncompressed WIF: {base58_check_encode('80' + final_key_hex)}")