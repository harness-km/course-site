---
title: 'Week 6 — Harness 1 MVP: three-way match and payment decision'
sidebar:
  label: W6 · Harness 1 MVP
week: 6
weekLabel: '6'
status: outline
summary: Learners complete the invoice harness end to end, from invoice PDF to payment decision, with all matching and tax arithmetic in plain Python and a notifier that cannot send twice. This is the Act 1 gate.
outcomes:
- 'Three-way match in a deterministic node: price within tolerance of the PO, billed quantity no more than received quantity, tax recomputed'
- 'Fraud and error checks: duplicate invoices (same supplier and invoice number, or same supplier and amount within 7 days) and bank details that differ from the supplier master'
- 'A decision per line and per invoice: APPROVE, PARTIAL, HOLD or BLOCK, each with reasons'
- Exception notes drafted by Haiku from computed results only, sent through an outbox with an idempotency key
- 'A Gradio screen: upload an invoice, see the decision'
n8nBridge: Chains of IF and Switch nodes with thresholds typed into them → matching rules in code and tolerances in one config file.
lab:
  path: week-06/lab.ipynb
  env: colab
stretch: Build the Gradio screen; write a one-paragraph business case comparing your cost per invoice with the cost of manual AP processing.
security:
  text: Side effects that cannot repeat (a duplicate payment is the costliest accounts-payable error), bank-detail fraud, and outbound notes that must not include other suppliers' data or internal comments.
  category: Tampering; sensitive information disclosure
adr:
  number: 6
  title: What tolerances, and who owns them?
  detail: 'Price and tax tolerances are a policy decision with a business owner, not a prompt tweak. In your pod, swap ADR 6 with a partner and check each other''s against four questions: is the context specific, are there two real options, is the reason the single most important one, and does it say when to revisit?'
breakIt: Let the model do the matching and run 5 invoices (20 as stretch). Count the wrong decisions and the cost.
deeper:
- 'The crash between effect and record: if the process dies after the outbox row is written but before the run records it, the idempotency key makes the replay safe. Week 9''s stretch demonstrates it with a deliberate kill.'
mvw: The three worked invoices get the expected decisions.
portfolio:
- ADR 6
- Threat model v0.6
- Cost per invoice end to end
- A 3-minute screen recording of Harness 1 deciding the three invoices
resource:
  measure: Cost per invoice, end to end
  optimise: Deterministic matching; notes drafted from computed results only
---

## Reading

- Three-way matching explained
- Idempotency
- The course's simplified GST rules (CGST + SGST within a state, IGST between states), teaching rules, not compliance guidance

## Live session

- "Deterministic first": price variance = (billed price − PO price) ÷ PO price, tolerance ±2%; billed quantity ≤ received quantity; tax = taxable value × rate, within ₹1 for rounding
- Code for computation, gated tools for consequences: deciding in code, explaining with a model
- Adapters: an outbox table now, email or an ERP payment queue later, with no change to the graph
- Idempotency keys: a hash of supplier + invoice number

## Assignment

1. Add the `match` node and a `MatchResult` schema per line: price check, quantity check, tax check, reasons.
2. Add `check_duplicates` and `check_bank_details` against the supplier master and past invoices.
3. Add `decide`, then `draft_note` (Haiku), given only the `MatchResult`, never the raw invoice.
4. Add `notify` via `OutboxNotifier`; a second run with the same key must not create a second row.
5. Run the three worked invoices below.

**Stretch:** Build the Gradio screen; write a one-paragraph business case comparing your cost per invoice with the cost of manual AP processing.

## Self-check (Act 1 gate)

| Invoice | Situation | Expected decision |
| --- | --- | --- |
| INV-A | PO-1001: 120 cases × ₹450 + 80 cases × ₹300, all received; 18% GST within the state | APPROVE ₹92,040 (taxable ₹78,000 + CGST ₹7,020 + SGST ₹7,020) |
| INV-B | Same PO; line 2 billed at ₹324, 8% above the PO price | PARTIAL: line 1 approved at ₹63,720; line 2 held for price variance |
| INV-C | Re-submission of INV-A's invoice number | BLOCK as a duplicate; no second outbox message |
