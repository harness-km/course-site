---
title: 'Week 10b — Capstone sprint 2: finish, evaluate, secure'
sidebar:
  label: W10b · Capstone sprint 2
week: 10.5
weekLabel: 10b
status: outline
summary: A build week with no live session. An optional one-hour drop-in clinic runs mid-week.
lab:
  path: harness/
  env: codespaces
stretch: 10 evaluation cases and five threat-model rows; a Gradio screen for your domain; a skill file (Appendix L) that packages know-how for one step.
selfCheck: '`git diff` shows no changes under `kernel/`; your evaluation cases run and most pass; five quick pokes behave sensibly: a multi-step case, a forbidden action, a malformed input, a crash and resume, and an approval.'
mvw: One case end to end, a policy that refuses one forbidden action, and the demo.
portfolio:
- The capstone domain pack, its evaluation results, threat-model rows and ADRs
---

## Assignment

1. Write at least 5 evaluation cases, including one that tries to break a rule, and run them.
2. Add the approval step and check that a forbidden action is refused at the policy layer.
3. Write the threat-model rows and your two ADRs, plus any kernel-gap ADRs.
4. Call your harness from one of your own n8n workflows through the provided `interfaces/api.py` (about 30 minutes; an example HTTP Request node is provided).
5. Record the cost per run and prepare a 3-minute demo for Week 11.

**Stretch:** 10 evaluation cases and five threat-model rows; a Gradio screen for your domain; a skill file (Appendix L) that packages know-how for one step.
