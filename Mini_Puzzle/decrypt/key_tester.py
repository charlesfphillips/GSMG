#!/usr/bin/env python3
"""
GSMG Puzzle Solver - Bitcoin Key Address Tester
Tests private keys and generates Bitcoin addresses to find the target
"""

import hashlib
import binascii
import sys

# Try to import ecdsa - if not available, provide fallback
try:
    import ecdsa
    from ecdsa import SigningKey, NIST256p
    ECDSA_AVAILABLE = True
except ImportError:
    ECDSA_AVAILABLE = False
    print("⚠️  WARNING: ecdsa library not found")
    print("   Install with: pip install ecdsa")
    print("   Continuing with WIF generation only...\n")

TARGET_ADDRESS = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

def base58_decode(s):
    """Decode base58 string"""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    decoded = 0
    for char in s:
        decoded = decoded * 58 + alphabet.index(char)
    return decoded

def base58_encode(num):
    """Encode number to base58"""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    encoded = ''
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = alphabet[remainder] + encoded
    return encoded

def private_key_to_address(private_key_hex, compressed=False):
    """
    Convert hex private key to Bitcoin address (uncompressed or compressed)
    Returns the address or error message
    """
    if not ECDSA_AVAILABLE:
        return None  # Can't generate address without ecdsa
    
    try:
        # Convert hex to bytes
        key_bytes = bytes.fromhex(private_key_hex.zfill(64))
        
        # Create ECDSA signing key
        sk = ecdsa.SigningKey.from_string(key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        
        # Get public key coordinates
        public_key_bytes = vk.to_string()
        
        if compressed:
            # Compressed format: prefix + x coordinate
            y_last_byte = public_key_bytes[32 * 2 - 1]
            prefix = b'\x03' if (y_last_byte & 1) else b'\x02'
            public_key_bytes = prefix + public_key_bytes[:32]
        else:
            # Uncompressed format: 04 + x + y
            public_key_bytes = b'\x04' + public_key_bytes
        
        # Hash public key: SHA256 then RIPEMD160
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        
        # RIPEMD160
        h = hashlib.new('ripemd160')
        h.update(sha256_hash)
        hash160 = h.digest()
        
        # Add version byte (0x00 for mainnet P2PKH)
        versioned = b'\x00' + hash160
        
        # Calculate checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        
        # Base58 encode
        address_bytes = versioned + checksum
        address_int = int.from_bytes(address_bytes, 'big')
        
        address = ''
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        while address_int > 0:
            address_int, remainder = divmod(address_int, 58)
            address = alphabet[remainder] + address
        
        # Add leading '1' for each leading zero byte
        for byte in address_bytes:
            if byte == 0:
                address = '1' + address
            else:
                break
        
        return address
    
    except Exception as e:
        return f"Error: {str(e)}"

def hex_to_wif(hex_key, compressed=False):
    """Convert hex private key to WIF format"""
    # Add version byte (0x80 for mainnet)
    extended = "80" + hex_key.zfill(64)
    
    if compressed:
        extended += "01"
    
    # Double SHA256 for checksum
    first_sha = hashlib.sha256(bytes.fromhex(extended)).digest()
    second_sha = hashlib.sha256(first_sha).digest()
    checksum = second_sha[:4].hex()
    
    final_hex = extended + checksum
    
    # Base58 encode
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    decoded_int = int(final_hex, 16)
    wif = ''
    while decoded_int:
        decoded_int, remainder = divmod(decoded_int, 58)
        wif = alphabet[remainder] + wif
    
    return wif or alphabet[0]

def test_keys_from_file(binary_file_path, target_addr=TARGET_ADDRESS):
    """Test all 32-byte keys from a binary file"""
    
    try:
        with open(binary_file_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{binary_file_path}' not found")
        return None
    
    print("=" * 100)
    print(f"GSMG PUZZLE KEY TESTER")
    print("=" * 100)
    print(f"\nTarget Address: {target_addr}")
    print(f"File: {binary_file_path} ({len(data)} bytes)")
    print(f"Extracting 32-byte keys...")
    
    results = []
    key_num = 0
    
    for offset in range(0, len(data) - 31, 32):
        key_num += 1
        chunk = data[offset:offset+32]
        hex_key = binascii.hexlify(chunk).decode()
        
        # Generate WIFs
        wif_uncompressed = hex_to_wif(hex_key, compressed=False)
        wif_compressed = hex_to_wif(hex_key, compressed=True)
        
        # Try to generate addresses if ecdsa available
        addr_uncompressed = None
        addr_compressed = None
        
        if ECDSA_AVAILABLE:
            addr_uncompressed = private_key_to_address(hex_key, compressed=False)
            addr_compressed = private_key_to_address(hex_key, compressed=True)
        
        result = {
            'key_num': key_num,
            'hex': hex_key,
            'wif_u': wif_uncompressed,
            'wif_c': wif_compressed,
            'addr_u': addr_uncompressed,
            'addr_c': addr_compressed,
            'match_u': addr_uncompressed == target_addr if addr_uncompressed else False,
            'match_c': addr_compressed == target_addr if addr_compressed else False,
        }
        
        results.append(result)
    
    print(f"\nFound {len(results)} candidate keys\n")
    
    # Display results
    if ECDSA_AVAILABLE:
        print("=" * 100)
        print(f"{'Key':<4} {'Uncompressed Address':<35} {'Compressed Address':<35} {'Match':<6}")
        print("=" * 100)
        
        for r in results:
            addr_u = r['addr_u'][:35] if r['addr_u'] else "ERROR"
            addr_c = r['addr_c'][:35] if r['addr_c'] else "ERROR"
            match = "✓ YES!" if r['match_u'] or r['match_c'] else ""
            
            print(f"{r['key_num']:<4} {addr_u:<35} {addr_c:<35} {match:<6}")
    
    print("\n" + "=" * 100)
    print("DETAILS")
    print("=" * 100)
    
    found_match = False
    
    for r in results:
        print(f"\nKey {r['key_num']}:")
        print(f"  Hex: {r['hex']}")
        print(f"  WIF (Uncompressed): {r['wif_u']}")
        print(f"  WIF (Compressed):   {r['wif_c']}")
        
        if ECDSA_AVAILABLE:
            print(f"  Address (Uncompressed): {r['addr_u']}")
            print(f"  Address (Compressed):   {r['addr_c']}")
            
            if r['match_u']:
                print(f"  ✓✓✓ UNCOMPRESSED MATCH! ✓✓✓")
                found_match = True
            if r['match_c']:
                print(f"  ✓✓✓ COMPRESSED MATCH! ✓✓✓")
                found_match = True
    
    print("\n" + "=" * 100)
    
    if found_match:
        print("🎉 SUCCESS! FOUND THE MATCHING KEY! 🎉")
    else:
        if not ECDSA_AVAILABLE:
            print("⚠️  No ecdsa library - addresses not generated")
            print("    Install ecdsa to verify addresses: pip install ecdsa")
        else:
            print("❌ No matching address found")
    
    print("=" * 100)
    
    return results

def main():
    """Main function"""
    if len(sys.argv) > 1:
        binary_file = sys.argv[1]
    else:
        # Default to decrypted.bin in current directory
        binary_file = 'decrypted.bin'
    
    results = test_keys_from_file(binary_file)
    
    if results:
        # If no ecdsa, provide WIFs for manual testing
        if not ECDSA_AVAILABLE:
            print("\n" + "=" * 100)
            print("NO ECDSA LIBRARY - WIFs FOR MANUAL TESTING")
            print("=" * 100)
            print("\nTest these WIFs at: https://www.bitaddress.org")
            print("1. Paste the WIF")
            print("2. Check if Uncompressed Address matches: " + TARGET_ADDRESS)
            print()
            
            for r in results:
                print(f"Key {r['key_num']}: {r['wif_u']}")

if __name__ == '__main__':
    main()