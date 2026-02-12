import hashlib
import itertools
import time

# Standard Base58 for WIF Checksum Validation
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# Puzzle data from salphaseion_real.txt
# We use the raw strings from your previous successful frequency analysis
SECTION2_K1 = "agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde"
SECTION3_K2 = "cfobfdhgdobdgooiigdocdaoofidh"
CUSTOM_ALPHABET = "abcdefghio"

def base58_encode(raw_bytes):
    """Encodes bytes to Bitcoin Base58 string"""
    n = int.from_bytes(raw_bytes, 'big')
    res = ""
    while n > 0:
        n, r = divmod(n, 58)
        res = BASE58_ALPHABET[r] + res
    return res

def get_wif_from_bytes(key_bytes, compressed=False):
    """Adds version byte and checksum, then encodes to Base58 WIF"""
    # 0x80 is the mainnet private key prefix
    extended = b'\x80' + key_bytes
    if compressed:
        extended += b'\x01'
    
    # Double SHA-256 for Checksum
    h1 = hashlib.sha256(extended).digest()
    h2 = hashlib.sha256(h1).digest()
    final_data = extended + h2[:4]
    
    return base58_encode(final_data)

def vic_optimized_search():
    print("="*60)
    print("🚀 FIXED VIC-OPTIMIZED BRUTE FORCE (P1000)")
    print("="*60)
    
    # Pool derived from VIC "Half/Better Half" clue
    # Letters: H, A, L, F, B, E, T, R, N, D (mapped to 0-9)
    # Since Section 2/3 are likely HEX/DIGIT encoded via A1Z26 (a=1, b=2... o=0)
    # we map the alphabet directly to digits 0-9.
    
    digits = "1234567890" 
    target_letters = list(CUSTOM_ALPHABET) # a, b, c, d, e, f, g, h, i, o
    
    start_time = time.time()
    tested = 0

    # The most likely scenario: a=1, b=2, c=3... o=0 (Standard A1Z26)
    # But we will permute the digits to find the specific 'creator' mapping
    for perm in itertools.permutations(digits):
        mapping = dict(zip(target_letters, perm))
        
        # 1. Convert letter strings to digit strings
        s2_digits = "".join(mapping[c] for c in SECTION2_K1)
        s3_digits = "".join(mapping[c] for c in SECTION3_K2)
        
        # 2. Convert digit strings to Hex bytes (e.g., "17" -> 0x17)
        # This assumes the sections are hex-encoded strings
        try:
            if len(s2_digits) % 2 == 0:
                k1_bytes = bytes.fromhex(s2_digits)
                if len(k1_bytes) == 32: # Standard Private Key length
                    k1_wif = get_wif_from_bytes(k1_bytes, compressed=False)
                    # Check if it generates a known address or starts with 5
                    if k1_wif.startswith('5'):
                         print(f"\n✅ FOUND k1: {k1_wif}")
                         
            if len(s3_digits) % 2 == 0:
                k2_bytes = bytes.fromhex(s3_digits)
                if len(k2_bytes) == 32:
                    k2_wif = get_wif_from_bytes(k2_bytes, compressed=True)
                    if k2_wif.startswith('L') or k2_wif.startswith('K'):
                         print(f"\n✅ FOUND k2: {k2_wif}")
                         return
        except:
            continue

        tested += 1
        if tested % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"\rTested: {tested:,} permutations... Rate: {int(tested/elapsed)}/s", end="")

    print("\n\nSearch complete.")

if __name__ == "__main__":
    vic_optimized_search()