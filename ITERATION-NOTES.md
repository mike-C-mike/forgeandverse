# Forge & Verse v18.19

This release combines the visual-consolidation round with the first complete physical-edition system.

## Visual consolidation

- Rebalanced split headings so supporting text no longer sits beside oversized display type.
- Reduced maximum hero and detail-page heading sizes while preserving strong editorial hierarchy.
- Standardized section spacing, content width, card gaps, and responsive breakpoints.
- Changed study and work cards to respect their natural content height instead of stretching to the tallest neighbor.
- Reworked journal rows so date and article type read as one metadata group rather than separate columns floating across the page.
- Tightened homepage edition typography, footer hierarchy, mobile spacing, and long-page rhythm.
- Added balanced typography through `text-wrap`, narrower measures, and more consistent heading limits.

## Physical edition system

- Added `/editions/` as a quiet physical-work archive rather than a storefront.
- Added five honest public states: In the studio, Proof in hand, Edition approved, Available, and Resting.
- Added a reusable edition-state partial, edition cards, and a complete work-page edition module.
- Added room, reading-distance, edition-model, material, surface, mounting, and format metadata.
- Added format comparison cards for metal and archival-paper directions.
- Added availability handling that shows no purchase link until a work is explicitly marked Available.
- Added validator rules requiring production-partner and fulfillment details before an edition can become Available.
- Added edition metadata to search and CreativeWork structured data.
- Added physical-edition fields to the Work archetype and documented the approval path.

## First converted work

**Believe in the Badge** now uses the full physical-edition model. It remains **In the studio** because the current images are composition and room studies, not a real physical sample.

The page records two directions under evaluation:

- floating metal panel
- archival paper with substantial mat and frame

No ordering link is shown.

## Content count

- 1 studio work
- 1 complete free release
- 5 journal pieces
- 4 active design studies
- 2 printable field-proof packages
- 1 physical edition in the studio archive
