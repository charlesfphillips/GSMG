import hashlib
import itertools
import time
import sys

# Standard Base58 for WIF Checksum Validation
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# Puzzle data from salphaseion_real.txt
SECTION2_K1 = "agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde"
SECTION3_K2 = "cfobfdhgdobdgooiigdocdaoofidh"
CUSTOM_ALPHABET = "abcdefghio"

# The VIC Cipher Alphabet provided in the clue
VIC_POOL = "FUBCDORALETHINGKYMVPSJQZXW5" # Added '5' because WIF must start with 5

def b58_decode(v):
    n = 0
    for char in v:
        n = n * 58 + BASE58_ALPHABET.index(char)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

def validate_wif(wif_str):
    """Validates Bitcoin WIF checksum (Double SHA256)"""
    try:
        raw = b58_decode(wif_str)
        payload = raw[:-4]
        checksum = raw[-4:]
        hash1 = hashlib.sha256(payload).digest()
        hash2 = hashlib.sha256(hash1).digest()
        return hash2[:4] == checksum
    except:
        return False

def vic_optimized_search():
    print("="*60)
    print("🚀 VIC-OPTIMIZED GPU BRUTE FORCE (P1000 Edition)")
    print("="*60)
    
    # HEURISTIC LOCKS: 
    # k1 (Sec 2) starts with 'a'. Uncompressed WIFs start with '5'.
    # k2 (Sec 3) starts with 'c'. Compressed WIFs start with 'L' or 'K'.
    
    fixed_mappings = {'a': '5'}
    k2_starts = ['L', 'K']
    
    # Remaining letters in our custom alphabet to map
    remaining_custom = [char for char in CUSTOM_ALPHABET if char not in ['a', 'c']]
    
    # Build the pool from the VIC hint characters
    # We remove '5' and 'L/K' from the pool to map the remaining positions
    pool_base = [c for c in "HALFBETRND" if c in BASE58_ALPHABET] # From "Half/Better Half"
    pool_extended = [c for c in VIC_POOL if c not in ['5', 'L', 'K'] and c in BASE58_ALPHABET]
    
    # Use the first 10-12 chars of the VIC alphabet for the mapping
    search_pool = list(dict.fromkeys(pool_base + pool_extended))[:10]
    
    print(f"Fixed: 'a' -> '5'")
    print(f"Pool: {search_pool}")
    print(f"Targeting: k1 (Length 51), k2 (Length 52)")
    
    start_time = time.time()
    tested = 0

    for k2_start in k2_starts:
        print(f"\nTesting with 'c' -> '{k2_start}'...")
        current_fixed = fixed_mappings.copy()
        current_fixed['c'] = k2_start
        
        # Permutations of the pool for the remaining 8 letters
        for perm in itertools.permutations(search_pool, len(remaining_custom)):
            mapping = current_fixed.copy()
            for i, char in enumerate(remaining_custom):
                mapping[char] = perm[i]
            
            # Construct the WIFs
            k1_candidate = "".join(mapping[c] for c in SECTION2_K1[:51])
            k2_candidate = "".join(mapping[c] for c in SECTION3_K2 + " " * (52-len(SECTION3_K2))) # Padding logic
            
            # Optimization: Only checksum if the strings look like WIFs
            if k1_candidate.startswith('5'):
                if validate_wif(k1_candidate):
                    print(f"\n✅ POTENTIAL k1 FOUND: {k1_candidate}")
                    # If k1 is found, we narrow intensely on k2
                    if validate_wif(k2_candidate):
                        print(f"🏆 DOUBLE MATCH! k2: {k2_candidate}")
                        return mapping
            
            tested += 1
            if tested % 50000 == 0:
                elapsed = time.time() - start_time
                print(f"\rTested: {tested:,} | Rate: {int(tested/elapsed)}/s", end="")

    print("\n\nNo matches found in this VIC subset.")

if __name__ == "__main__":
    vic_optimized_search()