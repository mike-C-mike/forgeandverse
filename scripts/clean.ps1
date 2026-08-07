param(
    [switch]$IncludeBackups
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

$Targets = @(
    (Join-Path $RepoRoot "public"),
    (Join-Path $RepoRoot "resources\_gen"),
    (Join-Path $RepoRoot ".hugo_build.lock")
)

foreach ($Target in $Targets) {
    if (Test-Path $Target) {
        Remove-Item $Target -Recurse -Force
        Write-Host "Removed $Target" -ForegroundColor DarkGray
    }
}

Get-ChildItem $RepoRoot -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    ForEach-Object {
        Remove-Item $_.FullName -Recurse -Force
        Write-Host "Removed $($_.FullName)" -ForegroundColor DarkGray
    }

Get-ChildItem $RepoRoot -Recurse -File -Include "*.pyc", "*.pyo" -ErrorAction SilentlyContinue |
    ForEach-Object {
        Remove-Item $_.FullName -Force
        Write-Host "Removed $($_.FullName)" -ForegroundColor DarkGray
    }

if ($IncludeBackups) {
    $BackupRoot = Join-Path $RepoRoot ".forge-backups"
    if (Test-Path $BackupRoot) {
        Remove-Item $BackupRoot -Recurse -Force
        Write-Host "Removed $BackupRoot" -ForegroundColor DarkGray
    }
}

Write-Host "Forge & Verse working tree cleanup complete." -ForegroundColor Green
