import hashlib

def sha256(s):
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)

def double_sha256(s):
    h = hashlib.sha256(s.encode()).digest()
    return int(hashlib.sha256(h).hexdigest(), 16)

# The Order of the Curve
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Generate the two "Halves"
k1_int = double_sha256("lastwordsbeforearchichoice")
k2_int = double_sha256("thispassword")

# Combine them
final_priv = (k1_int + k2_int) % N

print(f"Final Private Key (Hex): {hex(final_priv)}")