import hashlib
import base58
from ecdsa import SigningKey, SECP256k1

n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def raw_priv_to_wif(priv_hex, compressed=True):
    priv = bytes.fromhex(priv_hex)
    extended = b'\x80' + priv
    if compressed:
        extended += b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()

def priv_to_addr(priv_hex):
    sk = SigningKey.from_string(bytes.fromhex(priv_hex), curve=SECP256k1)
    vk = sk.verifying_key
    pub = b'\x04' + vk.to_string()  # uncompressed pubkey for hashing
    sha = hashlib.sha256(pub).digest()
    rip = hashlib.new('ripemd160', sha).digest()
    extended = b'\x00' + rip
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()

candidates = {
    "Add": "5cdd76796a772faf9cd8659445ebec5dc4c862cd95383aff174a455953a89b3b",
    "Sub": "ba7e601131063bf4afa2a9552b78b1d9ddd749e3e3b430965afbaac1614e0e23",
    "XOR": "5a8260715106cc0f50a7596b358bd25b7f68bf03347c90baa4db53d59318d362",
}

for name, hex_val in candidates.items():
    wif = raw_priv_to_wif(hex_val)
    addr = priv_to_addr(hex_val)
    print(f"{name}:")
    print(f"  WIF (compressed): {wif}")
    print(f"  Address: {addr}")
    print()