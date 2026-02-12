# Save as pubkey_to_addr.py and run: python pubkey_to_addr.py
import hashlib, base58, ecdsa

def pubkey_to_addr(pub_hex):
    pub = bytes.fromhex(pub_hex)
    sha = hashlib.sha256(pub).digest()
    rip = hashlib.new('ripemd160', sha).digest()
    extended = b'\x00' + rip
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    addr = base58.b58encode(extended + checksum)
    return addr.decode()

# Paste your pubkey hexes here (compressed only for now)
pubkeys = [
    "03d31006a6726a7b3ec42fe065b681221010780fe8a960ccad1c8cbb98ecdc73e5",
    "03fcf7aadaac0a231ba0cdf2812265786737e785799e50690c05130288b8f11867",
    "0288b8f11867a86c016ce3076e1ef94d9b9045c0154c3f328c074e8bede76da1f2",
]

for i, p in enumerate(pubkeys):
    print(f"Pubkey {i}: {pubkey_to_addr(p)}")