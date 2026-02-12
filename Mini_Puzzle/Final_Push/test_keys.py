hex_str = "9621e17480351dd14de7a0bcd63ee16e339fe2dd8f6a2a632e8e5e443e412f9e"

# WIF compressed
import hashlib, base58
priv = bytes.fromhex(hex_str)
extended = b'\x80' + priv + b'\x01'
checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
wif = base58.b58encode(extended + checksum).decode()
print("WIF:", wif)

# Address
from ecdsa import SigningKey, SECP256k1
sk = SigningKey.from_string(priv, curve=SECP256k1)
vk = sk.verifying_key
pub = b'\x04' + vk.to_string()
sha = hashlib.sha256(pub).digest()
rip = hashlib.new('ripemd160', sha).digest()
extended = b'\x00' + rip
checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
addr = base58.b58encode(extended + checksum).decode()
print("Address:", addr)