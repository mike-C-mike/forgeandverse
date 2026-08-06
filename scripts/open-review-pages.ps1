param(
    [int]$Port = 1314
)

$Base = "http://localhost:$Port"
$Pages = @(
    "/",
    "/works/",
    "/works/believe-in-the-badge/",
    "/editions/",
    "/materials/",
    "/journal/",
    "/roadmap/",
    "/roadmap/believe-in-the-badge-edition/",
    "/downloads/digital-forensics-intake-request/"
)

Write-Host "Opening Forge & Verse review pages from $Base" -ForegroundColor Cyan
foreach ($Page in $Pages) {
    Start-Process "$Base$Page"
}
