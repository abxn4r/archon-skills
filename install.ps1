# Archon One-Command Zero-Friction Installer (Windows PowerShell)
# Zero external dependencies. Uses system Python 3.

$ErrorActionPreference = "Stop"

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "              ARCHON SKILL SUITE INSTALLER                 " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

# 1. Locate Python
$PythonExe = $null
$pyCommands = @("python", "py", "python3")
foreach ($cmd in $pyCommands) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $PythonExe = $cmd
        break
    }
}

if (-not $PythonExe) {
    Write-Host "[ERROR] Python 3 was not found on your system PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org or the Microsoft Store."
    exit 1
}

$PyVersion = & $PythonExe -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "[✓] Found Python $PyVersion ($PythonExe)" -ForegroundColor Green

# 2. Configure Launcher in User Bin
$ArchonDir = $PSScriptRoot
$UserBin = Join-Path $env:USERPROFILE ".local\bin"
if (-not (Test-Path $UserBin)) {
    New-Item -ItemType Directory -Path $UserBin -Force | Out-Null
}

$BatchLauncher = Join-Path $UserBin "archon.bat"
$BatchContent = @"
@echo off
set "PYTHONPATH=$ArchonDir;%PYTHONPATH%"
$PythonExe -m archon.cli %*
"@

Set-Content -Path $BatchLauncher -Value $BatchContent -Encoding UTF8
Write-Host "[✓] Created executable launcher at $BatchLauncher" -ForegroundColor Green

# Check User PATH
$UserPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
if ($UserPath -notlike "*$UserBin*") {
    Write-Host "[+] Adding $UserBin to User PATH..." -ForegroundColor Cyan
    $NewPath = "$UserBin;$UserPath"
    [Environment]::SetEnvironmentVariable("PATH", $NewPath, [EnvironmentVariableTarget]::User)
    $env:PATH = "$UserBin;$env:PATH"
    Write-Host "[✓] Updated User PATH environment variable." -ForegroundColor Green
}

# 3. Run Archon Initialization & Agent Discovery
Write-Host "`n--- Auto-Detecting & Configuring AI Coding Agents ---" -ForegroundColor Cyan
& $PythonExe -m archon.cli init

Write-Host "`n[✓] Archon installation completed successfully!" -ForegroundColor Green
Write-Host "Run 'archon dashboard' or 'archon council `"<proposal>`"' to begin." -ForegroundColor Yellow
