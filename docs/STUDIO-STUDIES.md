# Studio Studies

On the Anvil entries are first-class content pages rather than data-only cards.

Each study must identify:

- the person it serves
- the exact moment or need it addresses
- the intended form
- the material direction
- the standard it must meet before release
- the boundaries that prevent it from becoming clutter or false utility

A study is not a promise that an item will be sold. It is a public record of work that has enough purpose to deserve continued development.

## Content location

Create studies in `content/roadmap/` using the existing pages as patterns.

## Required front matter

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

## When a study reaches proof

Add real preview imagery rather than continuing to rely on decorative CSS mockups.

Required proof fields:

- `card_image`
- `card_image_alt`
- `hero_image`
- `hero_image_alt`
- `prototype_title`
- `prototype_intro`
- `prototype_images`
- `open_questions`
- `prototype_source_files`

The public page shows the proof and the questions still unresolved. Exact-size PDFs remain under `source-assets/prototypes/` so they are available for testing without being published with the site.

Run `python scripts/validate.py` after changes.
