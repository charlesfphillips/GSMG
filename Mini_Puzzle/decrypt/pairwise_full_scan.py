# pairwise_full_scan.py - FULL SCAN + PAIRWISE + DER/WIF SEARCH
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

with open(FILE_PATH, 'rb') as f:
    data = f.read()

print(f"Full scan of {FILE_PATH} ({len(data)} bytes)...\n")

# ────────────────────────────────────────────────
# Part 1: Collect ALL 32-byte windows (no strict filter)
# ────────────────────────────────────────────────

candidates = []
for offset in range(len(data) - 31):
    block = data[offset:offset + 32]
    # Loose filter: skip all-zero or all-same-byte blocks
    if len(set(block)) > 4:  # at least 5 unique bytes
        candidates.append((offset, block.hex()))

print(f"Collected {len(candidates)} candidate 32-byte blocks (loose filter)\n")

# Check single candidates
print("Checking single candidates...")
single_found = False
for offset, hex_str in candidates:
    priv_bytes = bytes.fromhex(hex_str)
    addr = priv_to_addr(priv_bytes)
    if addr == PRIZE_ADDR:
        wif = raw_priv_to_wif(priv_bytes)
        print(f"\n*** SINGLE WINNER AT OFFSET {offset} ***")
        print(f"Hex: {hex_str}")
        print(f"WIF (compressed): {wif}")
        print(f"Address: {addr} ← PRIZE KEY!")
        single_found = True

if not single_found:
    print("No single candidate matches the prize address.\n")

# ────────────────────────────────────────────────
# Part 2: Pairwise combinations on first 50 candidates (to avoid too many pairs)
# ────────────────────────────────────────────────

print("Cycling pairwise combinations on first 50 candidates (add/sub/XOR)...")
n = CURVE_ORDER_N
pairs_checked = 0
pair_found = False

for i in range(min(50, len(candidates))):
    for j in range(i + 1, min(50, len(candidates))):
        offset1, hex1 = candidates[i]
        offset2, hex2 = candidates[j]
        k1 = int(hex1, 16)
        k2 = int(hex2, 16)
        pairs_checked += 1

        for op_name, op in [
            ("Add", (k1 + k2) % n),
            ("Sub k1-k2", (k1 - k2) % n),
            ("Sub k2-k1", (k2 - k1) % n),
            ("XOR", k1 ^ k2)
        ]:
            result_hex = f"{op:064x}"
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
                pair_found = True

        if pairs_checked % 50 == 0:
            print(f"Processed {pairs_checked} pairs...")

if not pair_found:
    print(f"\nAll {pairs_checked} pairs checked — no match found.")
    print("If no winner, keys may be DER-encoded or require different logic.")

# ────────────────────────────────────────────────
# Part 3: Quick DER and WIF string search
# ────────────────────────────────────────────────

print("\nSearching for DER structures (30 81/82) and WIF-like strings...")
for offset in range(len(data) - 4):
    if data[offset:offset+2] in [b'\x30\x81', b'\x30\x82']:
        print(f"Possible DER at offset {offset}: {data[offset:offset+100].hex()[:100]}...")
    # WIF-like (5/K/L + ~50 Base58 chars)
    if offset + 52 <= len(data) and data[offset] in b'5KL' and all(b in b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' for b in data[offset+1:offset+52]):
        wif_str = data[offset:offset+52].decode()
        print(f"Possible WIF string at offset {offset}: {wif_str}")