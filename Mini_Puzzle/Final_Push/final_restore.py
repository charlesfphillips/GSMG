import hashlib
import binascii

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
inv2 = pow(2, -1, N)

# The command string found via grep
cmd = "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -K 6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23 -iv c6ff2e39d98843bc3c26b8a33a15b5c9 -out cosmic_decrypted.bin"

# Mathematical Components
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
funds = 1106

# Calculations
better_half = int(hashlib.sha256(cmd.encode('utf-8')).hexdigest(), 16)
halved_a = (int(half_a_hex, 16) * inv2) % N

# The LK Duality Logic: (Half A + Half B + Funds)
final_int = (halved_a + better_half + funds) % N
final_hex = hex(final_int)[2:].zfill(64)

print(f"RECOVERED MASTER HEX: {final_hex}")

import base58

def hex_to_wif(hex_str):
    payload = '80' + hex_str + '01'
    digest = hashlib.sha256(binascii.unhexlify(payload)).digest()
    checksum = hashlib.sha256(digest).digest()[:4]
    return base58.b58encode(binascii.unhexlify(payload + checksum.hex())).decode()

print(f"WIF for 1G Address: {hex_to_wif(final_hex)}")