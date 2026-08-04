# Forge & Verse

A local-first Hugo framework for **forgeandverse.com**.

Forge & Verse is an independent design studio creating original art, writing, free operational releases, notebooks, and useful objects for people behind consequential work. Digital forensics leads the studio, followed by property and evidence, law-enforcement support, and cybersecurity.

## Current foundation

- Responsive Hugo layouts with no database, account system, or email gate
- Selective Work archive built to remain strong even when only one piece is public
- Editorial work pages with form, discipline, material intent, studio note, and optional outside-edition links
- Journal archive and article layouts
- Free Works archive with a functioning digital-forensics intake template
- Disciplines page tied dynamically to the public archive
- On the Anvil view for a small number of credible works in progress
- Studio, privacy, use-and-rights, and disclosure pages
- Open Graph metadata, manifest, icons, and social preview art
- Accessibility support, reduced-motion behavior, and keyboard-friendly navigation
- Internal curation, rights, content, voice, and release documentation

## Included free release

The **Digital Forensics Intake Request** includes:

- a two-page print-ready PDF
- a two-page editable DOCX
- authority, scope, device, target-data, handling, and acceptance fields
- explicit local-adaptation guidance
- permission for internal organizational adaptation and use

The release is intended as a strong starting framework. It is not a substitute for local policy, legal review, or prosecutor requirements.

## Local development

Install Hugo Extended, then run from this directory:

```bash
hugo server -D
```

Open the local address Hugo prints. Draft content appears because of the `-D` flag.

For a production-style local build:

```bash
hugo --gc --minify
```

The generated site will be written to `public/`.

## Content commands

Create a work:

```bash
hugo new works/name-of-work.md
```

Create a journal entry:

```bash
hugo new journal/name-of-entry.md
```

Create a free release:

```bash
hugo new downloads/name-of-release.md
```

The archetypes intentionally create drafts. A category never needs to be padded to look complete.

## Public work states

- `concept` -> Study
- `forging` -> In the studio
- `preview` -> Preview
- `released` -> Released
- `archived` -> Archived

## Discipline slugs

- `examiner-bench`
- `evidence-room`
- `watch`
- `signal`

## External editions

A work page shows no outside-edition button unless `external_url` is populated. When a production partner carries a physical edition, add the destination to that field. The studio site remains the canonical presentation of the work.

## Free releases

Direct-download files belong in `static/downloads/`. A release page should state the problem solved, file formats, intended use, adaptation permission, and any legal or workflow review expected before use.

## Source assets

High-resolution originals are retained under `source-assets/`. Web-optimized files live under `static/` so local editing assets are not shipped unnecessarily.

## Documentation

- `docs/CURATION-STANDARD.md`
- `docs/VOICE-AND-TONE.md`
- `docs/CONTENT-MODEL.md`
- `docs/RIGHTS-CHECKLIST.md`
- `docs/RELEASE-CHECKLIST.md`
- `docs/DIGITAL-FORENSICS-INTAKE-RELEASE-NOTES.md`
- `docs/BENCH-STATUS-PAD-BRIEF.md`

## Deployment

Deployment remains intentionally deferred. The current priority is content, visual review, and a solid local foundation. The framework remains compatible with a GitHub-connected static host later.
