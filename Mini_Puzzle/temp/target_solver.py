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
mystery_string = "3U^}ik^ -u?< " # 

target_address = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# Variation 1: SHA256 of the XORed components
k1_int = int(k1_hex, 16)
k2_int = int(k2_hex, 16)
xor_bytes = (k1_int ^ k2_int).to_bytes(32, 'big')
k_v1 = int(hashlib.sha256(xor_bytes + mystery_string.encode()).hexdigest(), 16) % n

# Variation 2: Using the mystery string as a literal Hex Offset (if applicable)
# We test if the string itself represents a hex value hidden in ASCII
try:
    hex_offset = int(mystery_string.strip().replace(" ", ""), 16)
    k_v2 = (k1_int + k2_int + hex_offset) % n
except:
    k_v2 = 0

tests = [("XOR-Hash-String", k_v1), ("Hex-String-Offset", k_v2)]

for name, k_val in tests:
    if k_val == 0: continue
    k_hex = format(k_val, '064x')
    addr = private_key_to_address(k_hex)
    print(f"{name}: {addr}")
    if addr == target_address:
        print(f"!!! MATCH FOUND: {k_hex} !!!")