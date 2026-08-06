# Open Release Packaging

Forge & Verse free operational releases should be packaged as complete, understandable handoffs rather than isolated files.

## Package standard

A substantial operational release should include, when applicable:

- A ready-to-review print PDF
- A fillable PDF when local digital completion adds real value
- An editable source file
- A short guide for the person expected to use or submit it
- Implementation or adaptation notes for the organization adopting it
- A plain-text README
- Clear use and adaptation terms
- Component SHA-256 values
- A machine-readable release manifest when the audience benefits from it
- A versioned bundle
- A public change history

Not every release needs every component. Each included file must have a distinct job.

## Version discipline

- Put the version and update date on the release page.
- Include the version in the bundle filename.
- Keep the public page URL stable when the release is updated.
- Preserve a brief public history of meaningful changes.
- Replace the authoritative bundle, but retain older source history in version control.
- Recalculate checksums after any file changes or package rebuild.

## Website presentation

The release page should answer:

- Who is this for?
- When does it belong in the workflow?
- What need does it fill?
- What is included?
- What should be adapted before use?
- What changed in the current version?
- How can the downloaded files be verified?

The page should not imply that a generic template is automatically compliant with local law, policy, records obligations, evidence procedures, prosecutor expectations, or accessibility requirements.

## Intake kit build order

1. Run `scripts/build_intake_kit_documents.py` to generate the editable guide DOCX files.
2. Render and visually review both DOCX files.
3. Place approved PDF exports beside the DOCX files under `static/downloads/intake-kit/`.
4. Run `scripts/build_fillable_intake_form.py` and `scripts/audit_fillable_intake_form.py`.
5. Run `scripts/package_intake_release.py`.
6. Update the bundle and component checksums in the release front matter if approved files changed.
7. Run `python scripts/validate.py`.
8. Run the full Hugo build and rendered-site validator locally.
