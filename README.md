# Forge & Verse v18.19

A local-first Hugo framework for **forgeandverse.com**.

Forge & Verse is an independent design studio creating original art, writing, open operational releases, tactile tools, and physical editions for people behind consequential work. Digital forensics leads the studio, followed by property and evidence, law-enforcement support, and cybersecurity.

Deployment remains intentionally deferred. The current goal is a durable local foundation, strong work, and honest physical proofs.

## Current foundation

- Static Hugo site with no database, accounts, email gate, or required outside service
- Digital-forensics-first homepage and dedicated pages for four professional disciplines
- Selective Work archive that does not need filler to look complete
- Complete Digital Forensics Intake Kit with printable, fillable, and editable formats
- Filterable Journal and On the Anvil archives
- Static client-side search across work, releases, writing, and studies
- Long-form reading tools, breadcrumbs, image lightbox, print support, and reduced-motion behavior
- Testable proof packages for the Bench Status Pad and Examination Notebook
- Physical-edition archive with explicit public availability states
- Work-page edition specifications for room, reading distance, material, surface, mounting, and format
- Materials page comparing metal and archival-paper presentation
- Open Graph metadata, structured data, icons, RSS, security headers, and social preview art
- Repository and rendered-output validators
- Windows PowerShell development, build, and review scripts

## The four rooms

- **The Examiner's Bench**: digital forensics
- **The Evidence Room**: property and evidence
- **The Watch**: law enforcement and support
- **The Signal**: cybersecurity and defensive technology

Each room can hold useful releases, tactile objects, physical editions, writing, and current studies. Empty paths remain empty until a piece earns its place.

## Public studio areas

- `/works/` — the complete studio index
- `/downloads/` — free operational releases
- `/journal/` — essays, practice notes, and studio notes
- `/roadmap/` — work still on the anvil
- `/editions/` — physical-edition archive and current availability states
- `/materials/` — metal, paper, scale, edge, frame, and mounting approach
- `/disciplines/` — the four professional rooms
- `/about/` — the studio

## Physical edition states

Physical work uses five public states:

1. `in-studio` — physical form is still being resolved
2. `proof-in-hand` — a real physical sample exists and is being tested
3. `edition-approved` — material, size, finish, and mounting are locked
4. `available` — a current external ordering link is present
5. `resting` — the edition remains archived but is not currently offered

A room mockup does not count as a physical proof.

Physical metadata lives in the nested `edition` block on a Work page. See:

- `docs/PHYSICAL-EDITION-SYSTEM.md`
- `docs/CONTENT-MODEL.md`
- `docs/RELEASE-CHECKLIST.md`

When an edition becomes available, the Work must include:

- `external_url`
- `partner_name`
- `fulfillment_note`
- `cta_label`

The studio remains the canonical presentation of the work. The named outside partner handles ordering, production, shipping, and returns.

## Internal release paths

Stable slugs support filtering and related content:

- `workbench` — forms, templates, continuity aids, references, and structured tools
- `workspace` — tactile notebooks, desk objects, and insider pieces
- `editions` — substantial mounted art and physical visual work

Public pages use natural language rather than exposing the internal model as a strategy diagram.

## Included open release

The **Digital Forensics Intake Kit v1.2** includes:

- two-page print-ready PDF
- local fillable PDF with 105 named fields and no automatic submission
- editable DOCX
- requester guide in PDF and DOCX
- implementation guide in PDF and DOCX
- JSON field map
- release manifest and SHA-256 records
- versioned ZIP bundle

The kit is a starting framework. Agencies must review it against local policy, legal requirements, evidence procedures, records obligations, accessibility needs, and approved software.

## Current field proofs

### Bench Status Pad

- exact-size 4 × 6 inch proof
- letter-size two-up print test
- field-test guide and evaluation sheet
- target: restore Monday-morning case context in under thirty seconds

### Examination Notebook

- 12-page, 5.5 × 8.5 inch interior proof
- structured orientation and index pages
- multiple open-note treatments
- field-test guide for writing space, structure, pen response, and re-entry

Source proofs live under `source-assets/prototypes/`. Public test bundles live under `static/downloads/studio-proofs/`.

## Local development on Windows

The launcher looks for `hugo.exe` in the repository, the parent directory, or PATH.

```powershell
.\scripts\dev.ps1
```

Default preview:

```text
http://localhost:1314/
```

Open the priority visual-review pages:

```powershell
.\scripts\open-review-pages.ps1
```

Use another port when needed:

```powershell
.\scripts\dev.ps1 -Port 1320
.\scripts\open-review-pages.ps1 -Port 1320
```

## Production-style local build

```powershell
.\scripts\build.ps1
```

The generated site is written to `public/`. The build script runs repository validation before Hugo and rendered-site validation afterward.

## Validation only

Install the validator dependency once:

```powershell
python -m pip install -r .\scripts\requirements.txt
```

Run:

```powershell
python .\scripts\validate.py
```

The validator checks:

- TOML, YAML, JSON, and front matter parsing
- reserved Hugo fields
- discipline and release-path relationships
- journal types and editorial connections
- physical edition states and nested format specifications
- availability requirements for outside ordering links
- roadmap stages, proof metadata, galleries, and source proofs
- release manifests, hashes, file sizes, PDF signatures, DOCX structure, and ZIP integrity
- static references, internal content routes, template delimiters, and stylesheet braces

After Hugo renders, `scripts/validate_public.py` checks generated links, assets, fragments, duplicate IDs, main landmarks, image alt attributes, and unresolved template markers.

## Creating content

```powershell
hugo new works/name-of-work.md
hugo new journal/name-of-entry.md
hugo new downloads/name-of-release.md
hugo new roadmap/name-of-study.md
```

Or:

```powershell
python .\scripts\new_content.py roadmap "Working Title" --discipline examiner-bench --release-path workbench
```

Archetypes create drafts. A discipline never needs to be padded to look complete.

## Public work states

- `concept` → **Study**
- `forging` → **In the studio**
- `preview` → **Preview**
- `released` → **Released**
- `archived` → **Archived**

These describe the creative work. Physical availability is described separately by the edition state.

## Rebuilding release packages

Intake kit:

```powershell
python -m pip install -r .\scripts\requirements.txt -r .\scripts\requirements-forms.txt
.\scripts\rebuild_intake_release.ps1
```

Include document-guide regeneration:

```powershell
python -m pip install -r .\scripts\requirements-docs.txt
.\scripts\rebuild_intake_release.ps1 -RebuildGuides
```

Studio proof packs:

```powershell
python -m pip install -r .\scripts\requirements-proofs.txt
python .\scripts\build_studio_proof_packs.py
```

Every changed PDF or DOCX must be rendered and visually inspected before its package is treated as approved.

## Source assets

High-resolution originals, production studies, and exact-size proofs live under `source-assets/`. Web-optimized previews and public downloads live under `static/`.

## Key documentation

- `docs/CURATION-STANDARD.md`
- `docs/VOICE-AND-TONE.md`
- `docs/CONTENT-MODEL.md`
- `docs/CONTENT-WORKFLOW.md`
- `docs/PHYSICAL-EDITION-SYSTEM.md`
- `docs/RIGHTS-CHECKLIST.md`
- `docs/RELEASE-CHECKLIST.md`
- `docs/STUDIO-PROOF-STANDARD.md`
- `docs/PROTOTYPE-TESTING.md`
- `docs/FILLABLE-PDF-STANDARD.md`
- `docs/OPEN-RELEASE-PACKAGING.md`
