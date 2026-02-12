#!/bin/bash

# Comprehensive password cracking for cosmic_duality_content.txt
# Run this in your bash terminal

cd /c/Temp/Mini_Puzzle/Final_Push

echo ""
echo "===================================================================="
echo "COSMIC DUALITY PASSWORD CRACKING"
echo "===================================================================="
echo ""
echo "File: cosmic_duality_content.txt"
echo "Format: OpenSSL enc'd data with salted password, base64 encoded"
echo "Target: Find password that produces file size != 1312 bytes"
echo ""

# Extended password list based on puzzle clues
passwords=(
    # From previous puzzle phases
    "matrixsumlist"
    "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5"
    "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c"
    
    # Basic candidates
    "HALFANDBETTERHALF"
    "halfandbetterhalf"
    "THEMATRIXHASYOU"
    "thematrixhasyou"
    "PRIVATEKEYS"
    "privatekeys"
    "COSMICDUALITY"
    "cosmicduality"
    "PUZZLE"
    "puzzle"
    "COSMIC"
    "cosmic"
    
    # Phrase variations
    "HALF AND BETTER HALF"
    "THE MATRIX HAS YOU"
    "PRIVATE KEYS"
    "COSMIC DUALITY"
    
    # Numbers and combinations
    "123456"
    "password"
    "bitcoin"
    "satoshi"
    "ernestcline"
    "jaquefrescoo"
    "jacque fresco"
    
    # From puzzle phases
    "Phase3"
    "phase3"
    "PHASE3"
    "Phase3.1"
    "phase3.1"
    
    # Common variants
    ""
    "a"
    "0"
    
    # Matrix/Cinema references
    "THEMATRIX"
    "thematrix"
    "NEO"
    "neo"
    "MORPHEUS"
    "morpheus"
    "ENTER"
    "enter"
    
    # Bitcoin/Crypto
    "BITCOIN"
    "bitcoin"
    "ETHEREUM"
    "ethereum"
    "SATOSHI"
    "satoshi"
    
    # Puzzle-specific
    "GSMG"
    "gsmg"
    "COSMICPUZZLE"
    "cosmicpuzzle"
    "HALF"
    "half"
    "BETTER"
    "better"
    
    # Try with different cases/separators
    "half-and-better-half"
    "HALF-AND-BETTER-HALF"
    "half_and_better_half"
    "HALF_AND_BETTER_HALF"
)

echo "Testing ${#passwords[@]} passwords..."
echo ""

found=0
tested=0

for pwd in "${passwords[@]}"; do
    tested=$((tested + 1))
    
    # Skip empty passwords or very long ones (likely not the answer)
    if [ -z "$pwd" ] || [ ${#pwd} -gt 80 ]; then
        continue
    fi
    
    # Test decryption
    openssl enc -aes-256-cbc -d -a \
        -in cosmic_duality_content.txt \
        -pass pass:"$pwd" \
        -md sha256 \
        -out temp_test.bin 2>/dev/null
    
    # Check file size
    size=$(wc -c < temp_test.bin 2>/dev/null)
    
    if [ -n "$size" ] && [ "$size" != "1312" ]; then
        echo "✓ FOUND! Password: '$pwd'"
        echo "  File size: $size bytes"
        echo "  Show first 32 bytes:"
        od -An -tx1 -N32 temp_test.bin
        echo ""
        found=1
        break
    fi
    
    # Progress indicator
    if [ $((tested % 10)) -eq 0 ]; then
        echo "  Tested $tested passwords... (current: ${pwd:0:30})"
    fi
done

rm -f temp_test.bin

echo ""
if [ $found -eq 0 ]; then
    echo "Password not found in the list."
    echo ""
    echo "Try these commands to test specific passwords:"
    echo ""
    echo "# Test with -pbkdf2"
    echo "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -pass pass:PASSWORD -pbkdf2 -out test.bin"
    echo "wc -c test.bin"
    echo ""
    echo "# Test with -md MD5"
    echo "openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -pass pass:PASSWORD -md MD5 -out test.bin"
    echo "wc -c test.bin"
    echo ""
    echo "Common passwords to try manually:"
    echo "  - Any text from the puzzle document"
    echo "  - Bitcoin addresses or hashes"
    echo "  - Names of people referenced"
    echo "  - Words from the puzzle story"
fi

echo ""
echo "===================================================================="