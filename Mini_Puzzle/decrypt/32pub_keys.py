# Save as raw_priv_to_addr.py
import hashlib, base58

def raw_priv_to_wif(priv_hex, compressed=True):
    priv = bytes.fromhex(priv_hex)
    extended = b'\x80' + priv
    if compressed:
        extended += b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()

def priv_to_addr(priv_hex):
    # Same as pubkey_to_addr but derives pubkey first (needs ecdsa)
    from ecdsa import SigningKey, SECP256k1
    sk = SigningKey.from_string(bytes.fromhex(priv_hex), curve=SECP256k1)
    vk = sk.verifying_key
    pub = b'\x04' + vk.to_string()  # uncompressed for simplicity
    return pubkey_to_addr(pub.hex())

candidates = [
    "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af",
    "d12f8b341cb879dd769ade1f8d399d40ae27695b880aa5701df9abd8c96387cd",
    "9205a339dbf3fc5a1c6d0a8e6793438a59cc52261c54b68193aea541ca0526db",
    "9ccfe92a60ad7cc63d43391570c49585a01ade76ca09e03ad533f498831f1916",
]

for i, priv in enumerate(candidates):
    print(f"Candidate {i}: WIF (comp) = {raw_priv_to_wif(priv)}")
    try:
        print(f"         Address = {priv_to_addr(priv)}")
    except:
        print("         Invalid privkey")