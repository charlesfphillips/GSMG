#!/bin/bash

# Test passwords against cosmic_duality_content.txt in bash
# Save as: test_passwords.sh
# Run: bash test_passwords.sh

cd /c/Temp/Mini_Puzzle/Final_Push

echo ""
echo "===================================================================="
echo "TESTING PASSWORDS WITH DIFFERENT DIGEST METHODS"
echo "===================================================================="
echo ""

INPUT="cosmic_duality_content.txt"

echo "Testing with -pbkdf2 method..."
echo ""

# Test 1
echo "[1] Testing HALFANDBETTERHALF with -pbkdf2"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:HALFANDBETTERHALF -pbkdf2 -out r1.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r1.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

# Test 2
echo "[2] Testing THEMATRIXHASYOU with -pbkdf2"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:THEMATRIXHASYOU -pbkdf2 -out r2.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r2.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

# Test 3
echo "[3] Testing PRIVATEKEYS with -pbkdf2"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:PRIVATEKEYS -pbkdf2 -out r3.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r3.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

# Test 4
echo "[4] Testing COSMICDUALITY with -pbkdf2"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:COSMICDUALITY -pbkdf2 -out r4.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r4.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

# Test 5
echo "[5] Testing PUZZLE with -pbkdf2"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:PUZZLE -pbkdf2 -out r5.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r5.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

echo "===================================================================="
echo "Testing with -md MD5 method..."
echo "===================================================================="
echo ""

# Test 6
echo "[6] Testing HALFANDBETTERHALF with -md MD5"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:HALFANDBETTERHALF -md MD5 -out r6.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r6.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

# Test 7
echo "[7] Testing THEMATRIXHASYOU with -md MD5"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:THEMATRIXHASYOU -md MD5 -out r7.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r7.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

# Test 8
echo "[8] Testing PRIVATEKEYS with -md MD5"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:PRIVATEKEYS -md MD5 -out r8.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r8.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

# Test 9
echo "[9] Testing COSMICDUALITY with -md MD5"
openssl enc -aes-256-cbc -d -a -in "$INPUT" -pass pass:COSMICDUALITY -md MD5 -out r9.bin 2>&1 | grep -v WARNING
SIZE=$(wc -c < r9.bin)
echo "    Result: $SIZE bytes"
if [ "$SIZE" != "1312" ]; then
    echo "    *** DIFFERENT SIZE - POSSIBLE SUCCESS! ***"
fi
echo ""

echo "===================================================================="
echo "SUMMARY"
echo "===================================================================="
echo ""
echo "Check which file is NOT 1312 bytes:"
ls -lh r*.bin | awk '{print $9, $5}'
echo ""
echo "If any file is different, run:"
echo "  od -An -tx1 -N64 r1.bin  (or whichever file had different size)"
echo ""