# Forge & Verse v19 Validation

The v19.2 cleanup hotfix was prepared against GitHub `main` at:

```text
a1725823dcd6e3b9a6caa116aefa1dfb3020182e
```

## Why v19.2 exists

The first v19 GitHub Actions run correctly exposed a malformed Hugo archetype before the workflow could reach source validation or the Hugo production render. A second repository crawl also found stale Work entries left behind by earlier iterations and two Journal entries missing the current type metadata.

## Corrected by v19.2

- fixed `archetypes/roadmap.md` so its Hugo title expression is valid YAML
- removed the rejected `Keeper of the Krapola` Work entry
- removed duplicate or undeveloped Work entries for `A Hash Is a Promise`, `Every Item Has a Story`, `The Hash Matched`, and `The Quiet Work Behind the Case`
- retained the two completed ideas that belong in Journal and normalized their Journal type metadata
- added retired Work paths to repository-hygiene regression checks
- moved `actions/checkout` and `actions/setup-python` to v6 to avoid the Node 20 deprecation path

## Required local checks after applying

```powershell
python .\scripts\validate_hygiene.py
python .\scripts\build_release_ledger.py
python .\scripts\validate.py
.\scripts\build.ps1
```

Then review:

```text
/
/works/
/works/believe-in-the-badge/
/journal/
/journal/a-hash-is-a-promise/
/journal/the-quiet-work-behind-the-case/
/editions/
/releases/
/roadmap/
```

The next push should allow GitHub Actions to continue past repository hygiene and exercise the release-ledger, source, Hugo, rendered-site, and ledger-diff checks.
