# Search and gallery foundation

## Search

The `/search/` page builds a small JSON index directly from regular Hugo pages in these sections:

- `works`
- `downloads`
- `journal`
- `roadmap`

No database or outside search service is required. The browser scores matches across title, summary, page text, discipline, and content type. Query strings use `?q=` so a search can be bookmarked or shared.

## Work galleries

A work may define a `gallery` list in front matter:

```yaml
gallery:
  - image: /images/studies/example/room.webp
    alt: Clear description of the image
    caption: What this proof is testing
```

Gallery entries are intended for room, scale, surface, material, mounting, edge, and detail studies. They should not be used to pad a page with near-duplicate mockups.

## Prototype galleries

On the Anvil studies continue to use `prototype_images`. Source proofs belong under `source-assets/prototypes/` so they are retained in the repository without being automatically published.

## Lightbox behavior

Any link with `data-lightbox` opens the shared accessible dialog. The linked image remains directly reachable when JavaScript is unavailable.
