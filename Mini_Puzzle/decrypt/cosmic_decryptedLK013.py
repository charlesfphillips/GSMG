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

# Half A: Decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
int_a = int(half_a_hex, 16)

# Better Half: The "Halved" Command Hash
cmd = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin"
sha_cmd = hashlib.sha256(cmd.encode('ascii')).digest()
# The "Halving" clue points to RIPEMD-160 (the 'halved' 20-byte hash)
ripemd_cmd = hashlib.new('ripemd160', sha_cmd).hexdigest()
int_b = int(ripemd_cmd, 16)

# Applying "LUV 1106" as the Life/Funding offset
# We add them together (2 of 2 / Built It) and add the 1106 satoshis
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
final_int = (int_a + int_b + 1106) % N
final_hex = hex(final_int)[2:].zfill(64)

print(f"Halved Duality WIF: {base58_check_encode('80' + final_hex)}")