# Content Workflow

## Add a new entry

Use the content helper from the repository root:

```powershell
python .\scripts\new_content.py roadmap "Working Title" --discipline examiner-bench --release-path workbench
```

Supported sections are `works`, `downloads`, `journal`, and `roadmap`.

The helper creates a draft Markdown file from the appropriate archetype and refuses to overwrite an existing entry.

## Before local review

```powershell
python .\scripts\validate.py
.\scripts\dev.ps1
```

## Before packaging a free release

1. Build the source documents.
2. Render PDFs and inspect every page.
3. Package the versioned files and checksum manifest.
4. Update the release front matter.
5. Run repository validation.
6. Run the complete Hugo build and generated-site validation.

## Studio proofs

Rebuild the current proof packs with:

```powershell
python .\scripts\build_studio_proof_packs.py
```

This command regenerates the field-test guides, copies the current prototypes, writes internal checksum manifests, and creates versioned ZIP bundles.

## Rebuild the Digital Forensics Intake Kit

```powershell
.\scripts\rebuild_intake_release.ps1
```

Use `-RebuildGuides` only when the requester or implementation guide source changes. Visually inspect every exported guide page and a representative filled form before publishing the rebuilt package.
