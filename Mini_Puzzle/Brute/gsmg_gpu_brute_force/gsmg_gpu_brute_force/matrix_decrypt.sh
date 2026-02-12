#!/bin/bash

FILE="cosmic_raw.bin"

# These are the specific "Matrix" combinations found in your notes
CANDIDATES=(
    "causality"
    "matrixsumlist"
    "thematrixhasyou"
    "matrixsumlistenterlastwordsbeforearchichoicethispassword"
    "matrixsumlist_enter_lastwordsbeforearchichoic_thispassword"
    "causalitySafenetLunaHSM11110"
    "matrixsumlistenter"
    "theone"
)

echo "--- Starting Matrix Decryption Scan ---"

for PASS in "${CANDIDATES[@]}"; do
    # Try Legacy MD derivation
    echo -n "Testing Legacy: [$PASS] ... "
    if openssl enc -aes-256-cbc -d -in "$FILE" -pass pass:"$PASS" -md sha256 -out "dec_legacy.bin" 2>/dev/null; then
        echo "SUCCESS! Result in dec_legacy.bin"
        break
    else
        echo "failed."
    fi

    # Try PBKDF2 derivation (Newer OpenSSL standard)
    echo -n "Testing PBKDF2: [$PASS] ... "
    if openssl enc -aes-256-cbc -d -pbkdf2 -in "$FILE" -pass pass:"$PASS" -md sha256 -out "dec_pbkdf2.bin" 2>/dev/null; then
        echo "SUCCESS! Result in dec_pbkdf2.bin"
        break
    else
        echo "failed."
    fi
done