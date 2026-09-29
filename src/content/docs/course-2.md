---
title: Course 2 (coming later)
description: What comes after Course 1. Designed from what the founding cohort learns.
sidebar:
  label: Course 2 · coming later
  badge:
    text: Later
    variant: note
---

<!-- Generated from guide/guide.md (Appendix N). -->

Course 2 builds on your Course 1 kernel and capstone: a second, harder harness, multi-agent coordination, and deployment to production on Azure. It is designed from what the founding cohort of Course 1 shows us, so the list below is a draft, not a syllabus.

*This is a parking list, not a syllabus. Course 2 will be redesigned from what the founding cohort shows in Course 1: where learners got stuck, which capstones they built, and the chatbot's question log. The full material is in the 16-week guide (revision 2), kept as the Course 2 source.*

**Likely prerequisite:** Course 1 completed, with a working Kernel v1 and a capstone domain pack.

| Theme | What it covers | Source in the 16-week guide |
| --- | --- | --- |
| Harness 2 | A second, harder domain (distribution) on Kernel v2: multi-step planning, exceptions, partial failure | Old Weeks 10–14 |
| Multi-agent and MCP | Supervisor and specialist agents; MCP servers for tools; MCP vs A2A | Old Week 12 |
| Queues and scale | Storage Queues with KEDA workers; idempotency; back-pressure | Old Week 11 |
| Identity | Entra ID; delegated identity (on-behalf-of: acting for a person); least privilege end to end | Old Week 11 |
| Plan mode | Plan-then-act, with approval of the plan | Old Week 13 |
| Release management | Pinned model and prompt versions; re-run evaluations before upgrades; shadow mode and rollback | Old Week 15 |
| Production on Azure | Container Apps, ACR, Key Vault with managed identity, PostgreSQL Flexible Server, GitHub Actions with OIDC, Bicep, Claude via Microsoft Foundry | Old production thread (Weeks 7–16); deployment in Week 15 |
| Full observability | Four records (logs, traces, metrics, audit) with Application Insights and Log Analytics via OpenTelemetry; dashboards and alerts; incident response | Old production thread (Weeks 7–16) |
| Isolation rings | Process, container and network isolation for tools and code execution; blast-radius design | Old Appendix M and Week 12 |
| Red-team suite | Prompt-injection, privilege-escalation and data-exfiltration tests run in CI | Old Weeks 12 and 15 |
| Skills evaluation | Measuring when a skill helps; skill libraries across domain packs | Old Appendix L and Week 12 |
| Model choice at scale | Routing across tiers; Jev bake-off for classification and risk-gating steps | Old Appendix F |
| Full capstone | Production-grade harness in the learner's own domain, deployed to their own Azure subscription | Old Week 16 |

The Course 1 kernel-gap ADRs (Week 10) are a direct input to Kernel v2.

**Open questions for the Course 2 design:** does it need its own gate at entry; should Azure come first (platform) or last (deployment); can the capstone reuse the Course 1 domain; is a teaching assistant needed at this level.
