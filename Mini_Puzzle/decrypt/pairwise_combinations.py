# pairwise_combinations.py
# Finds high-entropy 32-byte blocks
# Tries every unique pair with add/sub/XOR mod n
# Checks resulting address against prize

import hashlib
import base58
import math
from ecdsa import SigningKey, SECP256k1

PRIZE_ADDR = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
FILE_PATH = "cosmic_decrypted_nopad.bin"
CURVE_ORDER_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def raw_priv_to_wif(priv_bytes, compressed=True):
    extended = b'\x80' + priv_bytes
    if compressed:
        extended += b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()

def priv_to_addr(priv_bytes):
    try:
        sk = SigningKey.from_string(priv_bytes, curve=SECP256k1)
        vk = sk.verifying_key
        pub = b'\x04' + vk.to_string()
        sha = hashlib.sha256(pub).digest()
        rip = hashlib.new('ripemd160', sha).digest()
        extended = b'\x00' + rip
        checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
        return base58.b58encode(extended + checksum).decode()
    except:
        return None

print(f"Collecting high-entropy 32-byte candidates from {FILE_PATH}...\n")

with open(FILE_PATH, 'rb') as f:
    data = f.read()

candidates = []
for offset in range(len(data) - 31):
    block = data[offset:offset + 32]
    counts = [block.count(b) for b in range(256)]
    p = [v / 32 for v in counts if v > 0]
    entropy = -sum(pi * math.log2(pi) for pi in p) if p else 0
    if entropy > 7.0:  # adjustable threshold
        candidates.append((offset, block.hex()))

print(f"Found {len(candidates)} candidates with entropy >7.0\n")

# Check single candidates first
print("Checking single candidates:")
for offset, hex_str in candidates:
    priv_bytes = bytes.fromhex(hex_str)
    addr = priv_to_addr(priv_bytes)
    if addr == PRIZE_ADDR:
        wif = raw_priv_to_wif(priv_bytes)
        print(f"\n*** SINGLE CANDIDATE WINNER AT OFFSET {offset} ***")
        print(f"Hex: {hex_str}")
        print(f"WIF: {wif}")
        print(f"Address: {addr}")

# Pairwise combinations
print("\nCycling through all unique pairs (add/sub/XOR)...")
pairs_checked = 0

for i in range(len(candidates)):
    for j in range(i + 1, len(candidates)):
        offset1, hex1 = candidates[i]
        offset2, hex2 = candidates[j]
        k1 = int(hex1, 16)
        k2 = int(hex2, 16)
        pairs_checked += 1

        for op_name, result in [
            ("Add (k1 + k2)", (k1 + k2) % CURVE_ORDER_N),
            ("Sub (k1 - k2)", (k1 - k2) % CURVE_ORDER_N),
            ("Sub (k2 - k1)", (k2 - k1) % CURVE_ORDER_N),
            ("XOR", k1 ^ k2)
        ]:
            result_hex = f"{result:064x}"
            priv_bytes = bytes.fromhex(result_hex)
            addr = priv_to_addr(priv_bytes)
            if addr == PRIZE_ADDR:
                wif = raw_priv_to_wif(priv_bytes)
                print(f"\n*** {op_name} WINNER FROM PAIR (offsets {offset1}, {offset2}) ***")
                print(f"k1: {hex1}")
                print(f"k2: {hex2}")
                print(f"Result hex: {result_hex}")
                print(f"WIF (compressed): {wif}")
                print(f"Address: {addr} ← PRIZE KEY!")
                print("IMPORT THIS WIF INTO ELECTRUM NOW!")

        if pairs_checked % 50 == 0:
            print(f"Processed {pairs_checked} pairs...")

print(f"\nAll {pairs_checked} pairs checked — no match found.")
print("If no winner, try lowering entropy threshold to 6.0 or scan for DER/WIF strings.")