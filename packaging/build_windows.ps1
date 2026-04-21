# Build ET Scribe desktop bundle on Windows (64-bit Python).
# Run in PowerShell:  powershell -ExecutionPolicy Bypass -File packaging\build_windows.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found on PATH."
}

python -m pip install -r requirements.txt
python -m pip install -r packaging\requirements-packaging.txt
python -m PyInstaller --noconfirm packaging\et_scribe.spec

Write-Host "Built: $Root\dist\ET-Scribe\ET-Scribe.exe"
Write-Host "Copy ffmpeg.exe and ffprobe.exe next to the exe (or install FFmpeg on PATH)."
