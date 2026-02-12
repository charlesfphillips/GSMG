#!/usr/bin/env python3
"""
GSMG Duality Puzzle Solver
Combines k1 and k2 to find the final private key
"""

import hashlib
import sys

# secp256k1 parameters
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def hex_to_int(hex_str):
    """Convert hex string to integer"""
    return int(hex_str, 16)

def int_to_hex(num):
    """Convert integer to 64-character hex string"""
    return format(num, '064x')

def wif_encode(private_key_hex):
    """Encode private key to WIF format"""
    BASE58_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    def base58_encode(data):
        num = int.from_bytes(data, 'big')
        leading_zeros = len(data) - len(data.lstrip(b'\x00'))
        encoded = b''
        while num > 0:
            num, remainder = divmod(num, 58)
            encoded = bytes([BASE58_ALPHABET[remainder]]) + encoded
        return b'1' * leading_zeros + encoded
    
    private_key_bytes = bytes.fromhex(private_key_hex)
    
    # Uncompressed WIF
    wif_data = b'\x80' + private_key_bytes
    checksum = hashlib.sha256(hashlib.sha256(wif_data).digest()).digest()[:4]
    wif_uncompressed = base58_encode(wif_data + checksum).decode()
    
    # Compressed WIF
    wif_data_c = b'\x80' + private_key_bytes + b'\x01'
    checksum_c = hashlib.sha256(hashlib.sha256(wif_data_c).digest()).digest()[:4]
    wif_compressed = base58_encode(wif_data_c + checksum_c).decode()
    
    return wif_uncompressed, wif_compressed

def solve_duality(k1_hex, k2_hex, method='add'):
    """
    Solve the duality puzzle
    
    Args:
        k1_hex: First key (hex string)
        k2_hex: Second key (hex string)
        method: 'add' for (k1 + k2) mod n, 'sub' for (k1 - k2) mod n
    
    Returns:
        tuple: (ktarget_hex, wif_uncompressed, wif_compressed)
    """
    k1 = hex_to_int(k1_hex)
    k2 = hex_to_int(k2_hex)
    
    if method == 'add':
        ktarget = (k1 + k2) % n
        print(f"\n[Addition Method]")
        print(f"ktarget = (k1 + k2) mod n")
    else:  # sub
        ktarget = (k1 - k2) % n
        print(f"\n[Subtraction Method]")
        print(f"ktarget = (k1 - k2) mod n")
    
    ktarget_hex = int_to_hex(ktarget)
    wif_uncompressed, wif_compressed = wif_encode(ktarget_hex)
    
    print(f"\nk1: {k1_hex}")
    print(f"k2: {k2_hex}")
    print(f"\nktarget (hex): {ktarget_hex}")
    print(f"ktarget (int): {ktarget}")
    print(f"\nWIF Uncompressed: {wif_uncompressed}")
    print(f"WIF Compressed:   {wif_compressed}")
    
    return ktarget_hex, wif_uncompressed, wif_compressed

if __name__ == "__main__":
    print("="*80)
    print("GSMG DUALITY PUZZLE SOLVER")
    print("="*80)
    
    # k1 from our decryption
    k1 = "c8956d4ac326eac2d510bc4748d1cd9d898f1f55fc2e38494e228aa77eb88b67"
    
    if len(sys.argv) > 1:
        k2 = sys.argv[1]
        
        print(f"\nk1: {k1}")
        print(f"k2: {k2}")
        
        # Try both methods
        print("\n" + "="*80)
        print("METHOD 1: Addition (k1 + k2) mod n")
        print("="*80)
        ktarget_add, wif_unc_add, wif_comp_add = solve_duality(k1, k2, 'add')
        
        print("\n" + "="*80)
        print("METHOD 2: Subtraction (k1 - k2) mod n")
        print("="*80)
        ktarget_sub, wif_unc_sub, wif_comp_sub = solve_duality(k1, k2, 'sub')
        
        print("\n" + "="*80)
        print("RESULTS")
        print("="*80)
        print(f"""
Try importing these keys into Electrum and check which one has 2.5 BTC:

METHOD 1 - ADDITION:
  Uncompressed: {wif_unc_add}
  Compressed:   {wif_comp_add}

METHOD 2 - SUBTRACTION:
  Uncompressed: {wif_unc_sub}
  Compressed:   {wif_comp_sub}

The correct one should unlock 1GSMG1JCHXNstXW39VpS9iVfM9P6P7B3P with 2.5 BTC!
""")
    else:
        print(f"""
Usage: python3 DUALITY_SOLVER.py <k2_hex>

Where:
  k1 = {k1}
  k2 = your second key from blockchain dust transaction (64 hex characters)

Example:
  python3 DUALITY_SOLVER.py d353548d1007c81ad1f1601a6c46677c96ccaf0d2a4067e65d0355b1fb07ddf8

The script will calculate both:
  - ktarget = (k1 + k2) mod n
  - ktarget = (k1 - k2) mod n

And generate WIF keys for both methods.
""")

