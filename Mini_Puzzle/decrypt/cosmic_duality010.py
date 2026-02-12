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

# 1. THE DECRYPTED SOURCE
decrypted_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. THE "NO SPOON" TRUNCATION
# If 128-bit entropy was the signpost, 160-bit (20 bytes) is often the Reward
# because RIPEMD-160 is the heart of the address.
reward_entropy = decrypted_key_hex[:40] # First 20 bytes

# 3. THE BELLA CIAO SALT
passphrase = b"BellaCiao"
final_seed = hashlib.sha256(binascii.unhexlify(reward_entropy) + passphrase).hexdigest()

print(f"Final Reward Scalar: {final_seed}")
print("-" * 30)
# We test UNCOMPRESSED because the signpost 19Av3 was uncompressed
print(f"Uncompressed WIF: {base58_check_encode('80' + final_seed)}")