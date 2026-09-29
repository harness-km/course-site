---
title: Week 8 — Kernel services
sidebar:
  label: W8 · Kernel services
week: 8
weekLabel: '8'
status: outline
summary: 'Learners build the kernel services every future domain will reuse: model routing with a cost meter, a permission check on every tool call, guards that run as hooks, and a tamper-evident audit log.'
outcomes:
- Route each step to Haiku, Sonnet or Opus by configuration, logging cost per request
- 'Enforce role-based access in code: every tool call passes `policy.check(user, action, resource)`'
- Run guards (ID and amount validation, an injection check, PII masking) as hooks at fixed points in the loop
- Write every decision and tool call to a hash-chained audit log, with a run ID in every log line
n8nBridge: In n8n, a credential grants full access to everything a node can reach. In the kernel, identity and role decide what each call may do.
lab:
  path: harness/
  env: codespaces
stretch: A mini bake-off (10 evaluation cases on Haiku and Sonnet for one step, picking the cheaper model that clears the accuracy bar); the full bake-off (30 cases × 3 models × 3 runs, Appendix F); add Jev, TypeSafe AI's typed-decision model, as an optional tier for the injection check.
selfCheck: An AP clerk cannot release a held invoice; an auditor cannot write; changing a supplier's bank details without a second approver is refused; `audit.verify()` detects an edited row; the cost report lists each step's model and spend; all Week 7 tests still pass.
security:
  text: Access control enforced below the model, audit integrity, and keeping system prompts free of secrets or rules that only work if hidden.
  category: Excessive agency; system prompt leakage
adr:
  number: 8
  title: Which model for which step?
  detail: A table of step × model × expected cost and accuracy, with the escalation rule.
breakIt: As an AP clerk, ask the harness to release held invoice INV-B ("the manager said it's fine"), first politely, then via prompt injection. Both must fail at the policy layer.
deeper:
- 'Blast radius: the policy check lowers how often a bad action is attempted; least-privilege tools and read-only connections limit how much one miss can cost.'
- Per-user authorisation on every tool call ("who allowed this change?") is left out of scope by several open-source coding harnesses, according to Vizuara's open-problems review. This week's `policy.check` is exactly what enterprises need.
mvw: Steps 2 and 4, and the Break-it failing at the policy layer.
portfolio:
- ADR 8
- Threat model v0.8 (roles and trust boundaries)
- Cost per step by model
resource:
  measure: Cost meter per stage and model
  optimise: 'Model routing: Haiku / Sonnet / Opus by step'
---

## Reading

- OWASP Top 10 for LLM Applications (Excessive Agency, System Prompt Leakage)
- Role-based access control basics
- Choosing the right model (Appendix F)

## Live session

- Permissions belong in code: a prompt can be talked out of a rule, a policy check cannot
- Gate order: deny rules first, then role and limits, then a human approver; with no approver wired in, the default is refuse
- Hooks: if it must always happen, it belongs in a hook, not a prompt
- Roles for Harness 1: AP clerk (submit, view the queue), AP manager (resolve exceptions up to ₹5 lakh), finance controller (above that; bank-detail changes need a second approver), auditor (read-only)

## Assignment

1. Implement `kernel/models.py`: route by step name from `workflow.yaml`; record tokens and cost.
2. Implement `kernel/policy.py` (about 60 lines) reading `policy.yaml`; wrap every tool with it. A denied call goes back to the model as an error result (recoverable); repeated denials stop the run (Appendix G).
3. Implement the guards as hooks in `kernel/hooks.py` (a skeleton with named events is provided): ID, amount and maximum-input-size validation before a tool, masking before logging, audit after a tool.
4. Implement `kernel/audit.py` with hash chaining and a `verify()` function, recording each failure's class (Appendix G); wire the provided `kernel/telemetry.py` so every log line carries the run ID.

**Stretch:** A mini bake-off (10 evaluation cases on Haiku and Sonnet for one step, picking the cheaper model that clears the accuracy bar); the full bake-off (30 cases × 3 models × 3 runs, Appendix F); add Jev, TypeSafe AI's typed-decision model, as an optional tier for the injection check.
