import hashlib
import base58

def pubkey_to_addr(pub_hex):
    pub_bytes = bytes.fromhex(pub_hex)
    sha = hashlib.sha256(pub_bytes).digest()
    rip = hashlib.new('ripemd160', sha).digest()
    extended = b'\x00' + rip
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    addr = base58.b58encode(extended + checksum).decode()
    return addr

# Your extracted pubkeys (compressed ones first)
pubkeys = [
    "03d31006a6726a7b3ec42fe065b681221010780fe8a960ccad1c8cbb98ecdc73e5",
    "03fcf7aadaac0a231ba0cdf2812265786737e785799e50690c05130288b8f11867",
    "0288b8f11867a86c016ce3076e1ef94d9b9045c0154c3f328c074e8bede76da1f2",
]

for i, pub in enumerate(pubkeys):
    addr = pubkey_to_addr(pub)
    print(f"Pubkey {i} → Address: {addr}")