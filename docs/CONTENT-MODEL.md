# Content Model

## Shared purpose fields

Works and Free Works should identify:

- `discipline`: the professional room
- `release_path`: `workbench`, `workspace`, or `editions`
- `release_path_label`: public display label
- `audience`: who the release is made for
- `moment`: the specific working or emotional moment where it belongs
- `need`: the need, behavior, or meaning it addresses
- `format`: the physical or digital form carrying the idea

These fields allow the site to present an item as an answer to a real person rather than a commodity category.

## Works

Works are the selective studio archive. A work may be writing, art, a physical edition, or a useful object that has moved beyond a stray idea and earned a public page.

Required fields:

- `title`
- `summary`
- `discipline`
- `release_path`
- `audience`
- `moment`
- `need`
- `format`
- `format_label`
- `status`
- `rights`

Useful optional fields:

- `featured`
- `cover_style`
- `image`
- `image_alt`
- `series`
- `note`
- `material_intent`
- `external_url`
- `cta_label`
- `partner_name`
- `fulfillment_note`
- `affiliate`

There is no target number of works per discipline or path.

## Journal

Journal entries carry essays, field notes, professional observations, and design thinking. A journal entry can inspire a separate Work entry without automatically becoming one.

## Free Works

Free Works are direct releases. Each page should identify:

- the person served
- the problem solved or reason to keep the file
- what files are included
- intended use
- adaptation permission
- credit expectation
- dimensions or print details
- required local policy, legal, or workflow review
- limitations on redistribution or resale

## Disciplines

Discipline slugs are fixed because they drive filters and related content:

- `examiner-bench`
- `evidence-room`
- `watch`
- `signal`

Purpose paths are:

- `workbench`
- `workspace`
- `editions`

Add a new discipline only when credible work has already created the need for another room.

## Design studies

Current concepts live as Markdown pages under `content/roadmap/`. They are directly linkable, editable, and rendered with the `roadmap/single.html` layout.

Every study requires:

- `title`
- `weight`
- `summary`
- `stage`
- `stage_step`
- `discipline_slug`
- `release_path`
- `format`
- `audience`
- `moment`
- `need`
- `visual`
- `design_test`
- `material_direction`
- `details`

## Prototype-proof metadata

When a study reaches a testable proof, add:

- `card_image`: optimized image used in study cards
- `card_image_alt`: accessible description
- `hero_image`: larger study-page image
- `hero_image_alt`: accessible description
- `prototype_title`: public heading for the proof section
- `prototype_intro`: what the proof is intended to test
- `prototype_images`: list of images with `image`, `alt`, and `caption`
- `open_questions`: the unresolved questions that determine the next pass
- `prototype_source_files`: unpublished repository paths to exact-size PDFs or production proofs

Prototype source files belong under `source-assets/prototypes/`. Only preview images belong under `static/`.

## Study progression

Design studies use `stage_step` from 1 through 5:

1. Question
2. Structure
3. Material
4. Sample
5. Ready

A polished image alone does not justify advancing a study. A sample advances only after it can be tested against the working moment and release standard.
