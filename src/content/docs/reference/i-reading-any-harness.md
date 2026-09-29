---
title: I. Reading any harness
description: A checklist for reading an unfamiliar agent codebase or framework.
sidebar:
  order: 18
---

A checklist for reading an unfamiliar agent codebase or framework (used in Architect's corner and whenever you evaluate a framework or vendor product). For each item, find the file and line:

- **The loop:** where does the model get called, and what ends the loop?
- **Tools:** how are tools declared, validated and allow-listed?
- **State:** what is stored between steps, and where is it checkpointed?
- **Control:** where do policy, approvals and hooks sit relative to tool execution?
- **Context:** what goes into each prompt, and how is it trimmed?
- **Failure:** what happens on a bad tool result, a timeout, a refusal?
- **Evidence:** what does it log, trace and audit?

If you cannot find one of these, that is a finding worth an ADR.
