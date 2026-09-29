---
title: M. Troubleshooting runbook
description: 'Logs by run ID, trace, audit, replay: the same four steps every time.'
sidebar:
  order: 22
---

When a run misbehaves, follow the same four steps every time. Every record carries the run ID, so start there. The `make` commands below are provided in the starter repository; logs and the audit chain exist from Week 8, traces from Week 9 and checkpoints from Week 9. Before Week 8, use the printed message array and the resource meter instead.

1. **Logs by run ID.** `grep <run_id> logs/harness.jsonl` (or `make logs RUN=<run_id>`). Find the first `ERROR` or the last step that completed, and note the failure class ([Appendix G](/reference/g-failure-classification/)).
2. **Langfuse trace.** Open the trace for the same run ID. Read the exact prompt, the model's response, token counts and latency for the failing step. Most bugs show up here: a missing field in context, a truncated prompt, a wrong tool argument.
3. **Audit chain.** `make audit RUN=<run_id>` lists the policy decisions, approvals and tool calls in order and verifies the hash chain. Use it to answer "was this action allowed, and who approved it?"
4. **Replay the checkpoint.** `make replay RUN=<run_id> STEP=<n>` reloads the SQLite checkpoint before the failing step and runs it again, with the fake model adapter if you want a repeatable result. Fix, replay, then add the case to `evals/cases.yaml` so it never regresses.

If you are still stuck after 30 minutes: ask the course chatbot, then your pod, with the run ID and what each step showed. Never paste API keys or real data into a question.

| Symptom | First place to look |
| --- | --- |
| `401` / authentication error | Is the Colab or Codespaces secret set and named `ANTHROPIC_API_KEY`? Was the key rotated? (Never in a notebook, YAML file or the repository) |
| Run stops at approval and never resumes | Checkpointer path, thread ID, approval state in SQLite |
| Schema validation keeps failing | Trace: what the model returned vs the Pydantic model |
| Costs jump | Trace token counts; context growth across steps |
| Audit verify fails | Someone edited the log; the chain shows the first broken entry |
