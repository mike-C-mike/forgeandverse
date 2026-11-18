# Forge & Verse — Visual Improvement Action Queue

Created 2026-11-17. Source: [Visual Comprehension Audit](VISUAL-COMPREHENSION-AUDIT.md).

## Working agreement

**One item at a time.** For each item, propose a visual treatment, provide a reviewable design or mockup, receive explicit approval or revisions, then implement the approved version. Do not treat an approved concept as approval to publish. Verify accessibility and mobile presentation before deployment, and record the final URL and review outcome when complete.

**Status labels**
- `QUEUED`: not started; user has not reviewed the proposed art
- `DESIGN REVIEW`: concept/mockup awaiting user feedback
- `REVISING`: incorporating requested tweaks
- `APPROVED FOR IMPLEMENTATION`: visual direction approved, but not yet deployed
- `DEPLOYED / VERIFY`: published, verifying build, accessibility, mobile and live result
- `DONE`: approved result deployed and checked
- `BLOCKED`: requires a real image, source asset, technical validation, or manufacturing proof

Priorities reflect user comprehension, not commercial urgency. Prefer real artifact photographs/previews over atmosphere, and never represent unfinished products as available.

## Previously completed visual pass — retain, don't redo

- [x] **C01 — First Collection: current proof previews**. Used existing source images when a linked release or studio study has one; no invented renders for queued concepts. Commit: `ab175d04`.
- [x] **C02 — Studio: three formats pictured**. Used existing Intake Kit, Examination Notebook interior, and Believe in the Badge room-scale study. Commit: `ab175d04`.

## Review queue

### Immediate — biggest information gain

- [ ] **01 · P1 · Materials: demonstrate what survives at a distance**
  - **Where:** `/materials/`, “Scale is part of the sentence.”
  - **Design review v2:** Replace the generic three-room lifestyle montage with a purposeful typographic reading-distance comparison using the *real typography-led Believe in the Badge development study*. Explain close = full text and nuances; across the room = main line/hierarchy; passing = silhouette/contrast. End with the actual design decision: change typographic hierarchy to match where/how a piece will be seen, not simply enlarge the file.
  - **Review question:** Does this teach a visitor why different viewing situations change the design, instead of just confirming that larger rooms have larger walls?
  - **Guardrail:** Concept image is illustrative, **not** a measured legibility test or an approved production size. Before implementation, replace the illustrative reconstruction with the exact production-study artwork and remove any invented supporting copy; build labels in accessible HTML instead of embedding all copy in raster art.
  - **Status:** UPDATED IN REPOSITORY (2026-11-17) following user feedback that the Close / Med / Far preview looked blank and text-heavy. The original three-room scale-comparison concept is now the source image for the scale interaction, with separate literal scene crops for Close / Med / Far and an accessible link to the complete illustration. The finish-and-lighting module remains unchanged. Build validation and live-site verification are pending.
  - **Current direction:** Tabs `Close / Across the room / In passing`, actual artwork to replace illustrative art, explanatory text beside the artwork, and no unverified fixed distance values. Use mobile-first cards and preserve source wording. Mockup is design-only, not a final site rendering.
  - **Scope decision (2026-11-17):** The Materials page is **educational only**, not a product configurator, shopping assistant, or recommendation engine. Both reading-distance and future Finish & Lighting controls are illustrative demonstrations of design tradeoffs. No implied product availability, measured performance, certified longevity, or promise about any particular vendor finish. Real photographed samples and manufacturer-specific observations can be added *later*, only after actually tested examples exist and receive separate review. This scope is agreed; specific designs and publication are **not yet approved**.
  - **Companion idea for later review:** An adjacent **Finish & Lighting** interactive module, using the same artwork and fixed viewing angle, with a finish selector (Matte / Satin / Gloss) and room-light selector (Soft indirect daylight / Window opposite the art / Overhead spots). Visually model reflection intensity and color/contrast tradeoffs, not physical accuracy. Keep direct-sun **exposure longevity** distinct from reflected glare. Actual results require manufacturer-specific material samples; do not promise that “matte” prevents all glare, UV fading, or direct-sun damage. Keep as a follow-on review after item 01 is approved.

- [ ] **02 · P1 · Digital Forensics Intake Kit: show the three working formats**
  - **Where:** `/downloads/digital-forensics-intake-request/`, beside print/fillable/editable choices.
  - **Design review:** Three faithful crops of the *actual* printable, fillable, and editable release files, with a visible distinction in how each is used.
  - **Review question:** Can the requester choose a format by looking rather than reading instructions?
  - **Guardrail:** Verify each source file before depicting its behavior. No fabricated UI or untested software compatibility.
  - **Status:** QUEUED.

- [ ] **03 · P1 · Ordering: visualize who does what**
  - **Where:** `/ordering-and-fulfillment/`.
  - **Design review:** A two-lane diagram showing Studio responsibilities versus outside production partner responsibilities across Design → Proof → Approve → Fulfillment, with a visible checkout handoff.
  - **Review question:** Is it instantly clear who owns product design versus payment, manufacturing, shipping, and returns?
  - **Guardrail:** No false manufacturing partner, availability, approved stamp, or physical proof imagery.
  - **Status:** QUEUED.

- [ ] **04 · P1 · Professional landing pages: lifecycle without a wall of copy**
  - **Where:** Shared template for all four `/disciplines/` pages.
  - **Design review:** A concise, accessible visual pathway showing **Development → Production → Archive**, with precise status examples such as “Proof ready” and “Available.”
  - **Review question:** Is it obvious that a print-ready test file is *not* an orderable product?
  - **Guardrail:** Retain consistent public terminology across professions while allowing their other imagery to differ.
  - **Status:** QUEUED.

### Profession-specific imagery — give each lane its own space

- [ ] **05 · P2 · Examiner's Bench: show authentic bench practice**
  - **Where:** `/disciplines/examiner-bench/`.
  - **Design review:** Realistic, technically credible bench or note-taking workflow; ideally use actual proof artifacts and verified equipment context.
  - **Review question:** Would a working examiner recognize the method rather than just an expensive-looking desk?
  - **Guardrail:** No incorrect extraction connections, fabricated examiner outputs, or fake evidence identifiers.
  - **Status:** QUEUED.

- [ ] **06 · P2 · Evidence Room: demonstrate stewardship**
  - **Where:** `/disciplines/evidence-room/`.
  - **Design review:** Properly staged packaging, controlled storage, transfer, inventory, or disposition using anonymous fictional labels.
  - **Review question:** Does the visual recognize evidence custodianship rather than generic police branding?
  - **Guardrail:** No actual cases, identifying labels, misleading packaging, or stock “crime scene” props.
  - **Status:** QUEUED.

- [ ] **07 · P2 · The Watch: operational work behind the officer**
  - **Where:** `/disciplines/watch/`.
  - **Design review:** Field notebook/workflow imagery paired with a grounded human moment of judgment, handoff, or reflection.
  - **Review question:** Can officers see their specific work rather than another hero-pose recruitment image?
  - **Guardrail:** No false agency affiliation or dramatic tactical imagery.
  - **Status:** QUEUED.

- [ ] **08 · P2 · The Signal: make resilience tangible**
  - **Where:** `/disciplines/signal/`.
  - **Design review:** Real incident status-pad proof alongside a clearly fictional containment/restore checkpoint scenario.
  - **Review question:** Does the image show a defender's operating problem rather than just glowing monitors?
  - **Guardrail:** No purported real breaches, logs, infrastructure, or proprietary dashboards.
  - **Status:** QUEUED.

### Shared explanations and trust-building

- [ ] **09 · P2 · On the Anvil: make the internal design process visible**
  - **Where:** `/roadmap/`.
  - **Design review:** Compact illustration of Question → Structure → Material → Sample → Ready, visually separate from public Development/Production lifecycle.
  - **Review question:** Is the difference between an idea, a file, and a physical sample obvious?
  - **Guardrail:** Avoid redundant or conflicting status systems.
  - **Status:** QUEUED.

- [ ] **10 · P2 · Release Desk: explain SHA-256 verification**
  - **Where:** `/releases/`.
  - **Design review:** Annotated example of downloaded file → local digest calculation → comparison with the published digest.
  - **Review question:** Could a non-expert follow the process without believing a decorative example hash is a real file checksum?
  - **Guardrail:** Keep genuine hashes selectable and exact. Use unmistakably illustrative examples.
  - **Status:** QUEUED.

- [ ] **11 · P2 · Work index: illustrate the four formats**
  - **Where:** `/works/`.
  - **Design review:** A concise visual strip for useful tools, tactile objects, wall editions, and writing, using approved authentic examples.
  - **Review question:** Are the four paths understandable before the reader reaches the product cards?
  - **Guardrail:** Avoid duplicating every card image or making the index crowded on mobile.
  - **Status:** QUEUED.

- [ ] **12 · P2 · Editions: distinguish mockup, print file, physical proof, and approved edition**
  - **Where:** `/editions/`.
  - **Design review:** Evidence-based visual sequence of what the studio has *actually* completed; leave physical proof and approved-product photo slots absent until legitimate images exist.
  - **Review question:** Can visitors visually distinguish a render from a manufactured object?
  - **Guardrail:** Never substitute a render for a real physical sample.
  - **Status:** BLOCKED for final physical sample imagery; conceptual explanation can be reviewed now.

### Editorial and lower-urgency treatments

- [ ] **13 · P3 · Journal: selective editorial illustrations**
  - **Where:** Journal landing + `/journal/the-horizon/` and `/journal/everything-in-moderation/`.
  - **Design review:** One distinct editorial cover per major essay; optional conceptual figure only if it teaches something.
  - **Review question:** Does the image support the essay's idea without inventing autobiography or turning thoughtful writing into filler?
  - **Status:** QUEUED.

- [ ] **14 · P3 · Studio: demonstrate tactile thinking**
  - **Where:** `/about/`, “Not every thought wants to begin at a keyboard.”
  - **Design review:** Real notebook spread or a before/after annotated writing example using fictitious information.
  - **Review question:** Does the image explain what paper adds to the thinking process?
  - **Status:** QUEUED.

- [ ] **15 · P3 · Series: readable and restrained cover identity**
  - **Where:** `/series/`.
  - **Design review:** A simple recurring identity per essay series, with enough distinction for readers to recognize the series.
  - **Review question:** Is the series easier to find without turning the reading experience into a thumbnail wall?
  - **Status:** QUEUED.

## Approval log

| Item | Current design version | Decision | Requested changes | Publication confirmed |
| --- | --- | --- | --- | --- |
| 01 | Materials interactions v1.1 · Original three-room art drives Close / Med / Far | User requested the first concept image in place of the text-heavy preview; change committed | Validate render and mobile crop; verify Cloudflare deployment | Pending latest build / live site |

## Non-negotiable review checks for every item

- User reviews one mockup or concept at a time and can request revisions.
- Do not publish an artwork revision before explicit approval to implement.
- Profession-first fidelity, accurate source imagery and clearly labeled development status.
- Alt text, sufficient contrast, usable captions and legible mobile presentation (~390 px).
- Verify build and rendered content; confirm live deployment only with actual evidence.
