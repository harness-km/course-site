---
title: Week 9 — Durability, approval, tracing and evaluation
sidebar:
  label: W9 · Durability and approval
week: 9
weekLabel: '9'
status: outline
summary: 'Learners complete Kernel v1: runs survive crashes and pause for human approval, every run is traced, and one evaluation runner tests any domain. This is the Act 2 gate.'
outcomes:
- Persist graph state with the LangGraph checkpointer; resume after a crash
- Pause for approval with `interrupt`, and resume with the approver's decision
- Keep memory per user and per request with `thread_id`
- Trace runs in Langfuse, with personal data masked
- Run YAML test cases through `kernel/evals.py` and report pass rate, cost and latency
n8nBridge: n8n's Wait node and execution history → checkpointed state with resumable threads; "Simple Memory with a fixed session key" → a thread per user and request.
lab:
  path: harness/
  env: codespaces
stretch: Kill the process between `notify` and the checkpoint and show the idempotency key prevents a second note; swap to the provided PostgreSQL adapter by configuration; expose the harness through a small FastAPI endpoint and call it from one of your own n8n workflows.
selfCheck: '**Act 2 gate:** The evaluation suite passes at least 14 of 15; a crash mid-run resumes correctly; self-approval is refused; the production-readiness checklist for Course 1 (Appendix C) is reviewed.'
security:
  text: Approval fatigue and approver authorisation; one user's memory reaching another; personal data inside traces sent to a third-party service.
  category: Sensitive information disclosure
adr:
  number: 9
  title: What needs human approval?
  detail: Options by amount, risk signal, correction flag, or none. Include the cost of a human minute. Swap ADR 9 with a pod partner and check it against the four questions from Week 6.
breakIt: Two AP users share one memory key. Show the second user seeing the first user's supplier invoice, then fix it.
mvw: Steps 1, 2 and 5.
portfolio:
- The Kernel v1 tag
- Evaluation results
- ADR 9
- Threat model v1.0
resource:
  measure: Token and cost spans in Langfuse traces
  optimise: Prompt caching for long system prompts
---

## Reading

- LangGraph persistence and human-in-the-loop
- Langfuse quick start
- Evaluating a harness (Appendix H)

## Live session

- Durable execution: what Temporal and Azure Durable Functions do at scale, and what the checkpointer gives us now
- Approval as a durable step: propose and pause, stay paused safely, resume with the decision; a rejection's reason goes back to the model
- Logs, traces and audit: three records with three jobs
- Evaluation-driven development: write the test cases before the prompt, keep the checks hidden from the agent, and run each case more than once

## Assignment

1. Add `SqliteSaver`; kill the process mid-run and resume from the last checkpoint.
2. Add `approval.py`: PARTIAL and HOLD decisions, and any invoice above ₹5 lakh, pause for an AP manager; above ₹25 lakh, for the finance controller (teaching limits in `policy.yaml`).
3. Approver identity goes through `policy.check`: nobody approves an invoice they submitted.
4. Connect Langfuse with masking (bank account numbers and GSTINs masked). Given a run ID from a failing case, find the failing step using the runbook (Appendix M).
5. Ten evaluation cases are provided (clean, price variance, quantity over-billing, tax error, duplicate, bank-detail mismatch, injection in invoice text). Write five more of your own, including one attack, and run all 15.

**Stretch:** Kill the process between `notify` and the checkpoint and show the idempotency key prevents a second note; swap to the provided PostgreSQL adapter by configuration; expose the harness through a small FastAPI endpoint and call it from one of your own n8n workflows.
