# Forge & Verse — Shared File Proof Thumbnail Cropping Repair

2026-11-17 · Side quest prompted by a phone screenshot of the **A Hash Is a Promise** card.

## Root cause and affected paths

The studio-card and profession-card templates display valid image files but their shared CSS used `object-fit: cover`, forcing complete portrait PDFs/artwork previews into short landscape frames. This can hide nearly all meaningful material while leaving a large dark background visible. The release-card template had the same fit behavior for a document thumbnail.

### Scope of the fix

- `layouts/partials/head.html` loads a small, globally available, fingerprinted `assets/css/proof-card-framing.css` after the other styles.
- The study-card proof class receives a bounded visual row and full `object-fit: contain` artwork, with neutral matting. Compact and related grids retain their smaller row heights.
- `layouts/partials/profession-item-card.html` marks roadmap studies and released digital documents with the scoped `profession-piece-image--proof` class; its proof/document previews use `contain`.
- Release index card document images use `contain`, preserving the entire form or guide thumbnail.
- Content files, actual source images, photo-heavy profession heroes, photographic wall-edition mockups, and actual product status/availability are unchanged.

## Visual checks

On a ~390-pixel phone and desktop, verify these representative cases:
1. `/editions/`: **A Hash Is a Promise** must show the full 8×12 print-test composition inside the card.
2. `/roadmap/`: **Bench Status Pad**, **Examination Notebook**, **Incident Status Pad**, and **A Hash Is a Promise** should no longer cut off the page ends.
3. `/disciplines/examiner-bench/`: portrait studio studies and the Intake Kit release thumbnail should show complete document artwork.
4. `/downloads/`: Intake Kit preview should no longer crop as a background image.
5. `/works/` and `/disciplines/watch/`: photographic work covers should continue to use their intended imagery.

This change addresses fit and frame behavior, **not** the separate Evidence Intake Check Card, which lacks an authored card illustration, or artwork that is inherently sparse. Live Cloudflare and mobile visual inspection must still be confirmed.
