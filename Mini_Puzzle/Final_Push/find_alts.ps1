# Test top passwords with different digest methods
# The -md sha256 approach didn't work, so try -pbkdf2 or -md MD5

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "TESTING TOP PASSWORDS WITH ALTERNATIVE DIGEST METHODS"
Write-Host "===================================================================================================="
Write-Host ""

$inputFile = "cosmic_duality_content.txt"

# Top password candidates (priority order)
$passwords = @(
    "HALFANDBETTERHALF",
    "halfandbetterhalf",
    "THEPRIVATEKEYSBELONGTOHALFANDBETTERHALF",
    "theprivatekeysbelongtohalfandbetterhalf",
    "THEMATRIXHASYOU",
    "thematrixhasyou",
    "PRIVATEKEYS",
    "privatekeys",
    "COSMICDUALITY",
    "cosmicduality"
)

Write-Host "Testing $($passwords.Count) passwords with PBKDF2 method...`n"

$pbkdf2Results = @()

foreach ($pwd in $passwords) {
    Write-Host "Testing: '$pwd' with -pbkdf2"
    
    $outputFile = "pbkdf2_temp.bin"
    
    $process = Start-Process -FilePath "openssl" `
        -ArgumentList @("enc", "-aes-256-cbc", "-d", "-a", `
                        "-in", $inputFile, `
                        "-pass", "pass:$pwd", `
                        "-pbkdf2", `
                        "-out", $outputFile) `
        -NoNewWindow -RedirectStandardError $null -RedirectStandardOutput $null -Wait -PassThru
    
    if (Test-Path $outputFile) {
        $fileSize = (Get-Item $outputFile).Length
        Write-Host "  Result: $fileSize bytes"
        
        if ($fileSize -lt 1300 -and $fileSize -gt 50) {
            Write-Host "  *** DIFFERENT SIZE! Might be correct! ***" -ForegroundColor Green
            $pbkdf2Results += @{ Password = $pwd; Size = $fileSize }
            
            # Show hex
            $bytes = [System.IO.File]::ReadAllBytes($outputFile)
            $hex = ($bytes[0..31] | ForEach-Object { "{0:X2}" -f $_ }) -join " "
            Write-Host "  First 32 bytes: $hex"
        }
        
        Remove-Item $outputFile -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host ""
}

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "TESTING WITH -md MD5"
Write-Host "===================================================================================================="
Write-Host ""

$md5Results = @()

foreach ($pwd in $passwords[0..5]) {
    Write-Host "Testing: '$pwd' with -md MD5"
    
    $outputFile = "md5_temp.bin"
    
    $process = Start-Process -FilePath "openssl" `
        -ArgumentList @("enc", "-aes-256-cbc", "-d", "-a", `
                        "-in", $inputFile, `
                        "-pass", "pass:$pwd", `
                        "-md", "MD5", `
                        "-out", $outputFile) `
        -NoNewWindow -RedirectStandardError $null -RedirectStandardOutput $null -Wait -PassThru
    
    if (Test-Path $outputFile) {
        $fileSize = (Get-Item $outputFile).Length
        Write-Host "  Result: $fileSize bytes"
        
        if ($fileSize -lt 1300 -and $fileSize -gt 50) {
            Write-Host "  *** DIFFERENT SIZE! Might be correct! ***" -ForegroundColor Green
            $md5Results += @{ Password = $pwd; Size = $fileSize }
        }
        
        Remove-Item $outputFile -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host ""
}

Write-Host ""
Write-Host "===================================================================================================="
Write-Host "SUMMARY"
Write-Host "===================================================================================================="
Write-Host ""

if ($pbkdf2Results.Count -gt 0 -or $md5Results.Count -gt 0) {
    Write-Host "FOUND PROMISING RESULTS!" -ForegroundColor Green
    Write-Host ""
    
    if ($pbkdf2Results.Count -gt 0) {
        Write-Host "PBKDF2 Results:" -ForegroundColor Yellow
        foreach ($result in $pbkdf2Results) {
            Write-Host "  Password: '$($result.Password)' - Size: $($result.Size) bytes"
        }
        Write-Host ""
    }
    
    if ($md5Results.Count -gt 0) {
        Write-Host "MD5 Results:" -ForegroundColor Yellow
        foreach ($result in $md5Results) {
            Write-Host "  Password: '$($result.Password)' - Size: $($result.Size) bytes"
        }
        Write-Host ""
    }
} else {
    Write-Host "No different-sized files found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Try these manual tests:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -pass pass:HALFANDBETTERHALF -pbkdf2 -out test1.bin"
    Write-Host "  dir test1.bin"
    Write-Host ""
    Write-Host "  openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -pass pass:THEMATRIXHASYOU -pbkdf2 -out test2.bin"
    Write-Host "  dir test2.bin"
    Write-Host ""
}

Write-Host ""