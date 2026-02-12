import hashlib
import binascii

def base58_check_encode(hex_str):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    # Double SHA256 for checksum
    raw_payload = binascii.unhexlify(hex_str)
    first_sha = hashlib.sha256(raw_payload).digest()
    second_sha = hashlib.sha256(first_sha).digest()
    final_hex = raw_payload + second_sha[:4]
    
    # Convert to Base58
    num = int(final_hex.hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# Half A: From your terminal output
half_a = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# Better Half Candidates from transactions.txt and repository
# 1. The Hash160 of the Bella Ciao address
# 2. The TXID of the 5 BTC funding transaction
# 3. The 'Choice' Boolean sequence
candidates = [
    "f69542a4a75e2f16a13d76e4c34a2c53a812e5c6000000000000000000000000",
    "965b73547f639a41dc000db4f62c35fc4a373bd31abab67d0f9ec46a26af740d",
    "73e48ff571a7e9a4387574a50cf2fcb7b21b6ea5702c777a035664df57cbce02"
]

print("--- Final Phase Private Key Generation ---")
for i, b_half in enumerate(candidates):
    raw_a = binascii.unhexlify(half_a)
    raw_b = binascii.unhexlify(b_half)
    # XOR Duality
    merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()
    # Generate WIF (80 for Mainnet)
    wif = base58_check_encode("80" + merged)
    print(f"Candidate {i+1} WIF: {wif}")