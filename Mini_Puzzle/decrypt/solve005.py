import hashlib
import binascii

# Constants for Secp256k1
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Your Extracted Components
K1_HEX = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
K2_HEX = "a986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2"
LUV_OFFSET = 1106

def b58check_encode(hex_payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    raw_bin = binascii.unhexlify(hex_payload)
    digest = hashlib.sha256(hashlib.sha256(raw_bin).digest()).digest()
    num = int((raw_bin + digest[:4]).hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

def solve_duality():
    k1 = int(K1_HEX, 16)
    k2 = int(K2_HEX, 16)
    
    # 1. Calculate the Modular Midpoint: (k1 + k2) * inv(2) mod N
    # This is the "Duality Balance"
    inv_2 = pow(2, -1, N)
    midpoint = ((k1 + k2) * inv_2) % N
    
    # 2. Apply the LUV Offset
    # In many puzzles, the offset is added to the finalized coordinate
    final_scalar = (midpoint + LUV_OFFSET) % N
    final_hex = hex(final_scalar)[2:].zfill(64)
    
    print(f"Final Treasury Scalar: {final_hex}")
    print("-" * 30)
    print(f"Uncompressed WIF: {b58check_encode('80' + final_hex)}")
    print(f"Compressed WIF:   {b58check_encode('80' + final_hex + '01')}")

if __name__ == "__main__":
    solve_duality()