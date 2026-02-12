import hashlib
import base58

# The Curve Order for secp256k1
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def get_int(s):
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)

# THE LIST: These are the values the puzzle calls the "matrix"
# Try the sum of the two parts you decoded + the core foundation
k1 = get_int("causality")
k2 = get_int("lastwordsbeforearchichoice")
k3 = get_int("thispassword")

# THE SUM
prize_int = (k1 + k2 + k3) % N
prize_hex = hex(prize_int)[2:].zfill(64)

# Convert to WIF
extended = b'\x80' + bytes.fromhex(prize_hex) + b'\x01'
checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
prize_wif = base58.b58encode(extended + checksum).decode()

print(f"Final Prize WIF: {prize_wif}")