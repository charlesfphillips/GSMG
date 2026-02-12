# full_scanner_loose.py - LOWER THRESHOLD / NO FILTER VERSION
import hashlib
import base58
import math
from ecdsa import SigningKey, SECP256k1

PRIZE_ADDR = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
FILE_PATH = "cosmic_decrypted_nopad.bin"

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

print(f"Scanning EVERY 32-byte window in {FILE_PATH} ({len(open(FILE_PATH, 'rb').read())} bytes)...\n")

with open(FILE_PATH, 'rb') as f:
    data = f.read()

found = False
checked = 0

for offset in range(len(data) - 31):
    checked += 1
    candidate = data[offset:offset + 32]
    wif = raw_priv_to_wif(candidate)
    addr = priv_to_addr(candidate)

    if addr == PRIZE_ADDR:
        print(f"\n*** WINNER FOUND AT OFFSET {offset} ***")
        print(f"Raw hex: {candidate.hex()}")
        print(f"WIF (compressed): {wif}")
        print(f"Address: {addr} ← PRIZE KEY!")
        print("IMPORT THIS WIF INTO ELECTRUM NOW!")
        found = True
        # continue or break — your choice
        # break

    if offset % 200 == 0 and offset > 0:
        print(f"Scanned {offset} / {len(data)-31} positions...")

if not found:
    print(f"\nChecked all {checked} possible 32-byte windows — no match to {PRIZE_ADDR}")
    print("Next: pairwise combinations or DER/WIF string search.")