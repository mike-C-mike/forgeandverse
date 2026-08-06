# Forge & Verse v14

A local-first Hugo framework for **forgeandverse.com**.

Forge & Verse is an independent design studio creating original art, writing, open operational releases, tactile tools, and useful objects for people behind consequential work. Digital forensics leads the studio, followed by property and evidence, law-enforcement support, and cybersecurity.

## Current foundation

- Responsive Hugo layouts with no database, account system, email gate, or deployment dependency
- Digital-forensics-first homepage built around The Examiner's Bench
- Dedicated pages for all four professional disciplines
- Three internal release paths across every discipline, presented publicly as useful tools, objects for the room, and wall editions
- Selective Work archive designed to remain intentional even when only one piece is public
- Public release pages that explain who a piece serves, what it solves, and how it is meant to be used
- Journal archive and article layouts with essays, practice notes, studio notes, tags, and connected releases
- Static client-side search across work, free releases, journal pieces, and active design studies
- Free Works archive with a complete Digital Forensics Intake Kit, including request form, requester guide, implementation guide, editable source files, bundled release, version history, and SHA-256 manifests
- Visual On the Anvil studies for a small number of credible works in progress
- Prototype-proof galleries for studies that have reached physical or production-ready testing
- Future-ready outside-edition support with production-partner and fulfillment disclosure fields
- Studio, privacy, use-and-rights, material, and disclosure pages
- Open Graph metadata, structured data, manifest, icons, and social preview art
- Accessible navigation, breadcrumbs, image lightbox, reduced-motion support, print rules, and keyboard-friendly interactions
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

The **Digital Forensics Intake Kit v1.1** includes:

- a two-page print-ready intake request PDF
- an editable intake request DOCX
- a one-page requester guide in PDF and editable DOCX
- a four-page implementation guide in PDF and editable DOCX
- a versioned ZIP bundle
- a README, use terms, component checksums, and public SHA-256 manifest
- authority, scope, device, target-data, handling, and acceptance fields
- adaptation, pilot, publication, version-control, and records guidance

The release is a starting framework. It is not a substitute for local policy, legal review, prosecutor requirements, evidence procedures, records obligations, or accessibility review.

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

Prototype PDFs live under `source-assets/prototypes/`. Hugo does not publish that directory. The web-facing site receives only the optimized preview images under `static/images/studies/`.

## Local development on Windows

The repository includes a PowerShell launcher that looks for `hugo.exe` inside the repository, in the repository's parent folder, or on PATH.

From the repository root:

```powershell
.\scripts\dev.ps1
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

## Rebuilding the intake kit guides

The editable companion guides are generated with:

```powershell
python -m pip install -r .\scripts\requirements-docs.txt
python .\scripts\build_intake_kit_documents.py
```

Render and visually inspect the DOCX files before replacing the approved PDFs. After the approved PDFs are in `static/downloads/intake-kit/`, rebuild the ZIP and manifests with:

```powershell
python .\scripts\package_intake_release.py
```

The ZIP checksum changes whenever the archive is rebuilt. Update the release front matter before running validation.

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
