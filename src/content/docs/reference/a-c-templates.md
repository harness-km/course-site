---
title: A–C. Templates and checklist
description: ADR template, threat-model template and the production-readiness checklist.
sidebar:
  order: 10
---

## A. ADR template

```markdown
# ADR <n>: <decision in one line>
Date:        Status: proposed | accepted | superseded by ADR <m>

## Context
What problem, which constraints (cost, latency, accuracy, compliance, team skills).

## Options considered
1. <option> — pros / cons
2. <option> — pros / cons

## Decision and consequences
What we chose, the single most important reason, what gets harder, and when we would revisit.
```

A worked example, ADR 1 ("SDK or framework for model calls?"), is on the course site.

## B. Threat-model template

Learners add rows as the course goes; each control names the test that proves it. Test stubs are provided in the starter repository.

| Asset | Threat | Category (OWASP LLM / STRIDE) | Entry point | Control | Test that proves it | Residual risk |
| --- | --- | --- | --- | --- | --- | --- |
| Supplier bank details | Changed through a fake invoice | Prompt injection; tampering | Invoice text | Bank details read only from the supplier master; changes need two approvers | `test_bank_detail_change` | Low |
| Payment budget | The same invoice paid twice | Tampering | Re-submitted invoice | Duplicate check + idempotency key | `test_duplicate_invoice` | Low |
| Approval authority | A user approves their own invoice | Excessive agency | Approval step | Approver identity checked by `policy.check`; self-approval refused | `test_self_approval` | Low |

## C. Production-readiness checklist

Reviewed at the Act 2 gate. Items marked (Course 2) are covered when the harness is deployed.

- [ ] Every model output validated against a schema before use
- [ ] All arithmetic and business rules in code, covered by tests
- [ ] Every tool call passes the policy check; read tools use read-only access
- [ ] Guards, masking and audit run as hooks
- [ ] Secrets only in Colab or Codespaces secrets; none in code, config, logs or Git history
- [ ] Side effects are idempotent; retries cannot duplicate them
- [ ] Runs are checkpointed and resumable; approvals pause safely
- [ ] Audit log is append-only and verifiable; every log line carries a run ID
- [ ] Personal data masked in logs and traces
- [ ] Evaluation suite runs with a pass threshold
- [ ] Failure paths fail closed and notify a person
- [ ] ADRs exist for significant decisions; threat model is current
- [ ] Deployment, monitoring, alerts and rollback (Course 2)
