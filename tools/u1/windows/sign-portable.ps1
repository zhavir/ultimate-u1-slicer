param([Parameter(Mandatory=$true)][string]$Payload)
$ErrorActionPreference = 'Stop'
$payloadPath = (Resolve-Path $Payload).Path
$reportPath = Join-Path $payloadPath 'windows-signing.json'
if (-not $env:U1_WINDOWS_SIGNING_CERT_BASE64) {
    @{ signed=$false; status='not_configured'; reason='No code-signing identity configured; this is an unsigned test candidate.' } |
        ConvertTo-Json | Set-Content -Encoding utf8 $reportPath
    Write-Host 'Code-signing identity is not configured. Candidate remains explicitly unsigned.'
    exit 0
}
$tool = Get-ChildItem "${env:ProgramFiles(x86)}/Windows Kits/10/bin/*/x64/signtool.exe" |
    Sort-Object FullName -Descending | Select-Object -First 1
if (-not $tool) { throw 'Windows SDK SignTool is unavailable' }
$pfx = Join-Path $env:RUNNER_TEMP ('u1-signing-' + [guid]::NewGuid() + '.pfx')
$existing = @(Get-ChildItem Cert:/CurrentUser/My | ForEach-Object Thumbprint)
$imported = @()
try {
    [IO.File]::WriteAllBytes($pfx, [Convert]::FromBase64String($env:U1_WINDOWS_SIGNING_CERT_BASE64))
    $password = if ($env:U1_WINDOWS_SIGNING_CERT_PASSWORD) { ConvertTo-SecureString $env:U1_WINDOWS_SIGNING_CERT_PASSWORD -AsPlainText -Force } else { [Security.SecureString]::new() }
    $imported = @(Import-PfxCertificate -FilePath $pfx -CertStoreLocation Cert:/CurrentUser/My -Password $password)
    $certificate = @($imported | Where-Object {
        $_.HasPrivateKey -and ($_.EnhancedKeyUsageList.ObjectId -contains '1.3.6.1.5.5.7.3.3')
    })
    if ($certificate.Count -ne 1) { throw 'Expected one code-signing certificate with its private key' }
    if ($certificate[0].NotAfter -le (Get-Date)) { throw 'Code-signing certificate is expired' }
    $names = @('orca-slicer.exe','OrcaSlicer.dll','orca-slicer-console.exe','OrcaSlicer_profile_validator.exe')
    $files = @(Get-ChildItem $payloadPath -File | Where-Object { $_.Name -in $names })
    if (-not ($files.Name -contains 'orca-slicer.exe')) { throw 'Portable application executable is missing' }
    $signed = @()
    foreach ($file in $files) {
        & $tool.FullName sign /sha1 $certificate[0].Thumbprint /s My /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 $file.FullName
        if ($LASTEXITCODE -ne 0) { throw "Signing failed for $($file.Name)" }
        & $tool.FullName verify /pa /all $file.FullName
        if ($LASTEXITCODE -ne 0) { throw "Signature verification failed for $($file.Name)" }
        $signature = Get-AuthenticodeSignature -LiteralPath $file.FullName
        if ($signature.Status -ne 'Valid' -or -not $signature.TimeStamperCertificate) {
            throw "A trusted timestamped signature was not established for $($file.Name)"
        }
        $signed += @{file=$file.Name; status='Valid'; thumbprint=$signature.SignerCertificate.Thumbprint}
    }
    @{signed=$true; status='Valid'; files=$signed} | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 $reportPath
} finally {
    Remove-Item -LiteralPath $pfx -Force -ErrorAction SilentlyContinue
    foreach ($certificate in $imported) {
        if ($certificate.Thumbprint -notin $existing) {
            Remove-Item -LiteralPath ('Cert:/CurrentUser/My/' + $certificate.Thumbprint) -DeleteKey -Force
        }
    }
    Remove-Item Env:/U1_WINDOWS_SIGNING_CERT_BASE64 -ErrorAction SilentlyContinue
    Remove-Item Env:/U1_WINDOWS_SIGNING_CERT_PASSWORD -ErrorAction SilentlyContinue
}
