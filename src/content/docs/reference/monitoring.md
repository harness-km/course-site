---
title: Monitoring and troubleshooting
description: 'Logs, traces and audit: three records, one run ID.'
sidebar:
  order: 5
---

Every run carries one run ID, so any problem can be followed end to end. Course 1 uses three records; Course 2 adds cloud metrics, dashboards and alerts.

| Record | Answers | Built with |
| --- | --- | --- |
| Logs | What happened, in order? | Structured JSON logs from `kernel/telemetry.py` (Week 8) |
| Traces | How did one run flow, including every model call, its tokens and cost? | Langfuse, with personal data masked (Week 9) |
| Audit | Who decided, and were they allowed? | The hash-chained audit log (Week 8) |

The troubleshooting path: logs for the run ID → trace → audit entry → replay the checkpointed run locally ([Appendix M](/reference/m-troubleshooting-runbook/)).
