import hashlib

def hex_to_int(h):
    return int(h.replace(" ", ""), 16)

def encode_base58(b):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int.from_bytes(b, 'big')
    res = ""
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# THE COORDINATES FROM SOLUTION_DECRYPTED.bin
K1_hex = "C8956D4AC326EAC2D510BC4748D1CD9D898F1F55FC2E38494E228AA77EB88B67"
K2_hex = "D353548D1007C81AD1F1601A6C46677C96CCAF0D2A4067E65D0355B1FB07DDF8"
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 1. Calculate Private Key Integer
d = (hex_to_int(K1_hex) + hex_to_int(K2_hex)) % n
d_hex = format(d, '064x')

# 2. Convert to WIF (Wallet Import Format)
extended_key = "80" + d_hex
first_sha = hashlib.sha256(bytes.fromhex(extended_key)).digest()
second_sha = hashlib.sha256(first_sha).digest()
checksum = second_sha[:4].hex()
final_key_hex = extended_key + checksum
wif = encode_base58(bytes.fromhex(final_key_hex))

print(f"--- RECOVERY RESULTS ---")
print(f"Private Key (Hex): {d_hex.upper()}")
print(f"Private Key (WIF): {wif}")
print(f"------------------------")