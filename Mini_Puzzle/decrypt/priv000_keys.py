from ecdsa import SigningKey, SECP256k1
import hashlib, base58

priv_hex = "5f450dbd85166d2acee54fcc106ab7f309876ef0648edd12719a50d5a2938c67"
sk = SigningKey.from_string(bytes.fromhex(priv_hex), curve=SECP256k1)
vk = sk.verifying_key
pub = b'\x04' + vk.to_string()  # uncompressed pubkey
sha = hashlib.sha256(pub).digest()
rip = hashlib.new('ripemd160', sha).digest()
extended = b'\x00' + rip
checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
addr = base58.b58encode(extended + checksum).decode()
print("Address:", addr)