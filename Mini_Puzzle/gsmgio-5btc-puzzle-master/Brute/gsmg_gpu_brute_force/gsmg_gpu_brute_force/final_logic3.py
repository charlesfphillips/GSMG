import hashlib
import base58

# The Curve Order
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def get_int(s):
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)

# 1. The two halves
k_better = get_int("lastwordsbeforearchichoice")
k_half = get_int("thispassword")

# 2. The "LUV" Funds (1106 Satoshis) from the transaction log
k_luv = 1106 

# 3. The "Last Command" (causality)
k_cmd = get_int("causality")

# 4. The Sum: (Better Half + Half + Causality + LUV)
# This represents the "Matrix Sum List" combined with "Funds to Live"
prize_int = (k_better + k_half + k_cmd + k_luv) % N
prize_hex = hex(prize_int)[2:].zfill(64)

def to_wif(hex_val):
    extended = b'\x80' + bytes.fromhex(hex_val) + b'\x01'
    h = hashlib.sha256(hashlib.sha256(extended).digest()).digest()
    return base58.b58encode(extended + h[:4]).decode()

print(f"Final Prize WIF: {to_wif(prize_hex)}")