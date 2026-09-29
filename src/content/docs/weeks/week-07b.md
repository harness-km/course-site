---
title: Week 7b — Catch-up, a second domain and the capstone brief
sidebar:
  label: W7b · Catch-up and capstone brief
week: 7.5
weekLabel: 7b
status: outline
summary: No new kernel content. The week makes sure nobody starts the kernel services week behind, shows that the kernel is not invoice-shaped, and gets every learner's capstone brief written before the two heaviest weeks.
lab:
  path: harness/
  env: codespaces
stretch: One Week 7 stretch item (Docker, CI, prompt assembly); start generating your capstone data with the capstone starter kit (Week 10).
selfCheck: '`make test` passes in your repository; your brief fits the size limit (no more than four steps, exactly one approval).'
mvw: Step 1 and a half-page draft of the brief.
portfolio:
- The capstone brief
---

## Live session: open clinic and a second domain

- 0:00–0:25: the most common Week 7 problems from the pulse poll, pods and chatbot, fixed live
- 0:25–0:55: a second worked domain pack, expense-claim review (read the claim → check it against the expense policy in code → approve, reject or route to a manager), running on the same kernel with no kernel change. What changed: schemas, tools, `policy.yaml`, `workflow.yaml`, prompts, evaluation cases. What did not: anything under `kernel/`
- 0:55–1:00: break
- 1:00–1:40: breakout rooms by need: "my tests don't pass", "Git and Codespaces", "capstone ideas"
- 1:40–2:00: how to pick a capstone: the size limit, examples, and the brief template; pods rebalanced

## Assignment

1. Get Week 7 working: finish its minimum viable week, or run `make catch-up WEEK=07` and read the published solution until you can explain each file.
2. Read `domains/expenses/` side by side with `domains/invoices/`. For each of the six parts, note what differs and why.
3. Write your capstone brief (one page, template on the course site): the process, its users and roles, inputs, the decision, 3–4 steps (one model step, one decision in code, one human approval), the worst thing it could do, and the synthetic data you will generate.

**Stretch:** One Week 7 stretch item (Docker, CI, prompt assembly); start generating your capstone data with the capstone starter kit (Week 10).
