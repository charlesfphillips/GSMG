#!/usr/bin/env python3
"""
GSMG Puzzle Solver - Extract and Decode Tools
Includes decoders for all known cipher types
"""

import re
import sys
import hashlib
from typing import Tuple

class SalphaseionSolver:
    """Decode all Salphaseion sections"""
    
    @staticmethod
    def decode_abba(text: str) -> str:
        """Decode ABBA: a=0, b=1, interpret as binary ASCII"""
        clean = ''.join(c for c in text.lower() if c in 'ab')
        binary = clean.replace('a', '0').replace('b', '1')
        
        result = ""
        for i in range(0, len(binary) - 7, 8):
            byte = binary[i:i+8]
            val = int(byte, 2)
            if 32 <= val <= 126 or val in [9, 10, 13]:  # Include tab, newline, carriage return
                result += chr(val)
            else:
                result += f"[{val}]"
        return result
    
    @staticmethod
    def decode_hex_section(text: str) -> str:
        """
        Decode hex section: a=1...z=26, o=0
        Convert to numeric string, then interpret as hex
        """
        # Build mapping
        char_map = {}
        for i in range(26):
            char_map[chr(ord('a') + i)] = str(i + 1)
        char_map['o'] = '0'
        
        # Convert to number string
        num_str = ''.join(char_map.get(c, '') for c in text.lower() if c in char_map)
        
        # Try different grouping strategies
        results = {}
        
        # Strategy 1: Pairs (most common)
        r1 = ""
        for i in range(0, len(num_str) - 1, 2):
            pair = num_str[i:i+2]
            try:
                val = int(pair, 16)
                if 32 <= val <= 126:
                    r1 += chr(val)
            except:
                pass
        results['pairs'] = r1
        
        # Strategy 2: Triples
        r2 = ""
        for i in range(0, len(num_str) - 2, 3):
            triple = num_str[i:i+3]
            try:
                val = int(triple, 8)  # Octal
                if 32 <= val <= 126:
                    r2 += chr(val)
            except:
                pass
        results['triples'] = r2
        
        # Strategy 3: Custom grouping (1,2,1,2... pattern)
        r3 = ""
        i = 0
        while i < len(num_str):
            # Try 2-digit
            if i + 1 < len(num_str):
                pair = num_str[i:i+2]
                try:
                    val = int(pair, 16)
                    if 32 <= val <= 126:
                        r3 += chr(val)
                        i += 2
                        continue
                except:
                    pass
            i += 1
        results['adaptive'] = r3
        
        return results
    
    @staticmethod
    def extract_all_sections(page_content: str) -> dict:
        """Extract all sections from Salphaseion page"""
        sections = {
            'salphaseion_raw': '',
            'cosmic_duality': '',
        }
        
        # Extract Salphaseion textarea
        salph_match = re.search(r'<textarea[^>]*>(.+?)</textarea>', page_content, re.DOTALL)
        if salph_match:
            sections['salphaseion_raw'] = salph_match.group(1).strip()
        
        # Extract Cosmic Duality textarea
        cosmic_match = re.search(r'<h1>\s*Cosmic Duality\s*</h1>\s*<textarea[^>]*>(.+?)</textarea>', page_content, re.DOTALL)
        if cosmic_match:
            sections['cosmic_duality'] = cosmic_match.group(1).strip()
        
        return sections

def analyze_salphaseion(content: str):
    """Analyze and attempt to decode Salphaseion content"""
    
    print("="*80)
    print("SALPHASEION ANALYSIS & DECODING")
    print("="*80)
    
    # Remove spaces
    content_no_space = content.replace(' ', '')
    print(f"\nContent length: {len(content)} chars (with spaces), {len(content_no_space)} (no spaces)")
    
    # Split by 'z' which appears to be section separator
    parts = content.split(' z ')
    print(f"Number of parts separated by ' z ': {len(parts)}")
    
    for i, part in enumerate(parts):
        print(f"\n{'='*80}")
        print(f"SECTION {i+1}")
        print(f"{'='*80}")
        print(f"Length: {len(part)}")
        print(f"Preview: {part[:100]}...")
        
        # Check what type of encoding
        if all(c in 'ab ' for c in part):
            print("→ Appears to be ABBA binary encoding (a=0, b=1)")
            decoded = SalphaseionSolver.decode_abba(part)
            print(f"Decoded: {decoded[:200]}")
        
        elif any(c in '0123456789' for c in part):
            print("→ Contains numbers (possibly base-16 or base-26)")
        
        elif all(c.lower() in 'abcdefghijklmnopqrstuvwxyz ' for c in part):
            print("→ Appears to be alphabetic (substitution or hex encoding)")
            # Try hex section decoding
            results = SalphaseionSolver.decode_hex_section(part)
            print(f"Hex decode attempts:")
            for method, result in results.items():
                if result:
                    print(f"  {method}: {result[:100]}")
        
        elif any(c in part for c in '+/='):
            print("→ Appears to be Base64")
        
        else:
            print("→ Unknown encoding type")
            # Show character distribution
            char_freq = {}
            for c in part:
                if c != ' ':
                    char_freq[c] = char_freq.get(c, 0) + 1
            top_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            print(f"Top characters: {top_chars}")

def test_password_candidates(cosmic_duality_b64: str, candidates: list):
    """Test candidate passwords for Cosmic Duality"""
    
    print("\n" + "="*80)
    print("TESTING PASSWORD CANDIDATES FOR COSMIC DUALITY")
    print("="*80)
    
    for i, candidate in enumerate(candidates, 1):
        # Try both raw and hashed
        for variant in [candidate, hashlib.sha256(candidate.encode()).hexdigest()]:
            print(f"\nCandidate {i}a (raw): {candidate[:50]}...")
            print(f"Candidate {i}b (SHA256): {variant[:50]}...")
            
            # We can't actually decrypt without openssl, but we can provide the command
            print(f"  OpenSSL command:")
            print(f"    echo '{cosmic_duality_b64[:50]}...' | \\")
            print(f"    openssl enc -aes-256-cbc -d -a -pass pass:'{variant}'")

if __name__ == '__main__':
    # Example usage
    print("GSMG PUZZLE SOLVER - EXTRACTION TOOLS")
    print()
    
    # Test data
    test_abba = "abbabbababbaaaaabaabbbbabaaabbbaababbabaaababbbbaaaaaabbbaabbabbabbabababbaabbababbabbbabaaf"
    test_hex = "agdafaohaeiecggchgicbbhcgbehcfcoabicfdhhcdbcacagbdaiobbbgbeadeddecfobfdhdgdobdgoooiiigdocdaoofidfh"
    
    print("TEST 1: ABBA Decoding")
    print("-"*80)
    abba_result = SalphaseionSolver.decode_abba(test_abba)
    print(f"Input: {test_abba[:50]}...")
    print(f"Output: {abba_result}")
    
    print("\nTEST 2: Hex Section Decoding")
    print("-"*80)
    hex_results = SalphaseionSolver.decode_hex_section(test_hex)
    print(f"Input: {test_hex[:50]}...")
    for method, result in hex_results.items():
        if result:
            print(f"{method}: {result[:100]}")
    
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    print("""
To use with actual puzzle content:
1. Save Salphaseion HTML to file
2. Run this script with the HTML content
3. Analyze each section
4. Test password candidates on Cosmic Duality
    """)

