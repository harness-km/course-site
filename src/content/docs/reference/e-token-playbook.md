---
title: E. Token optimisation playbook
description: Find the most expensive stage, then pull the lever that fits it.
sidebar:
  order: 14
---

Find the most expensive stage first, then pull the lever that fits it.

| Lever | Cuts | How | Watch out for |
| --- | --- | --- | --- |
| Replace a model step with code | Input + output | Arithmetic, lookups, routing, matching in Python | Only for steps with a definite right answer |
| Right-size the model | Cost per token | Haiku for classification and drafting; Sonnet for extraction and audit; Opus on escalation only | Re-run evaluations after every downgrade |
| Cap and shape output | Output | Set `max_tokens`; ask for schema fields only | A cap that is too low truncates: check the stop reason |
| Prompt caching | Input cost | Put long, unchanging system prompts first and mark them cacheable | Pays off only when the same prefix repeats |
| Send only the state a node needs | Input | Each node receives selected fields, not the whole state | Missing context shows up as quality drops |
| Compact tool results | Input | Return a few named fields, not whole rows | — |
| Shrink images | Input | Render invoice pages at the lowest resolution that keeps digits readable | Too small loses digits |
| Retry budget | Input + output | Cap retries; fix the cause of repeated failures | A cap that is too low fails valid work |

**Resource report (keep weekly):** one row per stage with model, input tokens, output tokens, cached tokens, cost (USD), latency (s) and change since last week, plus a total per run.
