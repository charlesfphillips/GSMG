import hashlib
import base58

# 1. Your Decoded Parts
part1 = "lastwordsbeforearchichoice"
part2 = "thispassword"

# 2. The "Matrix" construction
# We combine the better half and the half
matrix_data = part1 + part2

# 3. "First hint is your last command"
# We append 'causality' as the final instruction (the salt)
final_seed = matrix_data + "causality"

# 4. Generate the Final Key
final_hex = hashlib.sha256(final_seed.encode()).hexdigest()

def to_wif(hex_key):
    # Compressed WIF format
    extended = b'\x80' + bytes.fromhex(hex_key) + b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()

print(f"Final Construction: {final_seed}")
print(f"Final Prize WIF: {to_wif(final_hex)}")