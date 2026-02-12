import binascii

# The fragment you just discovered
half_a = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# Common "Better Half" candidates in this puzzle
candidates = [
    "0000000000000000000000000000000000000000000000000000000000000001", # Genesis/Dummy
    "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23", # The Phase 5 Key
    "5b50d995383508d0705a3036e652c6f1d2c6c39f04128f28c292f72c67b2d56a"  # Known 'Better Half' hash
]

def xor_hex(hex1, hex2):
    raw1 = binascii.unhexlify(hex1)
    raw2 = binascii.unhexlify(hex2)
    return bytes([a ^ b for a, b in zip(raw1, raw2)]).hex()

print("--- Attempting Duality Merges ---")
for i, b_half in enumerate(candidates):
    result = xor_hex(half_a, b_half)
    print(f"Candidate {i+1} Result: {result}")