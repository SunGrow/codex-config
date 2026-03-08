[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$TargetRoot = (Join-Path $HOME ".codex"),
    [switch]$PruneStale
)

$ErrorActionPreference = "Stop"

$sourceRoot = Join-Path $RepoRoot ".codex"
if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Missing source tree: $sourceRoot"
}

$tracked = @(git -C $RepoRoot ls-files --full-name .codex)
if (-not $tracked) {
    throw "No tracked files found under .codex/"
}

$relativeFiles = @(
    $tracked |
        ForEach-Object { $_ -replace '^[.]codex[\\/]', "" } |
        Where-Object { $_ }
)

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

$manifestPath = Join-Path $TargetRoot ".codex-source-manifest.txt"
$previousManifest = @()
if ($PruneStale -and (Test-Path -LiteralPath $manifestPath)) {
    $previousManifest = @(Get-Content -LiteralPath $manifestPath)
}

$managedNow = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)

foreach ($relativePath in $relativeFiles) {
    $null = $managedNow.Add($relativePath)
    $sourcePath = Join-Path $sourceRoot $relativePath
    $targetPath = Join-Path $TargetRoot $relativePath
    $targetParent = Split-Path -Parent $targetPath

    if ($targetParent) {
        New-Item -ItemType Directory -Force -Path $targetParent | Out-Null
    }

    Copy-Item -LiteralPath $sourcePath -Destination $targetPath -Force
}

if ($PruneStale) {
    foreach ($relativePath in $previousManifest) {
        if (-not $managedNow.Contains($relativePath)) {
            $stalePath = Join-Path $TargetRoot $relativePath
            if (Test-Path -LiteralPath $stalePath -PathType Leaf) {
                Remove-Item -LiteralPath $stalePath -Force
            }
        }
    }
}

Set-Content -LiteralPath $manifestPath -Value ($relativeFiles | Sort-Object)
Write-Host ("Synced {0} managed files from {1} to {2}" -f $relativeFiles.Count, $sourceRoot, $TargetRoot)
