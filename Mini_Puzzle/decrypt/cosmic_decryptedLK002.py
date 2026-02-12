import hashlib
import binascii

def base58_check_encode(hex_payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    raw_bin = binascii.unhexlify(hex_payload)
    # Double SHA256 for checksum
    digest1 = hashlib.sha256(raw_bin).digest()
    digest2 = hashlib.sha256(digest1).digest()
    final_bin = raw_bin + digest2[:4]
    num = int(final_bin.hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# Better Half: The hash of the "Last Command"
cmd = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin"
better_half = hashlib.sha256(cmd.encode('utf-8')).hexdigest()

# XOR the halves first (The "Built It" step)
int_a = int(half_a_hex, 16)
int_b = int(better_half, 16)
xor_result = int_a ^ int_b

# Add the "Funds" (LUV 1106) to make it "Live"
# 1106 is the satoshi value from transaction 14
final_int = (xor_result + 1106) % (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)
final_hex = hex(final_int)[2:].zfill(64)

print(f"Final Living WIF (Uncompressed): {base58_check_encode('80' + final_hex)}")
print(f"Final Living WIF (Compressed):   {base58_check_encode('80' + final_hex + '01')}")