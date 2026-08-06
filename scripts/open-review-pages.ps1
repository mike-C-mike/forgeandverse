param(
    [int]$Port = 1314
)

$Base = "http://localhost:$Port"
$Pages = @(
    "/",
    "/works/",
    "/releases/",
    "/journal/",
    "/journal/the-pause-is-part-of-the-examination/",
    "/roadmap/",
    "/roadmap/bench-status-pad/",
    "/downloads/digital-forensics-intake-request/"
)

Write-Host "Opening Forge & Verse review pages from $Base" -ForegroundColor Cyan
foreach ($Page in $Pages) {
    Start-Process "$Base$Page"
}
