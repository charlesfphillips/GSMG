#!/bin/bash

# GSMG Puzzle - Final Password Test
# Test the most promising candidates

echo "Testing passwords on cosmic_duality_content.txt"
echo ""

# Most likely candidates
PASSWORDS=(
    "causality"
    "matrixsumlist"
    "thematrixhasyou"
    "theone"
    "turing_complete"
    "matrixsumlistenter"
    "women"
    "half"
    "betterhalf"
	"&"
	"enter"
)

for pwd in "${PASSWORDS[@]}"; do
    echo "Testing: $pwd"
    
    # Try with -md sha256 first
    openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt \
        -pass pass:"$pwd" -md sha256 -out "test_${pwd}.bin" 2>/dev/null
    
    if [ -f "test_${pwd}.bin" ]; then
        SIZE=$(wc -c < "test_${pwd}.bin")
        
        if [ "$SIZE" -eq 1343 ]; then
            echo "  ✓✓✓ SUCCESS! File is 1343 bytes"
            echo "  Password: $pwd"
            
            # Extract K1 and K2
            python3 << PYEOF
import binascii
with open('test_${pwd}.bin', 'rb') as f:
    data = f.read()
K1 = binascii.hexlify(data[0:32]).decode()
K2 = binascii.hexlify(data[671:703]).decode()
print(f"K1: {K1}")
print(f"K2: {K2}")
PYEOF
            exit 0
        else
            rm "test_${pwd}.bin"
        fi
    fi
done

echo ""
echo "No passwords produced 1343 bytes with -md sha256"
echo ""
echo "Trying again with different digest options..."
echo ""

# Try with default digest (MD5)
for pwd in "${PASSWORDS[@]}"; do
    echo "Testing (MD5): $pwd"
    
    openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt \
        -pass pass:"$pwd" -out "test_${pwd}_md5.bin" 2>/dev/null
    
    if [ -f "test_${pwd}_md5.bin" ]; then
        SIZE=$(wc -c < "test_${pwd}_md5.bin")
        
        if [ "$SIZE" -eq 1343 ]; then
            echo "  ✓✓✓ SUCCESS! File is 1343 bytes"
            echo "  Password: $pwd (with MD5)"
            
            # Extract K1 and K2
            python3 << PYEOF
import binascii
with open('test_${pwd}_md5.bin', 'rb') as f:
    data = f.read()
K1 = binascii.hexlify(data[0:32]).decode()
K2 = binascii.hexlify(data[671:703]).decode()
print(f"K1: {K1}")
print(f"K2: {K2}")
PYEOF
            exit 0
        else
            rm "test_${pwd}_md5.bin"
        fi
    fi
done

echo ""
echo "Still no match. Try running with -pbkdf2:"
echo ""
echo "for pwd in causality matrixsumlist thematrixhasyou theone; do"
echo "  openssl enc -aes-256-cbc -d -a -pbkdf2 -in cosmic_duality_content.txt -pass pass:\"\$pwd\" -out test_\$pwd.bin"
echo "done"