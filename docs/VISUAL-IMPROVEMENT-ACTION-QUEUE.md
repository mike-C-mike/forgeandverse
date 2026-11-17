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

- [ ] **01 · P1 · Materials: show scale with the same piece**
  - **Where:** `/materials/`, “Scale is part of the sentence.”
  - **Design review:** One three-scene comparison of the *same* artwork in a personal office, lab/briefing room, and corridor, with clear relative viewing distances and a readable human/desk reference.
  - **Review question:** Can someone tell why different settings require different sizes and text hierarchy without reading the three descriptions?
  - **Guardrail:** Illustrative scale only; no invented approved dimensions or finished-print claim.
  - **Status:** QUEUED.

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
| 01 | Not started | Awaiting review | — | No |

## Non-negotiable review checks for every item

- User reviews one mockup or concept at a time and can request revisions.
- Do not publish an artwork revision before explicit approval to implement.
- Profession-first fidelity, accurate source imagery and clearly labeled development status.
- Alt text, sufficient contrast, usable captions and legible mobile presentation (~390 px).
- Verify build and rendered content; confirm live deployment only with actual evidence.
