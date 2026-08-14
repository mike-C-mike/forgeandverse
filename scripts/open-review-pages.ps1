param(
    [int]$Port = 1314
)

$Base = "http://localhost:$Port"
$Pages = @(
    "/",
    "/roadmap/",
    "/roadmap/bench-status-pad/",
    "/roadmap/examination-notebook/",
    "/roadmap/believe-in-the-badge-edition/",
    "/roadmap/preserved-until-it-matters/",
    "/works/believe-in-the-badge/",
    "/releases/",
    "/materials/"
)

Write-Host "Opening Forge & Verse v20 review pages from $Base" -ForegroundColor Cyan
foreach ($Page in $Pages) {
    Start-Process "$Base$Page"
}
