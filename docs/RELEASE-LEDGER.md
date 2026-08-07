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

## Deterministic media types

Release metadata must be identical regardless of the machine that generated it.

The generator therefore uses a Forge & Verse canonical extension-to-media-type table instead of Python's host-dependent `mimetypes` registry. This prevents Windows and Linux from disagreeing about values such as ZIP files (`application/x-zip-compressed` versus `application/zip`).

Unknown release-file extensions are recorded as `application/octet-stream` until they are intentionally added to the canonical table.

Generated ledger files are also written with LF line endings so their bytes remain stable across supported development environments.

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

`scripts/test_build_release_ledger.py` protects the canonical media-type rules from platform-specific regression.

GitHub Actions rebuilds the ledger on Linux and then requires `git diff --exit-code -- static/releases` to remain clean. A Windows-generated ledger that changes when rebuilt on Linux is therefore treated as a reproducibility defect.

## Design rule

The ledger should stay boring in the best possible way. It exists to make release identity obvious, not to turn verification into marketing theater.
