---
title: Security lens map
description: One threat per week, mapped to the OWASP Top 10 for LLM Applications.
sidebar:
  order: 3
---

Security is taught every week in the context of what was just built. Categories follow the OWASP Top 10 for LLM Applications, plus classic threats where they apply.

| Week | What is built | Security lens | Threat category |
| --- | --- | --- | --- |
| 0 | Accounts, keys, course dataset | Secrets handling, spend limits; synthetic data only | Unbounded consumption |
| 1 | Raw API calls | Keys in notebooks and logs; runaway cost | Secrets exposure; unbounded consumption |
| 2 | Invoice extraction + structured output | Instructions hidden in invoice text; validating output; truncated pages | Prompt injection; improper output handling |
| 3 | Procure-to-pay tools + agent loop | SQL injection; least privilege; a tool's blast radius | Excessive agency; injection |
| 4 | LangGraph | Bounded loops, recursion limits, deterministic routing | Unbounded consumption |
| 5 | Extraction audit loop | A model checking its own reading; a misread digit becomes a wrong payment | Misinformation |
| 6 | Harness 1 MVP | Duplicate payments; bank-detail fraud; data leaking through outbound notes | Tampering; sensitive information disclosure |
| 7 | Package + configuration | Pinned dependencies; secrets outside code; config tampering | Supply chain |
| 8 | Kernel services | Access control in code; two-person approval for bank details; tamper-evident audit log | Excessive agency; system prompt leakage |
| 9 | Checkpoints, approval, tracing | Approval limits and self-approval; one user's memory reaching another; supplier data in traces | Sensitive information disclosure |
| 10 | Capstone | Threat model of each learner's own domain | All categories met so far |
