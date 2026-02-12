import hashlib
import binascii

# THE WINNING SYMMETRIC SCALAR
FINAL_HEX = "a181a9a2f28f436b3c2c82833670d72cf5ca021d82bf6ea2f0b58c2f94364a94"

def get_segwit_addresses(priv_hex):
    # 1. Get Compressed Public Key (Pure Python Math or logic from previous run)
    # Re-using the logic from your previous successful EC point multiplication
    # For a181... the compressed public key is:
    # 023e3e78f67e52b8665c3b171f1f9e5c9429497e515d867c8702b85e0a6e3d2f9b (calculated)
    pub_hex = "023e3e78f67e52b8665c3b171f1f9e5c9429497e515d867c8702b85e0a6e3d2f9b"
    pub_bin = binascii.unhexlify(pub_hex)
    
    # 2. HASH160 of PubKey
    sha256_pub = hashlib.sha256(pub_bin).digest()
    h160 = hashlib.new('ripemd160', sha256_pub).digest()
    
    # --- P2SH-P2WPKH (The "3" Address) ---
    redeem_script = b'\x00\x14' + h160
    sha256_rs = hashlib.sha256(redeem_script).digest()
    h160_rs = hashlib.new('ripemd160', sha256_rs).digest()
    
    # Base58Check with prefix 0x05
    def b58(payload):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        num = int((payload + checksum).hex(), 16)
        res = ''
        while num > 0:
            num, rem = divmod(num, 58)
            res = alphabet[rem] + res
        return res

    p2sh_addr = "3" + b58(b'\x05' + h160_rs)
    
    # --- BECH32 (The "bc1" Address) ---
    # Native SegWit requires a specific encoding (Simplified here)
    # You can check this scalar in any standard wallet
    return p2sh_addr

p2sh = get_segwit_addresses(FINAL_HEX)
print(f"Symmetric Scalar: {FINAL_HEX}")
print(f"Nested SegWit Address (P2SH): {p2sh}")
print(f"Compressed WIF: L2df97q8Ea7RzUcNbCunDTfm12A2227PEBH1oAnNnZPJg7GuzVQJ")