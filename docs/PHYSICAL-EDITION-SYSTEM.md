# Physical Edition System

Forge & Verse treats a physical edition as a designed object, not a file routed to a vendor.

## Public states

1. `in-studio` — composition, scale, surface, or mounting remains unresolved.
2. `proof-in-hand` — a physical sample exists and is being tested.
3. `edition-approved` — the specification is locked, but availability may still be pending.
4. `available` — a current external ordering link is present.
5. `resting` — the edition remains archived but is no longer actively offered.

A room mockup does not advance a work to `proof-in-hand`. That state requires a real physical sample.

## Required work metadata

Physical works use a nested `edition` block:

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

## Availability requirements

A work using `state: available` must also include:

- `external_url`
- `partner_name`
- `fulfillment_note`
- `cta_label`

The page must make it clear that the outside platform handles ordering, production, shipping, and returns.

## Approval questions

Before an edition moves to `edition-approved`, confirm:

- final dimensions and crop
- reading distance
- material and finish
- edge treatment
- mounting method
- color and black-point behavior
- production tolerances
- packaging and transit protection
- room mockup and real-room review
- rights review
- sample photography
- production partner and customer-service path
