#!/usr/bin/env python3
"""
STEP 1: Extract Salphaseion and Cosmic Duality from HTML
"""
import re

print("="*70)
print("STEP 1: EXTRACT CONTENT FROM HTML")
print("="*70)

try:
    html = open('salphaseion.html', 'r').read()
    print("\n✓ Opened salphaseion.html")
except FileNotFoundError:
    print("\n✗ ERROR: salphaseion.html not found!")
    print("  Please save the HTML document as salphaseion.html in this folder")
    exit(1)

# Extract Salphaseion
print("\nExtracting SALPHASEION section...")
salph_match = re.search(r'<h1>\s*SalPhaseIon\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)

if salph_match:
    salphaseion = salph_match.group(1).strip()
    open('salphaseion_content.txt', 'w').write(salphaseion)
    print(f"✓ Extracted {len(salphaseion)} characters")
    print(f"  Preview: {salphaseion[:80]}...")
else:
    print("✗ Could not find SALPHASEION section")

# Extract Cosmic Duality
print("\nExtracting COSMIC DUALITY section...")
cosmic_match = re.search(r'<h1>\s*Cosmic Duality\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)

if cosmic_match:
    cosmic = cosmic_match.group(1).strip()
    open('cosmic_duality_content.txt', 'w').write(cosmic)
    print(f"✓ Extracted {len(cosmic)} characters")
    print(f"  Preview: {cosmic[:80]}...")
else:
    print("✗ Could not find COSMIC DUALITY section")

print("\n" + "="*70)
print("RESULT: Two files created")
print("  • salphaseion_content.txt - SALPHASEION raw content")
print("  • cosmic_duality_content.txt - COSMIC DUALITY encrypted blob")
print("="*70)
print("\nNext: Run 02_decode_abba.py")
