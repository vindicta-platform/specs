$ErrorActionPreference = "Continue"

# Find all directories that start with a number (e.g., 001-ocr-parser)
$specDirs = Get-ChildItem -Directory -Filter "0*" | Select-Object -ExpandProperty Name

foreach ($spec in $specDirs) {
    if (Test-Path "$spec\spec.md") {
        Write-Host "Triggering speckit-pipeline for $spec..."
        gh workflow run speckit-pipeline.yml -f feature_dir="$spec"
        # Small delay to prevent API rate limiting
        Start-Sleep -Seconds 2
    } else {
        Write-Host "Skipping $spec (No spec.md found)."
    }
}

Write-Host "All pipelines triggered."
