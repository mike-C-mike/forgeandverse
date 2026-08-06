# Release Ledger

The Release Desk gives visitors one compact place to find current open releases and printable field proofs. It is a user-facing utility, not a catalogue of every studio concept.

## Public routes

- `/releases/` presents the human-readable desk.
- `/releases/forge-and-verse-release-ledger.json` publishes the machine-readable ledger.
- `/releases/forge-and-verse-release-ledger.sha256` publishes a plain-text checksum manifest.

## Included entries

The generator includes:

- every non-index page under `content/downloads/`
- every page under `content/roadmap/` where `proof_available: true`

Wall-edition studies and private source proofs are not included unless they expose a public downloadable package.

## File records

Every public file record includes:

- label
- file type
- root-relative path
- byte count
- media type
- SHA-256 value

The JSON ledger also preserves the person, moment, need, form, discipline, public page, version, and release status.

## Rebuild

```powershell
.\scripts\rebuild_release_ledger.ps1
```

Or directly:

```powershell
python .\scripts\build_release_ledger.py
```

Both `dev.ps1` and `build.ps1` rebuild the ledger before validation.

## Validation

`scripts/validate.py` checks:

- ledger schema and entry count
- unique entry IDs
- public content routes
- every recorded file path
- recorded byte sizes
- every recorded SHA-256 value
- the plain-text checksum manifest

A changed file therefore requires a rebuilt ledger before the repository can pass validation.

## Design rule

The ledger should stay boring in the best possible way. It exists to make release identity obvious, not to turn verification into marketing theater.
