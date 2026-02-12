import hashlib
import ecdsa
import base58

def private_key_to_address(priv_hex):
    priv_bytes = bytes.fromhex(priv_hex)
    sk = ecdsa.SigningKey.from_string(priv_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key_bytes = vk.to_string()
    prefix = b'\x02' if public_key_bytes[63] % 2 == 0 else b'\x03'
    compressed_pubkey = prefix + public_key_bytes[:32]
    sha = hashlib.sha256(compressed_pubkey).digest()
    h = hashlib.new('ripemd160')
    h.update(sha)
    network_byte = b'\x00' + h.digest()
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    return base58.b58encode(network_byte + checksum).decode('utf-8')

n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
k1_hex = "a78915fc3abc85e6360e00dc4fb4fca395d537c912856ca782ecd55869b0ab20"
k2_hex = "cf6a8a72e391bfab5822d40686aafaec76b44978d380bc42a732ed31f470b964"
target_address = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

with open("answer_3_2.txt", "rb") as f:
    data1 = f.read()
with open("answer3_2.txt", "rb") as f:
    data2 = f.read()

# Logic: XOR the data streams (Duality)
# Since they are different lengths, we XOR up to the shorter length
length = min(len(data1), len(data2))
xor_result = bytes(a ^ b for a, b in zip(data1[:length], data2[:length]))
k3_xor_hash = int(hashlib.sha256(xor_result).hexdigest(), 16)

# Logic: Use the hint string directly as the final entropy
hint_string = "ourfirsthintisyourlastcommand"
k3_hint_hash = int(hashlib.sha256(hint_string.encode()).hexdigest(), 16)

k1_int = int(k1_hex, 16)
k2_int = int(k2_hex, 16)

tests = [
    ("XOR Data Duality", (k1_int + k2_int + k3_xor_hash) % n),
    ("Direct Hint Hash", (k1_int + k2_int + k3_hint_hash) % n)
]

for label, k_val in tests:
    k_hex = format(k_val, '064x')
    addr = private_key_to_address(k_hex)
    print(f"{label}: {addr}")
    if addr == target_address:
        print(f"!!! MATCH !!! HEX: {k_hex}")