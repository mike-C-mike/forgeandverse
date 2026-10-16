# Forge & Verse UX Growth Foundation

This document is the design reference for growing Forge & Verse without turning the studio into a generic storefront or a collection of disconnected pages.

## North star

Forge & Verse is an independent design studio with a storefront, not a storefront pretending to be a studio.

Every public surface should help a visitor answer one of five questions quickly:

1. What is this place?
2. Is there something here for someone like me?
3. What can I use, read, test, or buy right now?
4. What is still being developed?
5. Why should I trust the work and the production decision behind it?

The platform should feel editorial, deliberate, practitioner-made, and calm under growth.

## What already works

The current system has several unusually strong foundations:

- The four disciplines are distinct rooms rather than shallow product categories.
- Work is organized by purpose: help with the work, make room for thought, hold the meaning, read the work.
- The Release Desk gives technical releases a level of provenance and verification that fits the audience.
- On the Anvil makes unfinished work legible instead of hiding it.
- Physical-edition states distinguish studio work from proofed and available objects.
- Search, filters, reading tools, breadcrumbs, and strong responsive rules already exist.
- The visual system has a coherent literary-industrial identity: ivory, coal, brass, oxblood, serif display type, restrained geometry.

The next design problem is not “make it prettier.” It is to make the system scale without losing that clarity.

## Information architecture

### Primary navigation

Keep the main navigation intentionally small:

- Work
- Journal
- Disciplines
- On the Anvil
- Studio
- Search

Do not add every new content type to the masthead. Growth should happen below these durable concepts.

### Where new things belong

- **Series** live under Journal and are discoverable through Journal, Search, breadcrumbs, and the footer.
- **Free Works** live under Work and have the Release Desk as the file-first destination.
- **Physical Editions** live under Work and can also be browsed through Editions.
- **Ordering & Fulfillment** belongs under Studio because it explains how Forge & Verse operates.
- New professional audiences should normally become content within an existing discipline before a fifth discipline is created.

This keeps the header stable while the archive grows.

## Discovery model

Visitors should be able to browse the same body of work through three different lenses:

### By purpose

Best for visitors who know what they need.

- Help with the work
- Make room for thought
- Hold the meaning
- Read the work

### By discipline

Best for visitors who identify with a profession.

- The Examiner's Bench
- The Evidence Room
- The Watch
- The Signal

### By state

Best for visitors trying to understand what is usable now.

- Open release
- Field proof
- In the studio
- Proof in hand
- Edition approved
- Available
- Resting

No single page needs to expose every lens at once. The platform should let people move between them without forcing one taxonomy everywhere.

## Commerce and fulfillment

Forge & Verse should not carry inventory merely to keep checkout visually inside the site.

The operating model is:

**Forge & Verse designs -> qualifies the physical configuration -> approves a proof -> sends the customer to the vetted specialist that makes and fulfills that object.**

For every partner-fulfilled item:

- identify the production partner before checkout;
- use “Order this edition,” not “Add to cart,” unless Forge & Verse actually owns the cart;
- state that checkout opens with the production partner;
- show “Studio proof approved” only after the actual configuration has been physically reviewed;
- keep billing, tax, shipping, returns, and transaction support with the partner;
- keep product-specification and quality concerns within Forge & Verse's responsibility.

The production partner is not the brand. The studio's selection and approval judgment is part of the brand.

## Product page hierarchy

A mature physical-product page should read in this order:

1. Work identity and emotional premise
2. Current state
3. Hero photography of the real object once available
4. Intended room / use / reading distance
5. Material and size rationale
6. Studio proof status
7. Production partner
8. Clear external-order CTA
9. Fulfillment disclosure
10. Design / material notes
11. Related studio study or journal writing

Vendor catalog language should never become the dominant voice of the page.

## Long-form writing

Journal remains the main writing archive.

Series are a structural layer over Journal rather than a separate publishing silo. Series essays should still appear in the Journal chronology, while series pages provide ordered reading and a stronger narrative container.

As more series appear:

- keep Series as a Journal feature rather than a permanent new masthead item;
- index series pages in Search;
- show series identity on essay rows;
- support filtering for series essays;
- allow a series to cross disciplines when the subject genuinely does.

## Search

Search should behave like a studio-wide retrieval layer, not merely an article search.

It should index:

- studio work;
- free releases;
- journal writing;
- current studies;
- long-form series;
- discipline landing pages.

Future additions should be indexed unless there is a strong reason not to expose them.

## Component rules

Cards should always answer three things without requiring a click:

1. What is it?
2. What state is it in?
3. Why would I care?

Avoid adding decorative badges unless they communicate state, audience, form, or trust.

Calls to action should be literal:

- View the work
- Open the study
- Read the piece
- Download the release
- Order this edition
- Follow the physical study
- Explore the series

Avoid vague CTAs such as “Learn more” when a more specific action is available.

## Growth constraints

### Header

Do not let the masthead grow taller or accumulate a second permanent row.

### Home

The homepage is an editorial front page, not a complete index. It should feature a few strong current examples and send visitors into durable archive pages.

Do not solve growth by adding one homepage section for every new content type.

### Work

The Work page can remain purpose-led while inventory is small. Once any purpose shelf regularly exceeds roughly 6–8 items, add filtering or a dedicated archive view instead of allowing an endless card wall.

### Journal

The Journal can scale further because list rows are compact. Once the archive becomes materially larger, add year grouping and persistent filter state before adding pagination.

### Disciplines

A discipline should feel inhabited. Do not create a new discipline until it has enough work, writing, or active studies to support a meaningful landing page.

## Visual system

The existing visual identity should remain restrained.

Preserve:

- ivory / paper backgrounds;
- coal / near-black structural bands;
- brass as orientation and craft signal;
- oxblood as a sparing action/accent color;
- serif display typography;
- square corners and architectural borders;
- generous whitespace that serves hierarchy.

Avoid:

- rounded SaaS cards;
- excessive pill badges;
- gradients used only for decoration;
- icon-heavy navigation;
- ecommerce visual clichés;
- oversized empty hero space;
- turning every section dark for drama.

## Accessibility baseline

Maintain:

- visible keyboard focus;
- skip link;
- semantic headings;
- explicit button labels;
- accessible filters with aria-pressed;
- Escape-to-close navigation and dialog behavior;
- descriptive image alt text when the image carries information;
- empty alt text when an image is truly redundant with adjacent text.

Future growth work should add automated accessibility checks rather than rely only on manual review.

## Technical design debt to address deliberately

The CSS currently contains many historical version layers in one large stylesheet. It works, but it will become harder to reason about as the platform expands.

Do not perform a risky wholesale rewrite immediately. Instead, the next structural refactor should migrate toward:

- tokens / base;
- layout primitives;
- shared components;
- content-type components;
- responsive rules colocated with their components where practical.

New components should avoid creating another “v22/v23/v24” pile at the bottom of the same file.

The homepage also contains several direct content references. That is acceptable while curation is highly intentional, but future editorial slots should eventually move to front matter or a small data file so changing the featured work does not require template surgery.

## Growth roadmap

### Phase 1 — discovery and trust

- make Series visible across footer, search, breadcrumbs, and Journal filters;
- make discipline filters data-driven;
- publish Ordering & Fulfillment guidance;
- prepare edition pages for studio-proof and vetted-partner trust signals;
- explain the specialist-production philosophy on Materials.

### Phase 2 — product maturity

- add real product photography;
- add proof-approved metadata;
- add production-partner metadata;
- add direct external order links;
- add material-selection notes;
- add “in the wild” photography after real installations and use.

### Phase 3 — archive scale

Trigger this when the amount of content makes current pages meaningfully harder to scan.

- searchable / filterable Work archive;
- year grouping in Journal;
- more explicit state browsing;
- optional discipline-specific featured works;
- lightweight related-content ranking rather than hand-linking every page.

### Phase 4 — design-system refactor

- split the monolithic stylesheet;
- formalize spacing, type, surface, state, and interaction tokens;
- add component-level regression coverage;
- add automated accessibility and performance budgets.

## Decision rule

When deciding whether to add a new page, navigation item, badge, filter, or component, ask:

**Does this reduce the amount of interpretation a visitor has to do, or does it merely expose more of our internal structure?**

If it only exposes internal structure, keep it out of the interface.
