# Forge & Verse

A local-first Hugo framework for **forgeandverse.com**.

Forge & Verse is an independent design studio creating art, writing, free digital releases, notebooks, and useful objects for people behind consequential work. Digital forensics leads the archive, followed by property and evidence, law-enforcement support, and cybersecurity.

## What is included

- Responsive Hugo layouts with no database or client account system
- Work archive with browser-side discipline filters
- Editorial work pages with state, form, discipline, studio note, and related work
- Journal archive and article layouts
- Free Works archive with functioning direct downloads
- Disciplines page tied dynamically to the work archive
- “On the Anvil” workbench view
- Studio, privacy, use-and-rights, and disclosure pages
- Open Graph metadata, manifest, icons, and social preview art
- Accessibility improvements, reduced-motion support, and keyboard-friendly navigation
- Internal content, voice, rights, and release documentation

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

## Public work states

Front matter uses stable machine values while layouts translate them into public language:

- `concept` → Study
- `forging` → In the studio
- `preview` → Preview
- `released` → Released
- `archived` → Archived

## Discipline slugs

- `examiner-bench`
- `evidence-room`
- `watch`
- `signal`

## External editions

A work page shows no sales button unless `external_url` is populated. When an outside production partner carries a physical edition, add the destination to that field. The studio site remains the canonical page for the work.

## Free releases

Direct-download files belong in `static/downloads/`. Add one or more files to a release page using the `files` front-matter list.

## Source assets

High-resolution originals are retained under `source-assets/`. Web-optimized files live under `static/` so local editing assets are not shipped to the public site.

## Documentation

- `docs/VOICE-AND-TONE.md`
- `docs/CONTENT-MODEL.md`
- `docs/RIGHTS-CHECKLIST.md`
- `docs/RELEASE-CHECKLIST.md`

## Deployment

Deployment is intentionally deferred. When the site is ready, the framework remains compatible with a GitHub-connected static host such as Cloudflare Pages.
