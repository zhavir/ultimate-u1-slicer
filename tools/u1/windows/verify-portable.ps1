param(
    [Parameter(Mandatory=$true)][string]$Archive,
    [Parameter(Mandatory=$true)][string]$OutputDirectory
)
$ErrorActionPreference = 'Stop'
$archivePath = (Resolve-Path $Archive).Path
$output = New-Item -ItemType Directory -Force $OutputDirectory
$work = Join-Path $env:RUNNER_TEMP ("u1-portable-" + [guid]::NewGuid())
Expand-Archive -LiteralPath $archivePath -DestinationPath $work
$executables = @(Get-ChildItem $work -Recurse -Filter orca-slicer.exe)
if ($executables.Count -ne 1) { throw 'Expected exactly one portable slicer executable' }
$exe = $executables[0]
$data = Join-Path $exe.DirectoryName 'ultimate_u1_data_dir'
if (-not (Test-Path (Join-Path $data 'portable-mode.txt'))) { throw 'Portable data directory marker missing' }
if (@(Get-ChildItem $data -Recurse -File).Count -ne 1) { throw 'Archive contains unexpected portable user data' }
if (Get-ChildItem $work -Recurse -File | Where-Object { $_.Name -in @('token', 'server.json') }) {
    throw 'Archive contains MCP authentication state'
}
$appData = Join-Path $env:APPDATA 'UltimateU1Slicer'
if (Test-Path $appData) { throw 'Verification requires a clean runner profile' }
$urlRegistration = 'HKCU:\Software\Classes\ultimate-u1-slicer'
if (Test-Path $urlRegistration) { throw 'Verification requires no prior Ultimate U1 URL registration' }
& $exe.FullName --help | Out-File (Join-Path $output 'help.txt')
if ($LASTEXITCODE -ne 0) { throw 'Native Windows help failed' }
$process = $null
try {
    $process = Start-Process -FilePath $exe.FullName -WorkingDirectory $exe.DirectoryName -ArgumentList '--mcp','--mcp-port','13981' -PassThru
    $discovery = Join-Path $data 'mcp/server.json'
    for ($attempt = 0; $attempt -lt 120; $attempt++) {
        if (Test-Path $discovery) { break }
        if ($process.HasExited) { throw "Portable GUI exited early: $($process.ExitCode)" }
        Start-Sleep -Milliseconds 500
    }
    if (-not (Test-Path $discovery)) { throw 'Portable GUI did not create MCP discovery beside the executable' }
    if (Test-Path $appData) { throw 'Portable launch wrote to the roaming application directory' }
    $server = Get-Content -Raw $discovery | ConvertFrom-Json
    if ($server.url -ne 'http://127.0.0.1:13981/mcp') { throw 'Unexpected MCP endpoint' }
    $body = @{jsonrpc='2.0'; id=1; method='initialize'; params=@{protocolVersion='2025-11-25'; capabilities=@{}; clientInfo=@{name='u1-portable-ci'; version='1'}}} | ConvertTo-Json -Depth 8 -Compress
    $anonymous = Invoke-WebRequest -Uri $server.url -Method Post -Body $body -ContentType application/json -SkipHttpErrorCheck
    if ([int]$anonymous.StatusCode -ne 401) { throw 'MCP did not require authentication' }
    $reply = Invoke-RestMethod -Uri $server.url -Method Post -Body $body -ContentType application/json -Headers @{Authorization="Bearer $($server.token)"}
    if ($reply.result.serverInfo.name -ne 'ultimate-u1-slicer') { throw 'Unexpected server identity' }
    $waitBody = @{jsonrpc='2.0'; id=2; method='tools/call'; params=@{name='wait'; arguments=@{for='ready'; timeout_s=45}}} | ConvertTo-Json -Depth 8
    $readyReply = Invoke-RestMethod -Uri $server.url -Method Post -Body $waitBody -ContentType application/json -Headers @{Authorization="Bearer $($server.token)"} -TimeoutSec 55
    if ($readyReply.result.isError) { throw 'Native GUI readiness check failed' }
    $ready = $readyReply.result.content[0].text | ConvertFrom-Json
    if (-not $ready.satisfied) { throw 'Native GUI did not finish startup' }
    if ((Test-Path $appData) -or (Test-Path $urlRegistration)) { throw 'Portable startup wrote roaming settings or registered a URL handler' }
    # Exercise the shipped bridge without --datadir or a token override: it must find the
    # same portable discovery file as the GUI, rather than another slicer's profile.
    $bridge = [Diagnostics.Process]::new()
    $bridge.StartInfo = [Diagnostics.ProcessStartInfo]::new($exe.FullName, '--mcp-stdio --mcp-port 13981')
    $bridge.StartInfo.WorkingDirectory = $exe.DirectoryName
    $bridge.StartInfo.UseShellExecute = $false
    $bridge.StartInfo.RedirectStandardInput = $true
    $bridge.StartInfo.RedirectStandardOutput = $true
    $bridge.StartInfo.RedirectStandardError = $true
    try {
        if (-not $bridge.Start()) { throw 'Could not launch the native stdio bridge' }
        $stdout = $bridge.StandardOutput.ReadToEndAsync()
        $stderr = $bridge.StandardError.ReadToEndAsync()
        $bridge.StandardInput.WriteLine($body)
        $bridge.StandardInput.Close()
        if (-not $bridge.WaitForExit(30000)) { throw 'Portable stdio bridge timed out' }
        if ($bridge.ExitCode -ne 0) { throw 'Portable stdio bridge failed' }
        $stdioReply = $stdout.GetAwaiter().GetResult() | ConvertFrom-Json
        if ($stdioReply.result.serverInfo.name -ne 'ultimate-u1-slicer') { throw 'Stdio bridge did not resolve the portable server' }
        $null = $stderr.GetAwaiter().GetResult()
    } finally {
        if (-not $bridge.HasExited) { $bridge.Kill(); $bridge.WaitForExit() }
        $bridge.Dispose()
    }
    if ((Test-Path $appData) -or (Test-Path $urlRegistration)) { throw 'Stdio startup escaped portable storage' }
    $report = @{platform='Windows x64'; portable_directory_detected=$true; roaming_directory_untouched=$true; url_registration_untouched=$true; native_gui_ready=$true; native_help_passed=$true; authenticated_mcp_initialize_passed=$true; portable_stdio_initialize_passed=$true; printer_contacted=$false; hardware_verified=$false; stable_release=$false; source_commit=$env:GITHUB_SHA}
    $report | ConvertTo-Json | Set-Content (Join-Path $output 'verification.json')
    $hash = (Get-FileHash $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    "$hash  $([IO.Path]::GetFileName($archivePath))" | Set-Content (Join-Path $output 'SHA256SUMS')
} finally {
    if ($process -and -not $process.HasExited) { Stop-Process -Id $process.Id -Force; $process.WaitForExit(15000) | Out-Null }
    # Only the private extracted test copy contains generated settings/tokens; never upload it.
    Remove-Item -Recurse -Force $work
}
