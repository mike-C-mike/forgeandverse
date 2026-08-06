param(
    [switch]$RebuildGuides
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $Python) { throw "Python was not found on PATH." }

Push-Location $RepoRoot
try {
    & $Python.Source -c "import fitz, yaml" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Required packages are missing. Run: python -m pip install -r .\scripts\requirements.txt -r .\scripts\requirements-forms.txt"
    }

    if ($RebuildGuides) {
        & $Python.Source -c "import docx" 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "python-docx is missing. Run: python -m pip install -r .\scripts\requirements-docs.txt"
        }
        & $Python.Source .\scripts\build_intake_kit_documents.py
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

        $LibreOffice = Get-Command soffice.exe -ErrorAction SilentlyContinue
        if (-not $LibreOffice) { $LibreOffice = Get-Command libreoffice.exe -ErrorAction SilentlyContinue }
        if (-not $LibreOffice) {
            throw "Guide DOCX files were rebuilt, but LibreOffice was not found on PATH. Export both guides to PDF, visually inspect every page, place the approved PDFs in static\downloads\intake-kit\, then rerun without -RebuildGuides."
        }

        $Kit = Join-Path $RepoRoot "static\downloads\intake-kit"
        $Temp = Join-Path $env:TEMP "forge-and-verse-intake-guides"
        if (Test-Path $Temp) { Remove-Item $Temp -Recurse -Force }
        New-Item -ItemType Directory -Path $Temp | Out-Null
        foreach ($Docx in @(
            "digital-forensics-intake-requester-guide.docx",
            "digital-forensics-intake-implementation-guide.docx"
        )) {
            & $LibreOffice.Source --headless --convert-to pdf --outdir $Temp (Join-Path $Kit $Docx)
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        }
        Copy-Item (Join-Path $Temp "*.pdf") $Kit -Force
        Write-Warning "The guide PDFs were exported automatically. Visually inspect every page before treating the package as approved."
    }

    & $Python.Source .\scripts\build_fillable_intake_form.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $Python.Source .\scripts\audit_fillable_intake_form.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $Python.Source .\scripts\package_intake_release.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $Python.Source .\scripts\validate.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "Digital Forensics Intake Kit rebuilt and validated." -ForegroundColor Green
} finally {
    Pop-Location
}
