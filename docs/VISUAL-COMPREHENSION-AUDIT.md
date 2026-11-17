# Visual Comprehension Audit — Forge & Verse
2026-11-17 · Based on current source templates, content, and image assets. This audit is not a guarantee of live Cloudflare deployment.

## The image test

Before adding a picture, ask: **What will the visitor know after looking that they would otherwise have to read to discover?** A credible product preview, process comparison, scale diagram, or properly captioned documentary scene outranks atmospheric imagery. Avoid decorative filler. Every image must reinforce the professional lane it belongs to, and must not imply that a prototype is already approved or for sale.

## Implemented quick wins (existing verified assets)

1. **The First Collection** (/collection/): current release and development proofs now show on their own work cards where their linked source pages already have images. Concepts with no art or approved design proof remain text-only. Captions distinguish a released file from an in-development image.
2. **Studio overview** (/about/): illustrated three actual formats with source imagery — released Digital Forensics Intake Kit, Examination Notebook interior study, and Believe in the Badge wall-scale study. These images clarify form and use rather than pretending to be finished products.

## Next original image work (prioritized)

| Priority | Page/section | Problem to solve visually | Preferred image or diagram | Grounding and guardrails |
| --- | --- | --- | --- | --- |
| P1 | /materials/ — “Scale is part of the sentence” | “Close / across / passing” is hard to imagine from text | One **same-work** three-panel room-scale diagram, with a person/desk/wall as consistent size references and legibility illustrated at each distance | Relative scale clearly labeled as *illustrative*, not approved final dimensions |
| P1 | /downloads/digital-forensics-intake-request/ — three working formats | The differences between print, fillable, editable are buried in feature text | Three *actual* preview crops: printed handwritten sheet, fillable field highlighted, editable source layout. Put immediately alongside mode choices | Use real file screenshots or verified mockups labeled “demonstration”; no implied compatibility without testing |
| P1 | /ordering-and-fulfillment/ — Design / Proof / Approve / Partner fulfills | The split of studio vs manufacturer is easy to misread | Simple process illustration with **who does what** shown as two swimlanes and a clear checkout handoff boundary | Do not put a fake partner logo, shipping rate, or approved stamp on unfinished work |
| P1 | Professional landing pages — Development / Production / Archive | Users must read three paragraphs to understand lifecycle and gates | Three-stage visual pathway with smaller milestone labels; photo of actual sample only after it exists | “Proof ready” is still Development; only “Available” means orderable |
| P2 | /roadmap/ — five-step workflow | Question / Structure / Material / Sample / Ready can read as a second status system | Compact illustrated *design process* diagram separate from the public product state | Clarify internal workflow vs public availability; do not conflate a mockup with physical sample |
| P2 | /releases/ — file verification | SHA-256 and release ledger feel abstract to nontechnical visitors | Annotated example of downloaded file → compute SHA-256 locally → compare to published digest | Example inputs only; no decorative hashes that could be mistaken for real releases |
| P2 | /works/ — format differences | Four shelves are mainly text headings before product cards | Small documentary-format strip introducing form, notebook, mounted piece, and journal in authentic settings | Current card images already convey individual products; avoid repeating the same photo |
| P2 | /editions/ — material/proof vs approved edition | Beautiful mockups may read as available stock | Side-by-side “screen composition / test PDF / real sample / approved object” evidence sequence | **Never** illustrate “real sample” using a render; wait for actual proof photographs |
| P2 | /disciplines/examiner-bench/ | A luxury tabletop still life is mood-setting but not instructive about forensic *method* | Carefully staged photo of actual bench state, verification step, or notes spread, with neutral identifiers | Avoid implying a mobile acquisition works through a storage write blocker or fabricated screenshots |
| P2 | /disciplines/evidence-room/ | Wax-like seals and antique archive imagery establish a mood but do not represent real custody practice | Documentary photo of proper packaging, accessible shelf organization, transfer/due-action workflow, or inventory reconciliation | Anonymous/fictitious labels; no real case details; real evidence-room procedure from approved practice |
| P2 | /disciplines/watch/ | Reflective officer image conveys character; actual field tools aren't shown until lower on page | Real field-notebook spread and officer handoff/decision context, editorially subtle | No badge props, unlicensed insignia, tactical spectacle, or glamorized confrontation |
| P2 | /disciplines/signal/ | Screen-world image conveys atmosphere but operational outputs are abstract | A clearly fictitious containment/restore checkpoint card paired with the actual pad design | Never imply a real incident, live breach, or actual user infrastructure |
| P3 | /journal/ + /journal/the-horizon/ + /journal/everything-in-moderation/ | Long literary essays have no visual opening, but too many illustrations would interrupt their voice | One unique original editorial image per major essay, plus occasional simple conceptual figure only when explanatory | No stock-lifestyle imagery, no fake biographical scenes; preserve author voice, especially autobiographical passages |
| P3 | /about/ — tactile thinking | Text explains why notebook and ink help but does not demonstrate page usefulness | Actual before/after working note or annotated example spread | Use fictitious case data. Existing notebook pages already support this |
| P3 | /series/ | Text-only series cards may be difficult to distinguish at a glance | One understated consistent cover image per series, not per essay | Avoid bloated repeated thumbnails; series is primarily reading-focused |

## Where NOT to add pictures

- Privacy, use-and-rights, affiliate disclosure, legal terms, file hashes, and release manifests: keep reference data scannable and selectable.
- Every Journal paragraph or product status badge: unnecessary ornament reduces reading speed and risks mobile overload.
- Queued items with no real proof: do not invent finished-looking images solely to make the grid symmetrical.
- Production-approval cues: they must come from a real, documented physical sample.

## Design system rules

- In professional rooms, lead with identifiable practice and truthful objects, not a single black/brass mood applied to everything.
- When the visual teaches a process, captions/labels should be HTML text, not baked into the graphic, for accessibility and mobile rendering.
- Use genuine, accessible alt text. Mark purely decorative background imagery as decorative; do not repeat the heading in the alt.
- Use responsive crops that protect subject and form. Avoid truncating legible text in rendered prototypes.
- Keep real product images linked to their current design files; update them when proofs change. Label early studies accurately.
- For each new image, test in a 390px mobile viewport and a desktop viewport before release, including long names and multiline statuses.
