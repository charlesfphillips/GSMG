#!/usr/bin/env python3
"""
Comprehensive Password Testing for GSMG Cosmic Duality
Run from: C:\Temp\Mini_Puzzle\Final_Push
Usage: python comprehensive_password_test.py
"""

import subprocess
import os
import sys
import binascii

def is_likely_valid_decryption(file_path):
    """Check if decrypted file looks valid (not garbage or still encrypted)"""
    try:
        with open(file_path, 'rb') as f:
            first_16 = f.read(16)
        
        if len(first_16) < 4:
            return False, "File too small"
        
        # Check for "Salted__" header (still encrypted)
        if first_16.startswith(b'Salted__'):
            return False, "Still encrypted (Salted__ header)"
        
        # Check if it's pure garbage (all same byte pattern like our earlier 'aa' test)
        if len(set(first_16[:8])) < 3:
            return False, "Garbage pattern detected"
        
        # If we get here, might be valid
        header_hex = binascii.hexlify(first_16).decode()
        return True, f"Potentially valid! Header: {header_hex}"
        
    except Exception as e:
        return False, f"Read error: {e}"

def test_passwords():
    """Test all password candidates"""
    
    passwords = [
        # From Phase 3.2 decoded message
        "HALFANDBETTERHALF",
        "halfandbetterhalf",
        "HALF AND BETTER HALF",
        "half and better half",
        
        # Variations with "THE"
        "THEPRIVATEKEYSBELONGTOHALFANDBETTERHALF",
        "theprivatekeysbelongtohalfandbetterhalf",
        "THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF",
        
        # Just key phrases
        "PRIVATEKEYS",
        "privatekeys",
        "PRIVATE KEYS",
        "private keys",
        
        # From Beaufort cipher
        "THEMATRIXHASYOU",
        "thematrixhasyou",
        "THE MATRIX HAS YOU",
        "the matrix has you",
        
        # From Phase 3.0
        "CAUSALITY",
        "causality",
        
        # Combinations
        "HALF",
        "BETTERHALF",
        "better half",
        "FUNDS",
        "funds",
        
        # Key words from message
        "UNBALANCED",
        "unbalanced",
        "EQUATION",
        "equation",
        "REMAINDER",
        "remainder",
        
        # Try with underscores/dashes
        "HALF_AND_BETTER_HALF",
        "half_and_better_half",
        "HALF-AND-BETTER-HALF",
        "half-and-better-half",
        
        # Numbers from Phase 3.2
        "15165943121972409169171213758951813",
        
        # Try "cosmic" related
        "COSMIC",
        "cosmic",
        "DUALITY",
        "duality",
        "COSMICDUALITY",
        "cosmicduality",
        
        # Matrix references
        "NEO",
        "neo",
        "MORPHEUS",
        "morpheus",
        "ENTER",
        "enter",
        "MATRIX",
        "matrix",
        
        # Additional attempts
        "SAFENET",
        "safenet",
        "LUNA",
        "luna",
        "HSM",
        "hsm",
        "PUZZLE",
        "puzzle",
    ]
    
    input_file = "cosmic_duality_content.txt"
    
    if not os.path.exists(input_file):
        print(f"ERROR: {input_file} not found!")
        print(f"Current directory: {os.getcwd()}")
        print(f"Files present: {os.listdir('.')[:10]}")
        sys.exit(1)
    
    print("="*80)
    print("COMPREHENSIVE PASSWORD TESTING - COSMIC DUALITY DECRYPTION")
    print("="*80)
    print(f"\nInput file: {input_file}")
    print(f"Testing {len(passwords)} password candidates...\n")
    
    successful = []
    suspicious = []
    failed = 0
    
    for i, pwd in enumerate(passwords, 1):
        output_file = f"test_output_{i:03d}.bin"
        
        # Test with -md sha256
        cmd = [
            'openssl', 'enc', '-aes-256-cbc', '-d', '-a',
            '-in', input_file,
            '-pass', f'pass:{pwd}',
            '-md', 'sha256',
            '-out', output_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                
                # Analyze the file
                is_valid, analysis = is_likely_valid_decryption(output_file)
                
                if is_valid:
                    successful.append((pwd, file_size, output_file, analysis))
                    print(f"✓ [{i:2d}] '{pwd}' → {file_size:4d} bytes - {analysis}")
                else:
                    suspicious.append((pwd, file_size, output_file, analysis))
                    print(f"? [{i:2d}] '{pwd}' → {file_size:4d} bytes - {analysis}")
                    failed += 1
            else:
                failed += 1
                print(f"✗ [{i:2d}] '{pwd}' → File not created")
                
        except subprocess.TimeoutExpired:
            print(f"✗ [{i:2d}] '{pwd}' → Timeout")
            failed += 1
        except Exception as e:
            print(f"✗ [{i:2d}] '{pwd}' → Error: {e}")
            failed += 1
    
    print("\n" + "="*80)
    print(f"RESULTS: {len(successful)} successful, {len(suspicious)} suspicious, {failed} failed")
    print("="*80)
    
    if successful:
        print("\n🎉 SUCCESSFUL DECRYPTIONS:\n")
        for pwd, size, output_file, analysis in successful:
            print(f"  Password: '{pwd}'")
            print(f"  File: {output_file} ({size} bytes)")
            print(f"  Analysis: {analysis}")
            print()
            
            # Show hex dump of first 32 bytes
            with open(output_file, 'rb') as f:
                data = f.read(32)
                hex_str = ' '.join(f'{b:02x}' for b in data)
                print(f"  First 32 bytes: {hex_str}")
            print()
    
    if suspicious:
        print("\n⚠️  SUSPICIOUS (might still be valid):\n")
        for pwd, size, output_file, analysis in suspicious[:5]:  # Show top 5
            print(f"  Password: '{pwd}'")
            print(f"  File: {output_file} ({size} bytes)")
            print(f"  Analysis: {analysis}")
            print()
    
    print("\nNEXT STEPS:")
    if successful:
        print("1. Examine the decrypted file(s) above")
        print("2. Check if first 32 bytes are valid secp256k1 coordinates")
        print("3. Test transformation formulas")
    else:
        print("1. Try -pbkdf2 digest method")
        print("2. Try with -iter parameter")
        print("3. Check Salphaseion grid for hidden password")
        print("4. Review GitHub issues for additional clues")

if __name__ == "__main__":
    test_passwords()