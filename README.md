# Forge & Verse v18

A local-first Hugo framework for **forgeandverse.com**.

Forge & Verse is an independent design studio creating original art, writing, open operational releases, tactile tools, and useful objects for people behind consequential work. Digital forensics leads the studio, followed by property and evidence, law-enforcement support, and cybersecurity.

## Current foundation

- Responsive Hugo layouts with no database, account system, email gate, or deployment dependency
- Digital-forensics-first homepage built around The Examiner's Bench
- Dedicated pages for all four professional disciplines
- Three internal release paths across every discipline, presented publicly as useful tools, objects for the room, and wall editions
- Selective Work archive designed to remain intentional even when only one piece is public
- Public release pages that explain who a piece serves, what it solves, and how it is meant to be used
- Filterable Journal archive and long-form reading layouts with generated contents, reading progress, print support, tags, and connected releases
- Static client-side search across work, free releases, journal pieces, and active design studies
- A public Release Desk for current open releases and printable field proofs, including versions, direct downloads, SHA-256 values, verification commands, and a local browser-based hash comparison tool
- A deterministic machine-readable release ledger with per-file hashes, byte sizes, media types, and a plain-text checksum manifest
- Free Works archive with a complete Digital Forensics Intake Kit, including request form, requester guide, implementation guide, editable source files, bundled release, version history, and SHA-256 manifests
- Filterable On the Anvil studies with a current-work ledger, visible progression, and a small number of credible works in progress
- Prototype-proof galleries for studies that have reached physical or production-ready testing
- Versioned print-and-use field-test packs for the Bench Status Pad and Examination Notebook, including test protocols, evaluation sheets, and SHA-256 manifests
- Future-ready outside-edition support with production-partner and fulfillment disclosure fields
- Studio, privacy, use-and-rights, material, and disclosure pages
- Open Graph metadata, structured data, manifest, icons, and social preview art
- Accessible navigation, breadcrumbs, image lightbox, reduced-motion support, article reading tools, a global search shortcut, print rules, and keyboard-friendly interactions
- Local repository validation, rendered-site link and HTML validation, plus Windows PowerShell development and build scripts
- Internal curation, rights, content, voice, prototype-testing, physical-format, and release documentation

## The four rooms

- **The Examiner's Bench**: digital forensics
- **The Evidence Room**: property and evidence
- **The Watch**: law enforcement and support
- **The Signal**: cybersecurity and defensive technology

Each room has its own page, language, useful tools, objects for the room, wall editions, related writing, and visible works in progress when they exist.

## Internal release paths

The repository retains stable slugs for filtering and future expansion:

- `workbench`: useful forms, templates, continuity aids, references, and structured tools
- `workspace`: tactile notebooks, desk objects, and insider pieces
- `editions`: substantial mounted art and visual reminders

Public pages use natural language rather than presenting this internal model as a brand strategy.

## Included open release

The **Digital Forensics Intake Kit v1.2** includes:

- a two-page print-ready intake request PDF
- a local-only fillable PDF with 105 named fields and no JavaScript or automatic submission
- an editable intake request DOCX
- a machine-readable JSON field map
- a one-page requester guide in PDF and editable DOCX
- a four-page implementation guide in PDF and editable DOCX
- a versioned ZIP bundle
- a README, release notes, use terms, component checksums, a public SHA-256 manifest, and a machine-readable release manifest
- authority, scope, device, target-data, handling, and acceptance fields
- adaptation, pilot, publication, version-control, and records guidance

The release is a starting framework. It is not a substitute for local policy, legal review, prosecutor requirements, evidence procedures, records obligations, accessibility review, or testing in the agency-approved PDF viewer.


## Release Desk and machine ledger

The public Release Desk is available at:

```text
/releases/
```

It separates finished open releases from field proofs that are still under controlled evaluation. Each entry publishes a version, updated date, direct bundle, and SHA-256 value. The page also includes verification commands for PowerShell, Windows `certutil`, macOS, and Linux.

The page also includes a Web Crypto verifier that calculates SHA-256 in the visitor's browser without uploading the selected file. The machine-readable files are generated from release and proof front matter plus the actual files under `static/`:

```text
/releases/forge-and-verse-release-ledger.json
/releases/forge-and-verse-release-ledger.sha256
```

Rebuild them with:

```powershell
.\scripts\rebuild_release_ledger.ps1
```

The development and production scripts rebuild the ledger before repository validation. Validation fails when a published byte count or SHA-256 value no longer matches the actual file. See `docs/RELEASE-LEDGER.md`.

## Editorial connections

A work can point to the journal piece, free release, or design study that genuinely extends the same idea. Supported front matter fields are:

- `related_release`
- `related_journal`
- `related_study`
- `related_work`

The public site resolves these into a connected reading panel. Repository validation fails broken internal routes. See `docs/EDITORIAL-CONNECTIONS.md`.

## Current prototype proofs

Four On the Anvil studies now include meaningful visual or physical proofs. Two include exact-size working prototypes:

### Bench Status Pad

- exact-size 4 x 6 inch proof
- landscape letter-size two-up print test
- public prototype gallery on the study page
- open questions for handwriting, field priority, and end-of-shift speed

### Examination Notebook

- 12-page, 5.5 x 8.5 inch interior prototype
- case orientation, source index, tool references, open questions, findings index, and pause/resume pages
- multiple open-note treatments for testing ruling and personal preference
- public cover and spread previews on the study page

Prototype source PDFs live under `source-assets/prototypes/`. Hugo does not publish that directory. The approved test copies are packaged separately under `static/downloads/studio-proofs/` with guides, README files, and SHA-256 manifests.

Rebuild both field-test packs with:

```powershell
python -m pip install -r .\scripts\requirements-proofs.txt
python .\scripts\build_studio_proof_packs.py
```

The generated bundle checksums are written to the console. Update the matching roadmap front matter whenever a proof package changes.

## Local development on Windows

The repository includes a PowerShell launcher that looks for `hugo.exe` inside the repository, in the repository's parent folder, or on PATH.

From the repository root:

```powershell
.\scripts\dev.ps1
```

With the server running, open the priority review set with:

```powershell
.\scripts\open-review-pages.ps1
```

The default local address is:

```text
http://localhost:1314/
```

Use another port when needed:

```powershell
.\scripts\dev.ps1 -Port 1320
```

The script runs the local validator when Python and PyYAML are available, then starts Hugo with drafts and future content enabled. The Hugo preview still starts when the optional Python dependency is absent.

## Production-style local build

```powershell
.\scripts\build.ps1
```

The generated site is written to `public/`.

## Validation only

Install the validator dependency once:

```powershell
python -m pip install -r .\scripts\requirements.txt
```

Then run:

```powershell
python .\scripts\validate.py
```

The repository validator checks:

- field-proof metadata, downloadable files, bundle hashes, and ZIP integrity

- TOML, YAML, and front matter parsing
- reserved Hugo front matter fields
- required fields for works, downloads, journal entries, and discipline pages
- discipline and purpose-path references
- roadmap relationships, stages, visual studies, prototype galleries, open questions, and source proofs
- static images, social preview art, roadmap images, and download files
- prototype PDF signatures
- Hugo template delimiter balance
- stylesheet brace balance
- work-gallery and source-proof references

After Hugo builds, `scripts/validate_public.py` also checks generated HTML, internal links, assets, duplicate IDs, unresolved template markers, main landmarks, and image alt attributes.

## Content commands

Create a work:

```powershell
hugo new works/name-of-work.md
```

Create a journal entry:

```powershell
hugo new journal/name-of-entry.md
```

Create a free release:

```powershell
hugo new downloads/name-of-release.md
```

Create an On the Anvil study:

```powershell
hugo new roadmap/name-of-study.md
```

Or use the repository helper, which also fills the discipline and release path:

```powershell
python .\scripts\new_content.py roadmap "Working Title" --discipline examiner-bench --release-path workbench
```

The archetypes create drafts. A discipline never needs to be padded to look complete.

## Public work states

- `concept` becomes **Study**
- `forging` becomes **In the studio**
- `preview` becomes **Preview**
- `released` becomes **Released**
- `archived` becomes **Archived**

## Discipline slugs

- `examiner-bench`
- `evidence-room`
- `watch`
- `signal`

## Purpose path slugs

- `workbench`
- `workspace`
- `editions`

Use `release_path` in front matter. Do not use `path`; Hugo reserves that field.

## Outside editions

A work page shows no outside-edition button until `external_url` is populated. Future physical releases can also define:

- `partner_name`
- `fulfillment_note`
- `affiliate`
- `cta_label`

The studio site remains the canonical presentation of the work while the outside production partner handles the transaction and fulfillment.

## Rebuilding the intake kit

The fillable PDF, field map, bundle, and manifests can be rebuilt with:

```powershell
python -m pip install -r .\scripts\requirements.txt -r .\scripts\requirements-forms.txt
.\scripts\rebuild_intake_release.ps1
```

To regenerate the requester and implementation guides as well, install the document dependency and run:

```powershell
python -m pip install -r .\scripts\requirements-docs.txt
.\scripts\rebuild_intake_release.ps1 -RebuildGuides
```

Every changed DOCX and PDF must be rendered and visually inspected before the updated bundle is treated as approved. The bundle checksum changes whenever the archive is rebuilt. Update release front matter when approved files change.

## Source assets

High-resolution originals and test proofs are retained under `source-assets/`. Web-optimized assets live under `static/` so working files are not published unnecessarily.

## Documentation

- `docs/PRODUCT-MAP.md`
- `docs/CURATION-STANDARD.md`
- `docs/VOICE-AND-TONE.md`
- `docs/CONTENT-MODEL.md`
- `docs/RIGHTS-CHECKLIST.md`
- `docs/RELEASE-CHECKLIST.md`
- `docs/PROTOTYPE-TESTING.md`
- `docs/DIGITAL-FORENSICS-INTAKE-RELEASE-NOTES.md`
- `docs/BENCH-STATUS-PAD-BRIEF.md`
- `docs/EXAMINER-NOTEBOOK-BRIEF.md`
- `docs/PRESERVED-UNTIL-IT-MATTERS-BRIEF.md`
- `docs/STUDIO-STUDIES.md`
- `docs/SEARCH-AND-GALLERIES.md`
- `docs/OPEN-RELEASE-PACKAGING.md`
- `docs/FILLABLE-PDF-STANDARD.md`
- `docs/STUDIO-PROOF-STANDARD.md`
- `docs/CONTENT-WORKFLOW.md`

## Deployment

Deployment remains deferred. The current priority is local content, physical proof review, and a durable studio foundation.

## v13 additions

- Full static studio search with shareable query URLs
- Simplified primary navigation and breadcrumbs
- Accessible image lightbox for previews and proof galleries
- Believe in the Badge composition, room, paper, and edge studies
- Preserved Until It Matters composition and room studies
- Expanded material and reading-distance presentation
- Work-gallery front matter support
- Rendered-site validation after production builds
