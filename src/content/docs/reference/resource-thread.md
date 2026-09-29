---
title: Resource meter
description: Tokens, cost and latency per stage, and one optimisation each week.
sidebar:
  order: 4
---

From Week 1, every model call records its token usage by stage, and each week learners apply one optimisation and measure its effect. Input and output tokens are tracked separately because they are priced differently.

| Week | Measurement added | Optimisation taught |
| --- | --- | --- |
| 1 | Read `usage` on every call; `cost_of(usage, model)` | Cap `max_tokens`; count tokens before sending |
| 2 | Image tokens per invoice page vs text tokens | Render pages at the lowest resolution that keeps digits readable; skip blank pages |
| 3 | Input tokens per agent turn | Compact tool results; see how every turn re-sends the whole history |
| 4 | Tokens and calls per graph node | Replace model-chosen steps with fixed edges |
| 5 | Tokens per audit attempt | Arithmetic and tax checks in Python before the model auditor; retry cap |
| 6 | Cost per invoice, end to end | Deterministic matching; notes drafted from computed results only |
| 7 | Per-stage token budgets in `workflow.yaml` | Budgets as configuration, reviewed like code |
| 8 | Cost meter per stage and model | Model routing: Haiku / Sonnet / Opus by step |
| 9 | Token and cost spans in Langfuse traces | Prompt caching for long system prompts |
| 10 | Cost per run in the capstone | Stated in the capstone reflection |

The optimisation levers and a stage budget worksheet are in Appendix E.
