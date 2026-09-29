---
title: F. Choosing the right model
description: The cheapest model that clears each step's accuracy threshold.
sidebar:
  order: 15
---

Choose the cheapest model that meets each step's accuracy threshold on your own test cases, not the one that tops public leaderboards.

| Task type | Examples in Course 1 | Starting choice | Why |
| --- | --- | --- | --- |
| No model needed | Three-way matching, tax checks, duplicate detection | Plain code | Exact, free, testable |
| Classification and routing | Injection check, document-type detection | Haiku | Short outputs; speed and cost matter most |
| Drafting from given facts | Exception notes to suppliers | Haiku | Facts come from code; the model only writes |
| Extraction and structuring | Invoice reading | Sonnet | Vision and schema reliability; errors are costly |
| Independent checking | Extraction audit | Sonnet, or a different model family | Errors must not correlate with the structurer's |
| Judgement on unusual cases | Suspicious invoices | Opus, on escalation only | Deepest reasoning where it pays; rare, so cost stays low |

**Selection method:** set the step's accuracy threshold; build test cases including edge cases and attacks; run candidates cheapest first; record pass rate, cost per correct result and latency; pick the cheapest model that clears the threshold; record the choice in an ADR.

**Optional tier (stretch):** Jev, TypeSafe AI's typed-decision model (released September 2026, early access), answers typed questions with probabilities instead of text. It suits routing and risk scores but is weak at arithmetic and multi-document work. Its speed and cost figures are vendor-reported, so treat it as a bake-off candidate only.
