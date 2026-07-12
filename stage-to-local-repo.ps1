param(
    [string]$Target = "C:\Users\steel\Desktop\Code\unity-meshy-studio"
)

$ErrorActionPreference = "Stop"
$Source = Join-Path $PSScriptRoot "repo"

if (-not (Test-Path $Target)) {
    throw "Target repository not found: $Target"
}

if (-not (Test-Path (Join-Path $Target ".git"))) {
    throw "Target exists but is not a Git repository: $Target"
}

Write-Host "Copying publish-ready files into $Target ..."

Get-ChildItem -LiteralPath $Source -Force | ForEach-Object {
    $destination = Join-Path $Target $_.Name
    if ($_.PSIsContainer) {
        Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -Force
    } else {
        Copy-Item -LiteralPath $_.FullName -Destination $destination -Force
    }
}

Set-Location $Target

Write-Host "`nRepository status before staging:"
git status --short

git add -A

Write-Host "`nStaged changes:"
git status --short

Write-Host "`nEverything is staged. Review with:"
Write-Host "  git diff --cached --stat"
Write-Host "  git diff --cached"
Write-Host "`nThen commit and push with:"
Write-Host '  git commit -m "Publish Unity Meshy Studio v1.1.0"'
Write-Host "  git push -u origin main"
