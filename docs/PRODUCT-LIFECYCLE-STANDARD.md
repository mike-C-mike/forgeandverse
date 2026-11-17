# Product Lifecycle Standard

Status: November 17, 2026

## One vocabulary, distinct professional identities

Forge & Verse gives every profession its own landing page, editorial voice, creative direction, and product mix. **Development, Production, and Archive are shared terminology, not shared product design.** A polished web page does not make a studio prototype a finished product.

The source of truth for public status is data/lifecycle-states.yaml. Hugo resolves existing content metadata using layouts/partials/lifecycle-state.html and displays the public phase and substage using layouts/partials/lifecycle-label.html.

| Public phase | Precise status | Interpretation |
| --- | --- | --- |
| Development | Planned | Listed on a concept map, not yet actively studied |
| Development | Concept | The practitioner need and artistic direction are being established |
| Development | In development | Writing, layout, materials, or functional design are being developed |
| Development | Proof ready | A manufacturing file can be ordered as a test; no physical sample has been evaluated |
| Development | Field proof available | A downloadable prototype can be used for testing, not a final release |
| Development | Physical proof in review | A real physical sample exists and is under evaluation |
| Production | Approved for production | Production specification approved, but ordering may still be unavailable |
| Production | Available | A physical edition has a current ordering path with a named production partner |
| Production | Released | A completed digital/open release is available for use |
| Archive | Archived | Retained for reference, not currently offered |

The label **Production** means an approved production specification or an actually released work, not a promise that finished inventory is sitting in a warehouse. Only **Available** implies a live ordering path for physical editions. **Released** is used for a finished digital or open work.

## Mapping existing content without rewriting history

- The collection map's queued items become Development / Planned.
- A roadmap stage at Question maps to Development / Concept; other active stages remain Development / In development unless more specific evidence exists.
- Roadmap proof_order_ready means Development / Proof ready.
- Roadmap proof_available means Development / Field proof available. Merely hosting files does not prove field testing has occurred.
- Physical edition in-studio means Development / In development.
- Physical edition proof-in-hand means Development / Physical proof in review; use only after a real sample arrives.
- Physical edition edition-approved means Production / Approved for production.
- Physical edition available means Production / Available.
- Physical edition resting means Archive / Archived.
- A complete download with status released means Production / Released.

The five-step study framework (Question, Structure, Material, Sample, Ready) remains an *internal design workflow* rather than a second availability vocabulary. The physical-edition approval gates and partner requirements are unchanged.

## Profession landing page contract

Each page under /disciplines/ must include the following:

1. Its own voice, account of the actual work, and authentic visual direction.
2. A separate **Released & available** area, not mixed into the development shelf.
3. A distinct **In development** area with precise lifecycle labels and no empty catalog padding.
4. Writing and essays kept distinct from merchandise and product status.
5. The same lifecycle explanation across professions.
6. Navigation that respects the four existing professions as separate peers.

A new profession should inherit the *information architecture*, not another profession's creative identity. Product types and quantities are determined by actual needs, not slot counts.

## Gates that must be met before moving a product

- **Proof ready:** manufacturing-specific file and a real test plan.
- **Physical proof in review:** an actual physical sample in hand.
- **Approved for production:** documented material, finish, fit, mounting, quality and rights review.
- **Available:** a current checkout path and named outside production/fulfillment partner.
- **Released:** complete digital/free files and verification appropriate to their use.

No amount of visual polish may replace a stage gate. Every listing must tell the visitor who it serves, what it is, and whether it is still being developed or can really be used or ordered.