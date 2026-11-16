---
title: Incident Status Pad
weight: 60
summary: A 5 x 7 continuity pad for keeping incident condition, containment, ownership, next action, and fragile context visible while the screens are already full.
description: A small Signal working-object study for incident response and operational recovery.
stage: Production proof ready
discipline_slug: signal
release_path: workbench
release_path_label: Useful tool
format: 5 x 7 top-glued tear-away pad
audience: Incident responders, system administrators, security analysts, technical leads, and operations staff
need: Preserve the current incident state across interruptions and handoffs without turning a paper pad into the incident system of record
visual: status-pad
design_test: The pad makes the next technical decision easier to recover while avoiding fields that encourage sensitive data or duplicate the incident platform.
material_direction: 5 x 7 uncoated writable stock, top glue, firm chipboard back
details:
- Incident or ticket reference
- Current condition
- Containment or change currently in effect
- Owner or decision maker
- Next action
- Next checkpoint
- Do not change or fragile context
moment: When an incident is active enough that the screen already contains too much to trust to memory.
stage_step: 4
card_image: /images/product-proofs/signal-incident-status-pad-v0.1-5x7-bleed.webp
card_image_alt: A light 5 by 7 Incident Status pad from The Signal.
hero_image: /images/product-proofs/signal-incident-status-pad-v0.1-5x7-bleed.webp
hero_image_alt: The production-ready Incident Status Pad proof.
proof_order_ready: true
proof_order:
  version: "0.1"
  target: 5 x 7 top-glued tear-away pad
  file: source-assets/product-proofs/signal-incident-status-pad-v0.1-5x7-bleed.pdf
  file_label: 5.25 x 7.25 PDF with 0.125 inch bleed
  first_test: 25 to 50 sheets on uncoated writable stock with chipboard back
  test_focus:
  - Whether responders can restore current state in under a minute
  - Whether Do not change captures genuinely fragile context
  - Whether the pad encourages unnecessary sensitive detail
  - Writing space during a realistically messy incident
---

## This is not an incident form

The fastest way to ruin the product would be to reproduce the fields already present in a ticketing platform, SIEM, case system, chat channel, or incident-management tool.

The pad exists for the unstable layer between those systems: what is true right now, which change is holding the situation together, who owns the next decision, and what must not be casually altered.

## A checkpoint matters more than a chronology

The full incident timeline belongs elsewhere.

This object is about re-entry. After a meeting, phone call, shift change, or fifteen-minute detour, can the responder see the current condition and know where the work resumes?

## The next honest gate

Put a real pad on a desk during a simulated incident. If people begin writing passwords, tokens, full logs, or sensitive payloads into it, the prompts need stronger boundaries before it can become a product.
