# Find duplicate .bin files and identify which password is correct
# This helps us figure out which .bin files have identical content

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "ANALYZING .BIN FILES FOR DUPLICATES AND CORRECT PASSWORD"
Write-Host "===================================================================================================="
Write-Host ""

$binFiles = @(Get-ChildItem -Filter "test_*.bin" -ErrorAction SilentlyContinue)
$binFiles += @(Get-ChildItem -Filter "test_output_*.bin" -ErrorAction SilentlyContinue)
$binFiles = $binFiles | Sort-Object Name

Write-Host "Found $($binFiles.Count) files`n"

# Calculate hash of each file
$fileHashes = @{}
$hashToFiles = @{}

Write-Host "Computing file hashes (to find duplicates)...`n"

foreach ($file in $binFiles) {
    $hash = (Get-FileHash -Path $file.FullName -Algorithm SHA256).Hash
    $fileHashes[$file.Name] = $hash
    
    if (-not $hashToFiles.ContainsKey($hash)) {
        $hashToFiles[$hash] = @()
    }
    $hashToFiles[$hash] += $file.Name
}

Write-Host "===================================================================================================="
Write-Host "DUPLICATE FILES (same content = same wrong password used)"
Write-Host "===================================================================================================="
Write-Host ""

$duplicateCount = 0
foreach ($hash in $hashToFiles.Keys) {
    if ($hashToFiles[$hash].Count -gt 1) {
        $duplicateCount++
        Write-Host "Group $duplicateCount - Files with identical content:"
        Write-Host "  Hash: $($hash.Substring(0, 16))..."
        foreach ($filename in $hashToFiles[$hash]) {
            Write-Host "    - $filename"
        }
        Write-Host ""
    }
}

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "UNIQUE FILES (different content = different wrong passwords OR correct password)"
Write-Host "===================================================================================================="
Write-Host ""

$uniqueCount = 0
foreach ($hash in $hashToFiles.Keys) {
    if ($hashToFiles[$hash].Count -eq 1) {
        $uniqueCount++
        $filename = $hashToFiles[$hash][0]
        Write-Host "[$uniqueCount] $filename - Hash: $($hash.Substring(0, 24))..."
    }
}

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "SUMMARY"
Write-Host "===================================================================================================="
Write-Host ""
Write-Host "Total files: $($binFiles.Count)"
Write-Host "Unique file hashes: $($hashToFiles.Keys.Count)"
Write-Host "Files in duplicate groups: $($binFiles.Count - $uniqueCount)"
Write-Host "Truly unique files: $uniqueCount"
Write-Host ""

if ($uniqueCount -lt 10) {
    Write-Host "GOOD NEWS: Only $uniqueCount unique files - makes it easier to check!"
} else {
    Write-Host "NOTE: $uniqueCount different files to check"
}

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "NEXT STEPS"
Write-Host "===================================================================================================="
Write-Host ""
Write-Host "1. This tells us that most passwords tested were WRONG (produced garbage)"
Write-Host "2. All files are 1312 bytes = same size as encrypted file (bad sign)"
Write-Host "3. The CORRECT password should produce DIFFERENT-sized output"
Write-Host ""
Write-Host "ACTION: Need to test with DIFFERENT DIGEST METHOD:"
Write-Host "  - Try: -pbkdf2 instead of -md sha256"
Write-Host "  - Try: -md MD5 instead of -md sha256"
Write-Host "  - Try: Different iteration counts (-iter parameter)"
Write-Host ""
Write-Host "The password may still be one of the tested ones, but with different encryption method!"
Write-Host ""