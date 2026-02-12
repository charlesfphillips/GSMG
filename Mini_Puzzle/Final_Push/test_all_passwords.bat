@echo off
REM Comprehensive Password Testing for Cosmic Duality
REM Save this as: test_all_passwords.bat
REM Run from: C:\Temp\Mini_Puzzle\Final_Push
REM Usage: test_all_passwords.bat

setlocal enabledelayedexpansion
cls

echo ================================================================================
echo COMPREHENSIVE PASSWORD TESTING - COSMIC DUALITY DECRYPTION
echo ================================================================================
echo.

set INPUT_FILE=cosmic_duality_content.txt
set COUNTER=0
set SUCCESS_COUNT=0

REM Define all password candidates
set "passwords[0]=HALFANDBETTERHALF"
set "passwords[1]=halfandbetterhalf"
set "passwords[2]=THEMATRIXHASYOU"
set "passwords[3]=thematrixhasyou"
set "passwords[4]=PRIVATEKEYS"
set "passwords[5]=privatekeys"
set "passwords[6]=THEPRIVATEKEYSBELONGTOHALFANDBETTERHALF"
set "passwords[7]=theprivatekeysbelongtohalfandbetterhalf"
set "passwords[8]=HALF"
set "passwords[9]=BETTERHALF"
set "passwords[10]=CAUSALITY"
set "passwords[11]=causality"
set "passwords[12]=COSMIC"
set "passwords[13]=cosmic"
set "passwords[14]=DUALITY"
set "passwords[15]=duality"
set "passwords[16]=COSMICDUALITY"
set "passwords[17]=cosmicduality"
set "passwords[18]=UNBALANCED"
set "passwords[19]=unbalanced"
set "passwords[20]=EQUATION"
set "passwords[21]=equation"
set "passwords[22]=REMAINDER"
set "passwords[23]=remainder"
set "passwords[24]=ENTER"
set "passwords[25]=enter"
set "passwords[26]=NEO"
set "passwords[27]=neo"
set "passwords[28]=MORPHEUS"
set "passwords[29]=morpheus"
set "passwords[30]=FUNDS"
set "passwords[31]=funds"
set "passwords[32]=15165943121972409169171213758951813"
set "passwords[33]=MATRIX"
set "passwords[34]=matrix"
set "passwords[35]=SAFENET"
set "passwords[36]=safenet"
set "passwords[37]=LUNA"
set "passwords[38]=luna"
set "passwords[39]=HSM"
set "passwords[40]=hsm"
set "passwords[41]=HALF_AND_BETTER_HALF"
set "passwords[42]=half_and_better_half"
set "passwords[43]=PRIVATE_KEYS"
set "passwords[44]=private_keys"
set "passwords[45]=THE_MATRIX_HAS_YOU"
set "passwords[46]=the_matrix_has_you"
set "passwords[47]=PUZZLE"
set "passwords[48]=puzzle"
set "passwords[49]=BITCOINCOMMUNITY"
set "passwords[50]=bitcoincommunity"

echo Testing passwords with -md sha256...
echo.

REM Test each password
:loop
if defined passwords[%COUNTER%] (
    set "PWD=!passwords[%COUNTER%]!"
    set /a COUNTER+=1
    
    REM Run openssl with -md sha256
    openssl enc -aes-256-cbc -d -a -in %INPUT_FILE% -pass pass:"!PWD!" -md sha256 -out test_!COUNTER!.bin 2>nul
    
    REM Check if file was created
    if exist test_!COUNTER!.bin (
        for %%A in (test_!COUNTER!.bin) do set SIZE=%%~zA
        
        REM Check first 4 bytes to see if it looks like valid data (not "Salted__")
        for /f "tokens=*" %%B in ('powershell -Command "Get-Content test_!COUNTER!.bin -Encoding Byte -ReadCount 4 | ForEach-Object {'{0:X2}{1:X2}{2:X2}{3:X2}' -f $_[0],$_[1],$_[2],$_[3]}"') do set HEADER=%%B
        
        if "!HEADER:~0,16!"=="53616C7465645F5F" (
            echo [!COUNTER!] '!PWD!' - STILL ENCRYPTED
        ) else if "!HEADER:~0,2!"=="AA" (
            echo [!COUNTER!] '!PWD!' - Garbage data (bad key)
        ) else (
            echo ✓ [!COUNTER!] '!PWD!' - POSSIBLE SUCCESS! Size: !SIZE! bytes, Header: !HEADER!
            set /a SUCCESS_COUNT+=1
            echo   ^>^> EXAMINE THIS FILE: test_!COUNTER!.bin
        )
    )
    
    goto loop
)

echo.
echo ================================================================================
echo TESTING COMPLETE
echo ================================================================================
echo.
echo If no success above, trying -pbkdf2 digest method on top candidates...
echo.

REM Try PBKDF2 on top candidates
set "pbkdf2_passwords[0]=HALFANDBETTERHALF"
set "pbkdf2_passwords[1]=halfandbetterhalf"
set "pbkdf2_passwords[2]=THEMATRIXHASYOU"
set "pbkdf2_passwords[3]=PRIVATEKEYS"
set "pbkdf2_passwords[4]=THEPRIVATEKEYSBELONGTOHALFANDBETTERHALF"

set PBKDF_COUNTER=0
:pbkdf2_loop
if defined pbkdf2_passwords[%PBKDF_COUNTER%] (
    set "PWD=!pbkdf2_passwords[%PBKDF_COUNTER%]!"
    set /a PBKDF_COUNTER+=1
    
    openssl enc -aes-256-cbc -d -a -in %INPUT_FILE% -pass pass:"!PWD!" -pbkdf2 -out test_pbkdf2_!PBKDF_COUNTER!.bin 2>nul
    
    if exist test_pbkdf2_!PBKDF_COUNTER!.bin (
        for %%A in (test_pbkdf2_!PBKDF_COUNTER!.bin) do set SIZE=%%~zA
        echo [PBKDF2-!PBKDF_COUNTER!] '!PWD!' - Size: !SIZE! bytes
    )
    
    goto pbkdf2_loop
)

echo.
echo Next: Run this command to examine successful files:
echo   od -An -tx1 -N32 test_N.bin
echo   (where N is the number of a successful test)
echo.
pause