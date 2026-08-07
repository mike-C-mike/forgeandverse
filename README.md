# Forge & Verse v19

A local-first Hugo site for **forgeandverse.com**.

Forge & Verse is an independent design studio creating original art, writing, open operational releases, tactile tools, and physical editions for people behind consequential work. Digital forensics leads the studio, followed by property and evidence, law-enforcement support, and cybersecurity.

## Current foundation

- Static Hugo site with no database, accounts, email gate, or required outside service
- Digital-forensics-first homepage and dedicated pages for four professional disciplines
- Selective Work archive designed to remain intentional without filler
- Complete Digital Forensics Intake Kit with print, fillable, editable, guide, manifest, and checksum paths
- Release Desk with current versions, direct files, SHA-256 values, a machine-readable ledger, and local browser verification
- Filterable Journal and On the Anvil archives
- Search across work, releases, writing, and studies without a database
- Long-form reading tools, breadcrumbs, image lightbox, print support, and reduced-motion behavior
- Testable proof packages for the Bench Status Pad and Examination Notebook
- Restored physical-edition archive with explicit public states and no purchase link before approval
- Repository and rendered-site validation, hygiene checks, and Windows PowerShell workflows
- GitHub Actions validation for every push and pull request

## The four rooms

- **The Examiner's Bench**: digital forensics
- **The Evidence Room**: property and evidence
- **The Watch**: law enforcement and support
- **The Signal**: cybersecurity and defensive technology

Each room may hold useful releases, tactile objects, physical editions, writing, and current studies. Empty paths stay empty until a work earns its place.

## Public studio areas

- `/works/` — complete studio index
- `/downloads/` — open operational releases
- `/releases/` — current release and field-proof ledger
- `/journal/` — essays, practice notes, and studio notes
- `/roadmap/` — work still on the anvil
- `/editions/` — physical-edition archive and availability states
- `/materials/` — material, scale, edge, frame, and mounting approach
- `/disciplines/` — the four professional rooms
- `/about/` — studio background

## Physical edition states

Physical editions use five public states:

1. `in-studio` — composition, scale, surface, or mounting remains unresolved
2. `proof-in-hand` — a real physical sample exists and is being tested
3. `edition-approved` — the physical specification is locked
4. `available` — a current external ordering link is present
5. `resting` — the edition remains archived but is not currently offered

A rendering or room mockup does not count as a physical proof.

When an edition becomes `available`, the work must also define:

- `external_url`
- `partner_name`
- `fulfillment_note`
- `cta_label`

The studio site remains the canonical presentation. The named outside partner handles ordering, production, shipping, and returns.

## Release Desk

The Release Desk separates complete open releases from printable field proofs. It publishes:

- version and update date
- direct bundle link
- SHA-256 value
- file-level machine ledger
- local browser-based hash comparison
- platform-specific verification commands

Rebuild the ledger with:

```powershell
.\scripts\rebuild_release_ledger.ps1
```

## Local development on Windows

The repository looks for `hugo.exe` in the repository root, its parent folder, or `PATH`.

```powershell
.\scripts\dev.ps1
```

Default preview:

```text
http://localhost:1314/
```

Open the priority review set after the server starts:

```powershell
.\scripts\open-review-pages.ps1
```

## Production-style local build

```powershell
.\scripts\build.ps1
```

The build sequence is:

1. repository hygiene audit
2. release-ledger rebuild
3. repository validation
4. Hugo production render
5. rendered-site validation

The generated site is written to `public/`.

## Validation only

Install the Python dependency once:

```powershell
python -m pip install -r .\scripts\requirements.txt
```

Run both source checks:

```powershell
python .\scripts\validate_hygiene.py
python .\scripts\validate.py
```

After Hugo renders:

```powershell
python .\scripts\validate_public.py
```

## Repository hygiene

The repository rejects:

- committed `__pycache__` directories and `.pyc` files
- generated `public/` and Hugo resource output
- duplicate YAML or front-matter keys
- Hugo-reserved `path` front matter
- obsolete rejected releases
- superseded public intake bundles left beside the current release
- physical edition pages without a valid edition block
- `available` editions without production and fulfillment details
- version disagreement between core project files
- stale release hashes and machine-ledger records

See `docs/REPOSITORY-HYGIENE.md`.

## Creating content

```powershell
hugo new works/name-of-work.md
hugo new journal/name-of-entry.md
hugo new downloads/name-of-release.md
hugo new roadmap/name-of-study.md
```

Or use the helper:

```powershell
python .\scripts\new_content.py roadmap "Working Title" --discipline examiner-bench --release-path workbench
```

The archetypes create drafts. A discipline never needs to be padded to look complete.

## Key documentation

- `docs/PRODUCT-MAP.md`
- `docs/CURATION-STANDARD.md`
- `docs/VOICE-AND-TONE.md`
- `docs/CONTENT-MODEL.md`
- `docs/PHYSICAL-EDITION-SYSTEM.md`
- `docs/RIGHTS-CHECKLIST.md`
- `docs/RELEASE-CHECKLIST.md`
- `docs/REPOSITORY-HYGIENE.md`
- `docs/ARCHIVE-POLICY.md`
- `docs/RELEASE-LEDGER.md`
- `docs/FILLABLE-PDF-STANDARD.md`
- `docs/STUDIO-PROOF-STANDARD.md`

## Deployment

Deployment remains deferred. The current priority is local review, physical proof testing, release quality, and a durable studio foundation.
