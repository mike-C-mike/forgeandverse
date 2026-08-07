# Forge & Verse v19

This is a consolidation release built from the audited GitHub repository rather than another additive layer.

## Restored and reconciled

- Restored the physical-edition model removed during the Release Desk update.
- Kept the Release Desk, machine ledger, browser hash verification, and release validation.
- Reconnected physical-edition metadata to Work pages.
- Restored `Believe in the Badge` as an `in-studio` physical edition with metal and archival-paper directions.
- Restored edition navigation from Materials and the footer.

## Repository cleanup

- Removed the rejected Verification Desk Card and wallpaper.
- Removed superseded v1.1 intake bundles and obsolete standalone intake duplicates.
- Removed committed Python bytecode and cache directories.
- Expanded `.gitignore` and `.gitattributes`.
- Added `.editorconfig`.
- Repaired duplicate fields in the Work archetype.
- Normalized the framework version to `19.0`.

## Validation and automation

- Added duplicate-key-aware YAML and front-matter checks.
- Added physical-edition metadata validation.
- Added version-alignment checks.
- Added forbidden-file and repository-hygiene checks.
- Added GitHub Actions production validation.
- Added cleanup and environment-doctor scripts.
- Updated build and development scripts to run hygiene validation first.

## Public behavior

The update does not add filler works or announce internal brand strategy. It strengthens the systems already visible to visitors: Work, Editions, Journal, On the Anvil, Free Works, and the Release Desk.

## v19.2 cleanup hotfix

- Fixed invalid YAML quoting in the roadmap archetype that stopped GitHub Actions at the hygiene stage.
- Removed five stale or rejected Work entries so the public Work archive contains only work that meets the current content model.
- Removed `Keeper of the Krapola` from the active repository and added a regression guard preventing it from returning as public Work.
- Kept `A Hash Is a Promise` and `The Quiet Work Behind the Case` in their more appropriate Journal form and completed their Journal type metadata.
- Updated the GitHub Actions checkout and Python setup actions to their Node 24-compatible v6 lines.
- Expanded the hygiene obsolete-file guard to reject the retired Work paths.

The framework remains v19.0; v19.2 identifies the cleanup hotfix applied to that baseline.
