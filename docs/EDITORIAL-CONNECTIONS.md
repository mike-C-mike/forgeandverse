# Editorial Connections

Forge & Verse pages can connect a practical release, journal piece, studio work, and design study without duplicating the same explanation on every page.

Supported front matter fields:

- `related_release`
- `related_journal`
- `related_study`
- `related_work`

Each value is an internal content route such as:

```yaml
related_study: "/roadmap/bench-status-pad/"
```

The `studio-connections.html` partial resolves the target page and uses its current title and summary. Broken routes fail repository validation.

Use a relationship only when the second page genuinely extends the idea. Do not connect pages merely to increase navigation density.
