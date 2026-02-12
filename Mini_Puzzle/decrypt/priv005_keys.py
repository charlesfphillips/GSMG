import hashlib
import base58
from ecdsa import SigningKey, SECP256k1

def raw_priv_to_wif(priv_hex, compressed=True):
    priv = bytes.fromhex(priv_hex)
    extended = b'\x80' + priv
    if compressed:
        extended += b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()

def priv_to_addr(priv_hex):
    try:
        sk = SigningKey.from_string(bytes.fromhex(priv_hex), curve=SECP256k1)
        vk = sk.verifying_key
        pub = b'\x04' + vk.to_string()  # uncompressed
        sha = hashlib.sha256(pub).digest()
        rip = hashlib.new('ripemd160', sha).digest()
        extended = b'\x00' + rip
        checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
        return base58.b58encode(extended + checksum).decode()
    except Exception as e:
        return f"Invalid: {e}"

candidates = [
    "f7f9c3927894563cd14f09dc69a203d31006a6726a7b3ec42fe065b681221010",  # 224-256
    "780fe8a960ccad1c8cbb98ecdc73e5364a3b4a0a367eedeaaee31d2672ebd4b2",  # 256-288
    "6aa8b5181216faf62481525ddd73546d892449eefbd4aaf97590d075d5ad35d9",  # 288-320
    "1c1b434b2bd6efb3c51e53023a7817bab7567bcb3cad7a4de22f3a4007fada02",  # 320-352
]

for i, priv_hex in enumerate(candidates):
    wif = raw_priv_to_wif(priv_hex)
    addr = priv_to_addr(priv_hex)
    print(f"Candidate {i} (offset ~{224 + i*32}):")
    print(f"  WIF (compressed): {wif}")
    print(f"  Address: {addr}")
    print()