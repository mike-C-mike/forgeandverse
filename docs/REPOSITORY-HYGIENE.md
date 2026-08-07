# Repository Hygiene

Forge & Verse keeps source, generated output, public release files, and local tools deliberately separated.

## Never commit

- `public/`
- `resources/_gen/`
- `.hugo_build.lock`
- `__pycache__/`
- `*.pyc`
- virtual environments
- editor settings
- local `hugo.exe`
- updater backup folders

## Source and public files

- high-resolution working files and exact-size source proofs belong under `source-assets/`
- optimized site images belong under `static/images/`
- approved public downloads belong under `static/downloads/`
- machine release records belong under `static/releases/`
- build helpers and validators belong under `scripts/`

## Generated release records

The release ledger is deterministic and tracked. Rebuild it before validation:

```powershell
.\scripts\rebuild_release_ledger.ps1
```

A clean rebuild should not change committed ledger files unless release metadata or a tracked artifact changed.

## Duplicate YAML keys

Duplicate keys are rejected because standard YAML parsers silently keep one value and discard another. This is especially dangerous in front matter where a repeated related link, status, or release field can hide the intended value.

Run:

```powershell
python .\scripts\validate_hygiene.py
```

## Version alignment

The framework version must agree across:

- `hugo.toml`
- `README.md`
- `ITERATION-NOTES.md`
- `VALIDATION.md`

## Obsolete releases

Rejected concepts and superseded public files are deleted rather than left in the active release tree. Historical version notes may remain in Markdown without retaining every old downloadable bundle.

See `docs/ARCHIVE-POLICY.md`.

## Public Work retirement

A concept is removed from `content/works/` when it is rejected, duplicated by a better editorial home, or does not yet satisfy the current Work content model. Git history is sufficient recovery for retired concepts; the active Work archive should not be used as a backlog.

The hygiene validator keeps a small explicit denylist for retired public paths that must not silently return during future merges or ZIP overlays.
