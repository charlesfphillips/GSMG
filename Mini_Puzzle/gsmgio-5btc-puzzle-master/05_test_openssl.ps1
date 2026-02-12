# STEP 5: Test Passwords with OpenSSL on Windows
# Run this with: powershell -ExecutionPolicy Bypass -File 05_test_openssl.ps1

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "STEP 5: TEST PASSWORDS WITH OpenSSL" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Check if OpenSSL is installed
try {
    $version = openssl version
    Write-Host "`n✓ OpenSSL found: $version`n" -ForegroundColor Green
} catch {
    Write-Host "`n✗ ERROR: OpenSSL not found!" -ForegroundColor Red
    Write-Host "Please install OpenSSL from: https://slproweb.com/products/Win32OpenSSL.html" -ForegroundColor Yellow
    exit 1
}

# Check if we have the encrypted file
if (!(Test-Path "cosmic_duality_content.txt")) {
    Write-Host "✗ ERROR: cosmic_duality_content.txt not found!" -ForegroundColor Red
    Write-Host "Please run 01_extract.py first" -ForegroundColor Yellow
    exit 1
}

# Read password candidates
$passwords = @()

if (Test-Path "test_passwords.txt") {
    Write-Host "Loading passwords from test_passwords.txt..." -ForegroundColor Yellow
    $passwords = Get-Content "test_passwords.txt"
    Write-Host "Found $($passwords.Count) candidates`n" -ForegroundColor Green
} else {
    Write-Host "✗ ERROR: test_passwords.txt not found!" -ForegroundColor Red
    Write-Host "Please run 04_combine_passwords.py first" -ForegroundColor Yellow
    exit 1
}

# Test each password
$found = $false
$counter = 0

foreach ($line in $passwords) {
    $counter++
    $parts = $line -split '\|'
    $type = $parts[0]
    $pass = $parts[1]
    
    if ($type -eq "RAW") {
        Write-Host "[$counter] Testing RAW password..." -ForegroundColor Cyan
        Write-Host "     $($pass.Substring(0, [Math]::Min(50, $pass.Length)))..." -ForegroundColor Gray
    } else {
        Write-Host "[$counter] Testing SHA256 hash..." -ForegroundColor Cyan
        Write-Host "     $($pass.Substring(0, 50))..." -ForegroundColor Gray
    }
    
    # Try to decrypt
    try {
        $result = & openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -pass pass:$pass 2>&1
        
        if ($result -notmatch "bad decrypt" -and $result.Length -gt 0) {
            Write-Host "✓ SUCCESS!" -ForegroundColor Green
            Write-Host "  Type: $type" -ForegroundColor Green
            Write-Host "  Password: $pass" -ForegroundColor Green
            Write-Host "`nDecrypted content (first 500 chars):" -ForegroundColor Green
            Write-Host "=" * 70 -ForegroundColor Green
            Write-Host $result.Substring(0, [Math]::Min(500, $result.Length)) -ForegroundColor White
            Write-Host "=" * 70 -ForegroundColor Green
            
            # Save full result
            $result | Out-File -FilePath "decrypted_result.txt" -Encoding UTF8
            Write-Host "`n✓ Full result saved to decrypted_result.txt" -ForegroundColor Green
            
            $found = $true
            break
        }
    } catch {
        # Ignore errors, continue to next
    }
    
    Write-Host "  ✗ Failed" -ForegroundColor Gray
    Write-Host ""
}

if (!$found) {
    Write-Host "`n" + "=" * 70 -ForegroundColor Red
    Write-Host "✗ NONE OF THE PASSWORDS WORKED" -ForegroundColor Red
    Write-Host "=" * 70 -ForegroundColor Red
    Write-Host "`nPossible reasons:" -ForegroundColor Yellow
    Write-Host "1. Decoded sections are incorrect (check hex/ABBA decoding)" -ForegroundColor Yellow
    Write-Host "2. Need to try different combinations" -ForegroundColor Yellow
    Write-Host "3. Password is not in the decoded sections" -ForegroundColor Yellow
}

Write-Host "`nDone!" -ForegroundColor Green
