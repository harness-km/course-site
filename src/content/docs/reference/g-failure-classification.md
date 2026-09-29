---
title: G. Failure classification
description: Transient, recoverable and terminal failures, and how the harness responds.
sidebar:
  order: 16
---

Every error the harness meets is sorted into one of three classes before anything else happens. The class decides the response, and the audit log records which class was chosen.

| Class | What it means | Harness response | Course 1 example |
| --- | --- | --- | --- |
| Transient | Likely to succeed if tried again | Retry with backoff and a cap (3 tries), then escalate | Model API rate limit or timeout |
| Recoverable | Fixable by the agent or a person without restarting | Return the error to the model (for example a tool result flagged `is_error`), re-prompt with the validation error, or route to a person via approval | Extracted invoice fails the Pydantic schema; PO number missing; a single policy denial |
| Terminal | Continuing would be unsafe or pointless | Stop the run, keep the checkpoint, alert, write the audit entry | Repeated policy denials in one run; tool not in the allow-list; budget cap reached |

Rules of thumb: never retry a terminal failure; never retry a recoverable one blindly (change something first); every retry is counted against the run's budget. Core in Week 5, where the audit retry cap is a recoverable-failure budget; from Week 8, the policy check returns denials to the model and the audit log records each failure's class.
