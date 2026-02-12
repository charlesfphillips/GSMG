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

# Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# Better Half: Hash of the OpenSSL command
cmd = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin"
cmd_hash = hashlib.sha256(cmd.encode('utf-8')).hexdigest()

# LUV 1106 as Little Endian (5204)
# We apply it to the last two bytes of the merged key
int_a = int(half_a_hex, 16)
int_b = int(cmd_hash, 16)
base_xor = int_a ^ int_b

# 0x5204 is the Little-Endian 'LUV' of 1106
living_key_int = base_xor ^ 0x5204
final_hex = hex(living_key_int)[2:].zfill(64)

print(f"LUV LE XOR WIF: {base58_check_encode('80' + final_hex)}")

# Alternative: Adding 1106 to the total sum (Decimal addition)
alt_living_int = (base_xor + 1106) % (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)
alt_hex = hex(alt_living_int)[2:].zfill(64)
print(f"LUV Decimal Add WIF: {base58_check_encode('80' + alt_hex)}")