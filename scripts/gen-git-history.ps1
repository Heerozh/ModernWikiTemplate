param(
    [int]$Limit = 10,
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$ContentDir = "content",
    [string]$OutputPath = "data/git_history.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$contentRoot = Join-Path $RepoRoot $ContentDir
$outputFile = Join-Path $RepoRoot $OutputPath
$outputDir = Split-Path -Parent $outputFile

$repoRootResolved = (Resolve-Path $RepoRoot).Path.TrimEnd('\', '/')
$contentRootResolved = (Resolve-Path $contentRoot).Path.TrimEnd('\', '/')

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
}

if (-not (Test-Path $contentRoot)) {
    [System.IO.File]::WriteAllText($outputFile, "{}", [System.Text.UTF8Encoding]::new($false))
    Write-Host "Content directory not found: $contentRoot. Wrote empty history file."
    exit 0
}

$null = git -C $RepoRoot rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0) {
    [System.IO.File]::WriteAllText($outputFile, "{}", [System.Text.UTF8Encoding]::new($false))
    Write-Host "Not a git repository: $RepoRoot. Wrote empty history file."
    exit 0
}

$result = [ordered]@{}
$mdFiles = Get-ChildItem -Path $contentRoot -Recurse -File -Filter *.md | Sort-Object FullName

foreach ($file in $mdFiles) {
    $repoRelativePath = $file.FullName.Substring($repoRootResolved.Length).TrimStart('\', '/').Replace('\', '/')
    $contentRelativePath = $file.FullName.Substring($contentRootResolved.Length).TrimStart('\', '/').Replace('\', '/')

    $rawLines = git -C $RepoRoot log --follow --max-count=$Limit --date=iso-strict --pretty=format:%H%x1f%h%x1f%an%x1f%ae%x1f%ad%x1f%s -- "$repoRelativePath"
    if ($LASTEXITCODE -ne 0) {
        continue
    }

    $commits = @()
    foreach ($line in $rawLines) {
        if ([string]::IsNullOrWhiteSpace($line)) {
            continue
        }

        $parts = $line -split [char]0x1f
        if ($parts.Count -lt 6) {
            continue
        }

        $commits += [ordered]@{
            hash = $parts[0]
            shortHash = $parts[1]
            authorName = $parts[2]
            authorEmail = $parts[3]
            authorDate = $parts[4]
            subject = $parts[5]
        }
    }

    $result[$contentRelativePath] = $commits
}

$json = $result | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText($outputFile, $json, [System.Text.UTF8Encoding]::new($false))

Write-Host "Git history generated: $outputFile"
Write-Host "Tracked files: $($result.Count); limit per file: $Limit"