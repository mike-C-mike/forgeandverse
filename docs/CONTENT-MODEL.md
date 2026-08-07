# Content Model

## Shared purpose fields

Works and Free Works identify:

- `discipline`: professional room
- `release_path`: `workbench`, `workspace`, or `editions`
- `release_path_label`: public display label
- `audience`: who the release is made for
- `moment`: the working or emotional moment where it belongs
- `need`: the need, behavior, or meaning it addresses
- `format`: the physical or digital form carrying the idea

These fields let the site present an item as an answer to a real person rather than a commodity category.

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
- `image_caption`
- `gallery`
- `series`
- `note`
- `material_intent`
- `external_url`
- `cta_label`
- `partner_name`
- `fulfillment_note`
- `affiliate`
- `related_journal`
- `related_release`
- `related_study`
- `related_work`

There is no target number of works per discipline or path.

## Physical editions

A Work with `release_path: editions` must define an `edition` block.

```yaml
edition:
  enabled: true
  state: in-studio
  headline: The work as an object.
  intended_room: Personal offices and shared professional rooms
  reading_distance: Close reading and across-room recognition
  edition_model: Format and edition model still under study
  study_url: /roadmap/example-edition/
  availability_note: No ordering link appears until the physical specification is approved.
  formats:
    - name: Floating metal panel
      status: Under evaluation
      size_direction: Large format; final dimensions pending proof
      surface: Low-gloss or matte surface under evaluation
      mount: Concealed float mount
      fit: Rooms where depth and architectural presence support the work
```

Valid edition states:

1. `in-studio`
2. `proof-in-hand`
3. `edition-approved`
4. `available`
5. `resting`

Use `proof-in-hand` only after a real physical sample exists. A rendering or room mockup remains `in-studio`.

An `available` edition must also define:

- `external_url`
- `partner_name`
- `fulfillment_note`
- `cta_label`

## Journal

Journal entries carry essays, practice notes, professional observations, and studio writing. A journal entry can inspire a separate Work without automatically becoming one.

Supported kinds:

- `practice-note`
- `essay`
- `studio-note`

## Free Works

Free Works are direct operational or creative releases. Each page should identify:

- the person served
- the problem solved or reason to keep the file
- what files are included
- intended use
- adaptation permission
- credit expectation
- dimensions or print details
- required local policy, legal, or workflow review
- limitations on redistribution or resale
- current version and update date
- published SHA-256 values

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

Current concepts live as Markdown pages under `content/roadmap/` and render with `roadmap/single.html`.

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

- `card_image`
- `card_image_alt`
- `hero_image`
- `hero_image_alt`
- `prototype_title`
- `prototype_intro`
- `prototype_images`
- `open_questions`
- `prototype_source_files`

Prototype source files belong under `source-assets/prototypes/`. Only optimized preview images and approved public packages belong under `static/`.

## Study progression

Design studies use `stage_step` from 1 through 5:

1. Question
2. Structure
3. Material
4. Sample
5. Ready

A polished image alone does not justify advancing a study. A sample advances only after it can be tested against the working moment and release standard.
