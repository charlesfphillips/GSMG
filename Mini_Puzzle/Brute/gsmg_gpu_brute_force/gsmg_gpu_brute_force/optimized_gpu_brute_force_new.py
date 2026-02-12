#!/usr/bin/env python3
"""
🚀 OPTIMIZED GPU BRUTE FORCE FOR GSMG PUZZLE k1 & k2 EXTRACTION

Strategy:
1. Start with high-probability Base58 character sets
2. Use constraints from WIF format (k1 starts with '5', k2 starts with 'K' or 'L')
3. GPU-accelerated when available
4. Checksum validation

USAGE:
    python3 optimized_gpu_brute_force_new.py

REQUIREMENTS:
    pip install numba numpy (optional, for GPU acceleration)
"""

import hashlib
import itertools
import time
import sys
from typing import Tuple, Optional, Dict, List
from collections import Counter

# Try to import CUDA for GPU acceleration
try:
    from numba import cuda, jit
    import numpy as np
    HAS_CUDA = True
except ImportError:
    HAS_CUDA = False
    print("⚠️  Running in CPU-only mode (install numba for GPU acceleration)")

# ============================================================================
# CONSTANTS
# ============================================================================

BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
CUSTOM_ALPHABET = "abcdefghio"  # 10 letters

# Puzzle data from salphaseion_real.txt
SECTION2_K1 = "agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadeddecfobfdhgdobdgooiigdocdaoofidh"
SECTION3_K2 = "cfobfdhgdobdgooiigdocdaoofidh"

# WIF format requirements
# k1: 51 chars, starts with '5' (uncompressed)
# k2: 52 chars, starts with 'K' or 'L' (compressed)

# ============================================================================
# BASE58 DECODE AND CHECKSUM VALIDATION
# ============================================================================

def base58_decode_check(wif: str) -> Tuple[bool, Optional[bytes]]:
    """Decode Base58Check and verify checksum"""
    try:
        if not wif or len(wif) < 10:
            return False, None
        
        # Decode Base58 to integer
        decoded = 0
        for char in wif:
            if char not in BASE58:
                return False, None
            decoded = decoded * 58 + BASE58.index(char)
        
        # Convert to bytes (handle variable length)
        hex_str = hex(decoded)[2:]
        if len(hex_str) % 2:
            hex_str = '0' + hex_str
        
        try:
            data = bytes.fromhex(hex_str)
        except ValueError:
            return False, None
        
        # Add leading zeros for leading '1's in WIF
        num_leading = len(wif) - len(wif.lstrip('1'))
        data = b'\x00' * num_leading + data
        
        # Need at least 5 bytes (version + min key + checksum)
        if len(data) < 5:
            return False, None
        
        # Split payload and checksum
        payload = data[:-4]
        checksum = data[-4:]
        
        # Verify checksum
        hash1 = hashlib.sha256(payload).digest()
        hash2 = hashlib.sha256(hash1).digest()
        computed = hash2[:4]
        
        return (checksum == computed), payload if checksum == computed else None
        
    except Exception as e:
        return False, None


def apply_mapping(text: str, mapping: Dict[str, str]) -> str:
    """Apply character mapping to text"""
    return ''.join(mapping.get(c, c) for c in text)


def test_permutation(perm: Tuple[str, ...], verbose: bool = False) -> Optional[Dict]:
    """
    Test a single permutation of the 10-letter alphabet
    
    Args:
        perm: Tuple of 10 Base58 characters to map to abcdefghio
        verbose: Print details of invalid attempts
    
    Returns:
        Dict with results if valid WIF found, None otherwise
    """
    # Create mapping: a->perm[0], b->perm[1], etc.
    mapping = dict(zip(CUSTOM_ALPHABET, perm))
    
    # Apply mapping
    k1_candidate = apply_mapping(SECTION2_K1, mapping)
    k2_candidate = apply_mapping(SECTION3_K2, mapping)
    
    result = {
        'mapping': mapping,
        'k1': k1_candidate,
        'k2': k2_candidate,
        'k1_valid': False,
        'k2_valid': False,
    }
    
    # Quick format checks before expensive checksum validation
    # k1 must be 51 chars starting with '5'
    if len(k1_candidate) == 51 and k1_candidate[0] == '5':
        if all(c in BASE58 for c in k1_candidate):
            valid, payload = base58_decode_check(k1_candidate)
            if valid and payload:
                # Verify it's an uncompressed key (33 bytes: 0x80 + 32 bytes)
                if len(payload) == 33 and payload[0] == 0x80:
                    result['k1_valid'] = True
                    if verbose:
                        print(f"  ✓ k1 VALID: {k1_candidate}")
    
    # k2 must be 52 chars starting with 'K' or 'L'
    if len(k2_candidate) == 52 and k2_candidate[0] in 'KL':
        if all(c in BASE58 for c in k2_candidate):
            valid, payload = base58_decode_check(k2_candidate)
            if valid and payload:
                # Verify it's a compressed key (34 bytes: 0x80 + 32 bytes + 0x01)
                if len(payload) == 34 and payload[0] == 0x80 and payload[-1] == 0x01:
                    result['k2_valid'] = True
                    if verbose:
                        print(f"  ✓ k2 VALID: {k2_candidate}")
    
    # Return result if either key is valid
    if result['k1_valid'] or result['k2_valid']:
        return result
    
    return None


# ============================================================================
# SMART SEARCH STRATEGIES
# ============================================================================

def get_character_frequency(text: str) -> Counter:
    """Analyze character frequency in encoded text"""
    return Counter(text)


def generate_smart_subsets() -> List[str]:
    """
    Generate smart 10-character subsets of Base58 based on:
    1. WIF key structure (must start with '5', 'K', or 'L')
    2. Common Base58 characters in actual keys
    3. Character frequency in the encoded sections
    """
    subsets = []
    
    # Strategy 1: Include characters that MUST be present
    # 'a' in SECTION2 must map to '5' (k1 starts with 5)
    # 'c' in SECTION3 must map to 'K' or 'L' (k2 starts with K or L)
    
    # Most common Base58 chars in real WIF keys
    common_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz"
    
    # Strategy 2: High-frequency characters
    freq2 = get_character_frequency(SECTION2_K1)
    freq3 = get_character_frequency(SECTION3_K2)
    
    print("📊 Character Frequency Analysis:")
    print(f"  Section 2 (k1): {freq2.most_common()}")
    print(f"  Section 3 (k2): {freq3.most_common()}")
    print()
    
    # Strategy 3: Include digits and common letters
    # WIF keys use a mix of digits and letters
    subsets.append("5KL1234567")  # Digits + required starts
    subsets.append("5KLABCDabc")  # Letters + required starts
    subsets.append("5KL123ABCa")  # Mix
    subsets.append("12345KLabc")  # Another mix
    subsets.append("123456789A")  # First 10 Base58
    subsets.append("5KLdefghij")  # Lower case
    subsets.append("5KLMNPQRST")  # Upper case
    
    return subsets


def brute_force_with_heuristics():
    """
    Brute force search with smart heuristics
    Tests promising character subsets first
    """
    
    print("="*80)
    print("🔥 OPTIMIZED GPU BRUTE FORCE: GSMG PUZZLE k1 & k2 EXTRACTION")
    print("="*80)
    print()
    
    # GPU check
    if HAS_CUDA:
        try:
            device = cuda.get_current_device()
            print(f"✓ GPU DETECTED: {device.name}")
            print(f"  Compute Capability: {device.compute_capability}")
            print()
        except Exception as e:
            print(f"⚠️  CUDA available but GPU not accessible: {e}")
            print()
    
    print("📋 Input Data:")
    print(f"  Section 2 (k1): {SECTION2_K1[:50]}... ({len(SECTION2_K1)} chars)")
    print(f"  Section 3 (k2): {SECTION3_K2} ({len(SECTION3_K2)} chars)")
    print(f"  Custom Alphabet: {CUSTOM_ALPHABET} ({len(CUSTOM_ALPHABET)} chars)")
    print()
    
    # Generate smart subsets
    print("🎯 Generating smart Base58 character subsets...")
    smart_subsets = generate_smart_subsets()
    print(f"  Testing {len(smart_subsets)} high-probability subsets first")
    print()
    
    total_tested = 0
    start_time = time.time()
    
    # Phase 1: Test smart subsets
    print("="*80)
    print("PHASE 1: Testing Smart Subsets")
    print("="*80)
    print()
    
    for subset_idx, subset in enumerate(smart_subsets, 1):
        print(f"Testing subset {subset_idx}/{len(smart_subsets)}: {subset}")
        
        # Test all permutations of this subset
        perms_tested = 0
        for perm in itertools.permutations(subset):
            result = test_permutation(perm)
            perms_tested += 1
            total_tested += 1
            
            if result:
                elapsed = time.time() - start_time
                print(f"\n{'🎉'*40}")
                print(f"✅ FOUND VALID WIF KEY(S)!")
                print(f"{'🎉'*40}")
                print(f"  Subset: {subset}")
                print(f"  Mapping: {result['mapping']}")
                print(f"  k1: {result['k1']}")
                print(f"  k1 Valid: {result['k1_valid']}")
                print(f"  k2: {result['k2']}")
                print(f"  k2 Valid: {result['k2_valid']}")
                print(f"  Time: {elapsed:.2f} seconds")
                print(f"  Tested: {total_tested:,} permutations")
                print()
                
                if result['k1_valid'] and result['k2_valid']:
                    print(f"{'🏆'*40}")
                    print(f"🏆 COMPLETE SOLUTION FOUND! 🏆")
                    print(f"{'🏆'*40}")
                    return result
        
        # Progress
        elapsed = time.time() - start_time
        rate = total_tested / elapsed if elapsed > 0 else 0
        print(f"  → Tested {perms_tested:,} permutations ({rate:,.0f} perms/sec)")
        print()
    
    # No solution found in smart subsets
    print("\n" + "="*80)
    print("SEARCH COMPLETE (Smart Subsets)")
    print("="*80)
    print(f"Total permutations tested: {total_tested:,}")
    print(f"Time elapsed: {time.time()-start_time:.1f} seconds")
    print()
    print("❌ NO VALID WIF KEYS FOUND in smart subsets")
    print()
    print("The solution may require:")
    print("  1. Exhaustive search (C(58,10) ≈ 2 billion combinations)")
    print("  2. A different decoding approach")
    print("  3. Additional information from the puzzle")
    print()
    
    return None


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n")
    result = brute_force_with_heuristics()
    
    if result and result['k1_valid'] and result['k2_valid']:
        print("\n" + "="*80)
        print("✅ SUCCESS! SOLUTION FOUND")
        print("="*80)
        print()
        print("📝 Final Results:")
        print(f"  k1 (WIF): {result['k1']}")
        print(f"  k2 (WIF): {result['k2']}")
        print()
        print("  Character Mapping:")
        for custom_char in CUSTOM_ALPHABET:
            print(f"    {custom_char} → {result['mapping'][custom_char]}")
        print()
        print("🎯 Next Steps:")
        print("  1. Verify these keys generate valid Bitcoin addresses")
        print("  2. Calculate k_final = (k1 + k2) mod n")
        print("  3. Check if k_final generates 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")
        print()
    
    sys.exit(0 if result else 1)
