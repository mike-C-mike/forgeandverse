# Forge & Verse v19 Validation

The v19.4 release-ledger portability hotfix was prepared against GitHub `main` at:

```text
c6fd5716d27b60066c3f652098d9ea1b80d1b8da
```

## What the v19.3 CI run proved

The v19.3 workflow passed every substantive validation stage:

1. rendered-site validator regression tests
2. repository hygiene
3. release-ledger generation
4. source and release-artifact validation
5. Hugo Extended 0.164.0 production build
6. rendered-site validation

The production build rendered 45 Hugo pages, and the rendered-site validator passed over 32 HTML pages and 107 static files.

The only failure occurred in the final reproducibility check:

```text
git diff --exit-code -- static/releases
```

Windows had previously generated ZIP media types as:

```text
application/x-zip-compressed
```

while the Linux GitHub runner regenerated them as:

```text
application/zip
```

The release files, byte counts, and SHA-256 values were unchanged. The defect was host-dependent metadata generation.

## Corrected by v19.4

- removes dependence on Python's OS MIME registry for release records
- defines canonical media types for supported Forge & Verse release-file extensions
- records ZIP as `application/zip` on every platform
- uses `application/octet-stream` for unknown extensions until intentionally classified
- writes generated ledger and checksum records with LF line endings
- adds six portability regression tests
- runs the new tests in both `scripts/build.ps1` and GitHub Actions
- warns during a local production build if the ledger was regenerated differently from the committed records

## Local verification

Run:

```powershell
python .\scripts\test_build_release_ledger.py
python .\scripts\test_validate_public.py
.\scripts\clean.ps1
.\scripts\build.ps1
```

The first v19.4 build is expected to update:

```text
static/releases/forge-and-verse-release-ledger.json
static/releases/forge-and-verse-release-ledger.sha256
```

because the committed records were generated under Windows MIME rules. Review those two deterministic changes and include them in the v19.4 commit.

Expected GitHub result after pushing:

1. both regression-test suites pass
2. repository hygiene passes
3. release ledger rebuilds
4. source validation passes
5. Hugo production build succeeds
6. rendered-site validation passes
7. final release-ledger diff is clean

At that point the complete v19 validation pipeline is green.
