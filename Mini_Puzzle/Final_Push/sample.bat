@echo off
setlocal enabledelayedexpansion

cls
echo.
echo ====================================================================
echo TESTING PASSWORDS WITH ALTERNATIVE DIGEST METHODS
echo ====================================================================
echo.

set "INPUT=cosmic_duality_content.txt"

echo Testing with -pbkdf2...
echo.

echo [1/10] Testing HALFANDBETTERHALF with -pbkdf2
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:HALFANDBETTERHALF -pbkdf2 -out test_pbkdf2_1.bin 2>nul
for %%A in (test_pbkdf2_1.bin) do echo     Result: %%~zA bytes
echo.

echo [2/10] Testing halfandbetterhalf with -pbkdf2
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:halfandbetterhalf -pbkdf2 -out test_pbkdf2_2.bin 2>nul
for %%A in (test_pbkdf2_2.bin) do echo     Result: %%~zA bytes
echo.

echo [3/10] Testing THEPRIVATEKEYSBELONGTOHALFANDBETTERHALF with -pbkdf2
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:THEPRIVATEKEYSBELONGTOHALFANDBETTERHALF -pbkdf2 -out test_pbkdf2_3.bin 2>nul
for %%A in (test_pbkdf2_3.bin) do echo     Result: %%~zA bytes
echo.

echo [4/10] Testing THEMATRIXHASYOU with -pbkdf2
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:THEMATRIXHASYOU -pbkdf2 -out test_pbkdf2_4.bin 2>nul
for %%A in (test_pbkdf2_4.bin) do echo     Result: %%~zA bytes
echo.

echo [5/10] Testing PRIVATEKEYS with -pbkdf2
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:PRIVATEKEYS -pbkdf2 -out test_pbkdf2_5.bin 2>nul
for %%A in (test_pbkdf2_5.bin) do echo     Result: %%~zA bytes
echo.

echo ====================================================================
echo Testing with -md MD5...
echo ====================================================================
echo.

echo [1/5] Testing HALFANDBETTERHALF with -md MD5
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:HALFANDBETTERHALF -md MD5 -out test_md5_1.bin 2>nul
for %%A in (test_md5_1.bin) do echo     Result: %%~zA bytes
echo.

echo [2/5] Testing THEMATRIXHASYOU with -md MD5
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:THEMATRIXHASYOU -md MD5 -out test_md5_2.bin 2>nul
for %%A in (test_md5_2.bin) do echo     Result: %%~zA bytes
echo.

echo [3/5] Testing PRIVATEKEYS with -md MD5
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:PRIVATEKEYS -md MD5 -out test_md5_3.bin 2>nul
for %%A in (test_md5_3.bin) do echo     Result: %%~zA bytes
echo.

echo [4/5] Testing COSMICDUALITY with -md MD5
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:COSMICDUALITY -md MD5 -out test_md5_4.bin 2>nul
for %%A in (test_md5_4.bin) do echo     Result: %%~zA bytes
echo.

echo [5/5] Testing PUZZLE with -md MD5
openssl enc -aes-256-cbc -d -a -in %INPUT% -pass pass:PUZZLE -md MD5 -out test_md5_5.bin 2>nul
for %%A in (test_md5_5.bin) do echo     Result: %%~zA bytes
echo.

echo ====================================================================
echo CHECKING RESULTS
echo ====================================================================
echo.
echo Files that are NOT 1312 bytes (possible success):
echo.

for %%F in (test_pbkdf2_*.bin test_md5_*.bin) do (
    for %%S in (%%F) do (
        if not !SIZE!==1312 (
            echo Found: %%F - %%~zA bytes
        )
    )
)

echo.
echo If you see a file above that is not 1312 bytes, that password worked!
echo.
echo To view the decrypted content:
echo   Format-Hex -Path 'test_pbkdf2_1.bin' -Count 128
echo   or
echo   Get-Content 'test_pbkdf2_1.bin' -Encoding UTF8
echo.
pause