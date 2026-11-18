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

- [x] **01 · P1 · Materials: demonstrate what survives at a distance**
  - **Where:** `/materials/`, “Scale is part of the sentence.”
  - **Design review v2:** Replace the generic three-room lifestyle montage with a purposeful typographic reading-distance comparison using the *real typography-led Believe in the Badge development study*. Explain close = full text and nuances; across the room = main line/hierarchy; passing = silhouette/contrast. End with the actual design decision: change typographic hierarchy to match where/how a piece will be seen, not simply enlarge the file.
  - **Review question:** Does this teach a visitor why different viewing situations change the design, instead of just confirming that larger rooms have larger walls?
  - **Guardrail:** Concept image is illustrative, **not** a measured legibility test or an approved production size. Before implementation, replace the illustrative reconstruction with the exact production-study artwork and remove any invented supporting copy; build labels in accessible HTML instead of embedding all copy in raster art.
  - **Status:** DONE — user reviewed and confirmed the completed Materials interactions working correctly on the live site (November 17, 2026). Correct “What Survives at a Distance?” infographic, scale controls, matching finish-and-lighting art, and consolidated earlier explanations accepted.
  - **Current direction:** Tabs `Close / Across the room / In passing`, actual artwork to replace illustrative art, explanatory text beside the artwork, and no unverified fixed distance values. Use mobile-first cards and preserve source wording. Mockup is design-only, not a final site rendering.
  - **Scope decision (2026-11-17):** The Materials page is **educational only**, not a product configurator, shopping assistant, or recommendation engine. Both reading-distance and future Finish & Lighting controls are illustrative demonstrations of design tradeoffs. No implied product availability, measured performance, certified longevity, or promise about any particular vendor finish. Real photographed samples and manufacturer-specific observations can be added *later*, only after actually tested examples exist and receive separate review. This scope is agreed; specific designs and publication are **not yet approved**.
  - **Companion idea for later review:** An adjacent **Finish & Lighting** interactive module, using the same artwork and fixed viewing angle, with a finish selector (Matte / Satin / Gloss) and room-light selector (Soft indirect daylight / Window opposite the art / Overhead spots). Visually model reflection intensity and color/contrast tradeoffs, not physical accuracy. Keep direct-sun **exposure longevity** distinct from reflected glare. Actual results require manufacturer-specific material samples; do not promise that “matte” prevents all glare, UV fading, or direct-sun damage. Keep as a follow-on review after item 01 is approved.

- [x] **02 · P1 · Digital Forensics Intake Kit: show the three working formats**
  - **Where:** `/downloads/digital-forensics-intake-request/`, beside print/fillable/editable choices.
  - **Design review:** Three faithful crops of the *actual* printable, fillable, and editable release files, with a visible distinction in how each is used.
  - **Review question:** Can the requester choose a format by looking rather than reading instructions?
  - **Guardrail:** Verify each source file before depicting its behavior. No fabricated UI or untested software compatibility.
  - **Status:** DONE — user reviewed the published live Intake Kit visual format comparison and confirmed it is fine (November 17, 2026). Actual Page 1 form and Print / Fillable / Editable choices accepted.

- [x] **03 · P1 · Ordering: visualize who does what**
  - **Where:** `/ordering-and-fulfillment/`.
  - **Design review:** A two-lane diagram showing Studio responsibilities versus outside production partner responsibilities across Design → Proof → Approve → Fulfillment, with a visible checkout handoff.
  - **Review question:** Is it instantly clear who owns product design versus payment, manufacturing, shipping, and returns?
  - **Guardrail:** No false manufacturing partner, availability, approved stamp, or physical proof imagery.
  - **Status:** DONE — user reviewed the live mobile ordering page after its responsive fix and explicitly confirmed Item 03 complete (2026-11-17). Approved process infographic, mobile sizing, and streamlined copy accepted.

- [x] **04 · P1 · Professional landing pages: lifecycle without a wall of copy**
  - **Where:** Shared template for all four `/disciplines/` pages.
  - **Design review:** A concise, accessible visual pathway showing **Development → Production → Archive**, with precise status examples such as “Proof ready” and “Available.”
  - **Review question:** Is it obvious that a print-ready test file is *not* an orderable product?
  - **Guardrail:** Retain consistent public terminology across professions while allowing their other imagery to differ.
  - **Status:** DONE — user reviewed and accepted the illustrated lifecycle guide on the professional landing pages (November 17, 2026). The responsive Development / Production / Archive cards, exact status distinctions, and updated product headings are approved. GitHub production build and rendered-site validation passed.

### Profession-specific imagery — give each lane its own space

- [x] **05 · P2 · Examiner's Bench: show authentic bench practice**
  - **Where:** `/disciplines/examiner-bench/`.
  - **Design review:** Realistic, technically credible bench or note-taking workflow; ideally use actual proof artifacts and verified equipment context.
  - **Review question:** Would a working examiner recognize the method rather than just an expensive-looking desk?
  - **Guardrail:** No incorrect extraction connections, fabricated examiner outputs, or fake evidence identifiers.
  - **Status:** DONE — user confirmed Item 05 complete after reviewing the live Examiner's Bench page (November 17, 2026). Approved “Method over spectacle” imagery and responsive presentation accepted.

- [ ] **06 · P2 · Evidence Room: demonstrate stewardship**
  - **Where:** `/disciplines/evidence-room/`.
  - **Design review:** Properly staged packaging, controlled storage, transfer, inventory, or disposition using anonymous fictional labels.
  - **Review question:** Does the visual recognize evidence custodianship rather than generic police branding?
  - **Guardrail:** No actual cases, identifying labels, misleading packaging, or stock “crime scene” props.
  - **Status:** DEPLOYED / VERIFY — user approved “The Chain That Holds” artwork and requested publication. Optimized desktop/mobile imagery was added in the Evidence Room practice section. Shared profession template now uses per-discipline image labeling and dimensions. GitHub Actions run 44228313051 passed production Hugo build and rendered-site validation. Cloudflare live delivery and user phone review remain unverified; proceed to Item 07 concept work meanwhile.

- [ ] **07 · P2 · The Watch: operational work behind the officer**
  - **Where:** `/disciplines/watch/`.
  - **Design review:** Field notebook/workflow imagery paired with a grounded human moment of judgment, handoff, or reflection.
  - **Review question:** Can officers see their specific work rather than another hero-pose recruitment image?
  - **Guardrail:** No false agency affiliation or dramatic tactical imagery.
  - **Status:** DEPLOYED / VERIFY — user approved the second, male-officer “Between the Calls” scene and requested publication. An optimized desktop/mobile WebP is now used in the Watch practice section, preserving the hero and shared lifecycle guide. The caption clarifies the fictional uniform, patch, location and scenario. GitHub Actions run 44229847206 passed the production Hugo build and rendered-site validator. Cloudflare live delivery and phone review remain pending. The woman-officer study is reserved for a possible later wall edition.

- [ ] **08 · P2 · The Signal: make resilience tangible**
  - **Where:** `/disciplines/signal/`.
  - **Design review:** Real incident status-pad proof alongside a clearly fictional containment/restore checkpoint scenario.
  - **Review question:** Does the image show a defender's operating problem rather than just glowing monitors?
  - **Guardrail:** No purported real breaches, logs, infrastructure, or proprietary dashboards.
  - **Status:** DEPLOYED / VERIFY — user approved “The Quiet Recovery” and directed publication. Optimized desktop and mobile WebP images are in The Signal practice section, with a clear fictional-incident disclaimer. GitHub Actions run 44233690115 passed the production Hugo build and rendered-site validation. Cloudflare deployment and live phone appearance await user verification.

### Shared explanations and trust-building

- [ ] **09 · P2 · On the Anvil: make the internal design process visible**
  - **Where:** `/roadmap/`.
  - **Design review:** Compact illustration of Question → Structure → Material → Sample → Ready, visually separate from public Development/Production lifecycle.
  - **Review question:** Is the difference between an idea, a file, and a physical sample obvious?
  - **Guardrail:** Avoid redundant or conflicting status systems.
  - **Status:** DEPLOYED / VERIFY — user approved the “From an Idea to an Object” five-stage graphic and requested publication. Placed full infographic between collection callout and study listing, removed the redundant text-only five-stage key, and supplied separate readable mobile crops of each approved stage with accessible explanations. Explicit note distinguishes illustrative Status Pad concept and internal design progression from actual product approval / availability. GitHub build and live mobile verification pending.

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
| 01 | v1.2 · Selected What Survives infographic + matching Badge artwork in both interactions | **Accepted by user on live site; complete** | None | **Yes (user verified)** |
| 02 | v1 · Actual intake form and print/fillable/editable choices | **Accepted by user on live site; complete** | None | **Yes (user verified)** |
| 03 | v1.1 · Approved infographic + full-image mobile preview | **Accepted by user on live site; complete** | None | **Yes (user verified)** |
| 04 | v1 · Illustrated HTML lifecycle guide across four professional pages | **Accepted by user; complete** | None | **Yes (user reviewed)** |
| 05 | v1 · Method over spectacle — Examiner's Bench practice artwork | **Accepted by user on live site; complete** | None | **Yes (user verified)** |
| 06 | v1 · The Chain That Holds — evidence custody and storage image | **Approved and pushed** | GitHub build and rendered-site checks passed; verify Cloudflare and mobile presentation | GitHub verified; live review pending |
| 07 | v2 · Male-officer Between the Calls practice scene | **Approved and pushed** | GitHub production build and render checks passed; user to verify mobile | GitHub verified; live review pending |
| 08 | v1 · The Quiet Recovery — security incident restoration practice scene | **Approved and pushed** | Production build and rendered-site validation passed; verify live Cloudflare and phone layout | GitHub passed; live review pending |
| 09 | v1 · From an Idea to an Object — approved five-stage process artwork | **User approved and directed publishing** | Validate build, mobile stage crops and live site | Build pending; live review pending |

## Non-negotiable review checks for every item

- User reviews one mockup or concept at a time and can request revisions.
- Do not publish an artwork revision before explicit approval to implement.
- Profession-first fidelity, accurate source imagery and clearly labeled development status.
- Alt text, sufficient contrast, usable captions and legible mobile presentation (~390 px).
- Verify build and rendered content; confirm live deployment only with actual evidence.
