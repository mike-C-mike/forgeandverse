# Forge & Verse v19 Validation

Prepared from a crawl of the public GitHub repository at commit:

```text
7d1e87c1d4770ee826276851fe1035751d76e9b8
```

## Repository issues corrected by this update

- orphaned physical-edition layouts and documentation
- removed edition metadata on the only current wall work
- rejected Verification Desk Card still present as a public release
- committed Python bytecode and cache directories
- duplicate fields in the Work archetype
- inconsistent v18 / v18.19 / 18.0 version labels
- superseded downloadable bundles mixed with the current release

## Package-level checks completed

- updater archive integrity
- Python syntax compilation for new scripts
- YAML parsing for replacement front matter
- PowerShell script syntax review
- replacement-file path verification
- delete-manifest path verification

## Required local checks after applying

```powershell
.\scripts\clean.ps1
.\scripts\build.ps1
```

Then review:

```text
/
/works/
/works/believe-in-the-badge/
/editions/
/materials/
/releases/
/downloads/digital-forensics-intake-request/
/roadmap/bench-status-pad/
/roadmap/examination-notebook/
```

The GitHub Actions workflow performs the same production build on future pushes and pull requests.
