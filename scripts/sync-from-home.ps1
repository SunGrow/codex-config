[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$SourceRoot = (Join-Path $HOME ".codex")
)

$ErrorActionPreference = "Stop"

$targetRoot = Join-Path $RepoRoot ".codex"
New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

$shareablePaths = @(
    ".gitignore",
    "AGENTS.md",
    "AGENTIC-WORKFLOW-INSTRUCTIONS.md",
    "CODEX-CONFIG-INSTRUCTIONS.md",
    "config.template.toml",
    "README.md",
    "RESEARCH-INSTRUCTIONS.md",
    "UE-INSTRUCTIONS.md",
    "agent-rules",
    "docs",
    "memories",
    "skills"
)

foreach ($relativePath in $shareablePaths) {
    $sourcePath = Join-Path $SourceRoot $relativePath
    $targetPath = Join-Path $targetRoot $relativePath

    if (-not (Test-Path -LiteralPath $sourcePath)) {
        continue
    }

    if (Test-Path -LiteralPath $sourcePath -PathType Container) {
        if (Test-Path -LiteralPath $targetPath) {
            Remove-Item -LiteralPath $targetPath -Recurse -Force
        }
        Copy-Item -LiteralPath $sourcePath -Destination $targetPath -Recurse -Force
        continue
    }

    $targetParent = Split-Path -Parent $targetPath
    if ($targetParent) {
        New-Item -ItemType Directory -Force -Path $targetParent | Out-Null
    }

    Copy-Item -LiteralPath $sourcePath -Destination $targetPath -Force
}

$cleanupPaths = @(
    (Join-Path $targetRoot "skills\\.system\\slides"),
    (Join-Path $targetRoot "skills\\.system\\spreadsheets"),
    (Join-Path $targetRoot "skills\\.system\\.codex-system-skills.marker"),
    (Join-Path $targetRoot "archived_sessions"),
    (Join-Path $targetRoot "sqlite"),
    (Join-Path $targetRoot "vendor_imports"),
    (Join-Path $targetRoot "migrations"),
    (Join-Path $targetRoot "migrated-from-claude")
)

foreach ($path in $cleanupPaths) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -LiteralPath $path -Recurse -Force
    }
}

Write-Host ("Imported shareable Codex config from {0} into {1}" -f $SourceRoot, $targetRoot)
