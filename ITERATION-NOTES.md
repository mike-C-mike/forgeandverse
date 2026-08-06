# Forge & Verse v18

This iteration adds a public release-verification layer without changing the studio into a download warehouse.

## Public changes

- Added the Release Desk for current open releases and printable field proofs.
- Separated finished operational releases from controlled field proofs.
- Added visible versions, update dates, bundle hashes, direct downloads, and concise purpose context.
- Added platform-specific SHA-256 verification commands for PowerShell, Windows, macOS, and Linux.
- Added a machine-readable JSON release ledger and plain-text checksum manifest.
- Added Release Desk entry points from Work, Free Works, the homepage, and the footer.
- Clarified that direct downloads do not require an account or email gate and that the fillable intake PDF contains no telemetry or automatic submission.

## Foundation changes

- Added deterministic release-ledger generation from front matter and actual public files.
- Added per-file byte counts, media types, and SHA-256 values to the generated JSON.
- Added a PowerShell rebuild helper.
- Updated development and production scripts to rebuild the ledger before validation.
- Expanded repository validation to catch missing files, stale byte counts, stale hashes, invalid ledger entries, and broken checksum-manifest lines.
- Added internal documentation for maintaining the ledger.

## Current release desk

- 1 open operational release
- 2 printable field proofs
- 18 current public package files and manifests tracked by SHA-256
