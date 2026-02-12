# Analyze all .bin files from password testing
# Save as: analyze_bin_files.ps1
# Run from: C:\Temp\Mini_Puzzle\Final_Push

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "ANALYZING DECRYPTION ATTEMPTS" 
Write-Host "===================================================================================================="
Write-Host ""

# Find all .bin files
$binFiles = @(Get-ChildItem -Filter "test_*.bin" -ErrorAction SilentlyContinue)
$binFiles += @(Get-ChildItem -Filter "test_output_*.bin" -ErrorAction SilentlyContinue)
$binFiles = $binFiles | Sort-Object Name

if ($binFiles.Count -eq 0) {
    Write-Host "ERROR: No test_*.bin files found!" 
    Write-Host "Current directory: $(Get-Location)"
    Write-Host ""
    exit 1
}

Write-Host "Found $($binFiles.Count) .bin files to analyze`n"

$validCandidates = @()
$largeFiles = @()

Write-Host "Processing files...`n"

foreach ($file in $binFiles) {
    $filename = $file.Name
    $filepath = $file.FullName
    $fileSize = $file.Length
    
    # Read first bytes
    try {
        $bytes = [System.IO.File]::ReadAllBytes($filepath)
        
        if ($bytes.Length -eq 0) {
            Write-Host "EMPTY:  $filename - 0 bytes"
        }
        else {
            # Check for patterns
            $first32 = $bytes[0..31]
            $hexFirst8 = ($first32[0..7] | ForEach-Object { "{0:X2}" -f $_ }) -join ""
            
            # Large files are likely valid
            if ($fileSize -gt 1300) {
                Write-Host "[LARGE] $filename - $fileSize bytes - LIKELY DECRYPTED!"
                $validCandidates += $file
                $largeFiles += $file
            }
            # 64-byte files could be two coordinates
            elseif ($fileSize -eq 64) {
                Write-Host "[64B]   $filename - 64 bytes - Could be K1+K2"
                $validCandidates += $file
            }
            # 32-byte files could be single coordinate
            elseif ($fileSize -eq 32) {
                Write-Host "[32B]   $filename - 32 bytes - Could be single coordinate"
                $validCandidates += $file
            }
            # Check for garbage patterns
            elseif ($hexFirst8 -match "^AA7E81|^0000|^FFFFFF|^FEFEFE") {
                Write-Host "[GARBAGE] $filename - $fileSize bytes - Bad decrypt pattern: $hexFirst8"
            }
            else {
                Write-Host "[?] $filename - $fileSize bytes"
            }
        }
    }
    catch {
        Write-Host "[ERROR] $filename - Cannot read"
    }
}

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "SUMMARY"
Write-Host "===================================================================================================="
Write-Host ""
Write-Host "Total files: $($binFiles.Count)"
Write-Host "Large files (>1300 bytes): $($largeFiles.Count)"
Write-Host "Valid candidates: $($validCandidates.Count)"
Write-Host ""

if ($largeFiles.Count -gt 0) {
    Write-Host "============================================"
    Write-Host "SUCCESS! LARGE FILES FOUND"
    Write-Host "============================================"
    Write-Host ""
    
    foreach ($file in $largeFiles) {
        Write-Host "File: $($file.Name)"
        Write-Host "Size: $($file.Length) bytes"
        Write-Host ""
        
        # Show first 64 bytes
        try {
            $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
            $first64 = $bytes[0..63]
            $hexStr = ($first64 | ForEach-Object { "{0:X2}" -f $_ }) -join " "
            
            Write-Host "First 64 bytes (hex):"
            Write-Host $hexStr
            Write-Host ""
        }
        catch {}
    }
    
    Write-Host ""
    Write-Host "NEXT STEP: Examine the file(s) above in detail"
    Write-Host ""
    Write-Host "To view full hex dump:"
    Write-Host "Format-Hex -Path 'test_output_XX.bin' -Count 200"
    Write-Host ""
    Write-Host "To view as text:"
    Write-Host "Get-Content 'test_output_XX.bin' -Encoding UTF8"
    Write-Host ""
}

if ($validCandidates.Count -eq 0 -and $largeFiles.Count -eq 0) {
    Write-Host "WARNING: No valid candidates found yet"
    Write-Host ""
    Write-Host "This means:"
    Write-Host "1. Password has not been found yet"
    Write-Host "2. Try different digest method (-pbkdf2, -md MD5)"
    Write-Host "3. Check puzzle for additional password hints"
    Write-Host ""
}

Write-Host "Analysis complete."
Write-Host ""