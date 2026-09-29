---
title: H. Evaluating a harness
description: 'Five questions for any harness: correctness, safety, recoverability, observability, cost.'
sidebar:
  order: 17
---

A harness is judged on more than whether the model answered well. Use these five questions at the Week 9 gate and on your capstone; questions 1, 2 and 5 already apply to Harness 1 at the Week 6 gate.

1. **Correctness:** does the eval set (`evals/cases.yaml`) pass at the agreed threshold, including the edge cases you added after Break-its?
2. **Safety:** does every tool call go through `policy.check`, and do the threat-model tests ([Appendix B](/reference/a-c-templates/)) pass, including `test_self_approval`?
3. **Recoverability:** kill the run mid-approval and resume it from the checkpoint. Does it continue without repeating side effects?
4. **Observability:** given a run ID, can you reconstruct what happened from logs, the trace and the audit chain alone ([Appendix M](/reference/m-troubleshooting-runbook/))?
5. **Cost:** tokens and money per run against the budget in the resource thread; the cheapest model tier that still passes the evals.

Stretch: add a model-as-grader check for free-text outputs, and calibrate it against 10 cases you graded by hand before trusting it.
