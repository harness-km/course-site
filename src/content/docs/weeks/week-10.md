---
title: 'Week 10 — Capstone sprint 1: design and the first case running'
sidebar:
  label: W10 · Capstone sprint 1
week: 10
weekLabel: '10'
status: outline
summary: 'Each learner applies Kernel v1 to a small process from their own work by writing a new domain pack, without changing the kernel. The capstone runs over two weeks: in Week 10 one case runs end to end; Week 10b finishes, evaluates and secures it.'
lab:
  path: harness/
  env: codespaces
selfCheck: One case runs end to end; `git diff` shows no changes under `kernel/`.
mvw: Steps 1 and 2, and a `workflow.yaml` whose first step runs.
resource:
  measure: Cost per run in the capstone
  optimise: Stated in the capstone reflection
---

**Good capstone processes** are small, decision-shaped and familiar: a purchase requisition check, the first check in vendor onboarding, customer complaint triage, a leave or overtime approval, a quality-inspection report. Expense-claim review is the Week 7b worked example, so pick something else.

**Size limit:** 3–4 steps, with one model step, one decision made in code and one human approval. If your process is bigger, build its first 3–4 steps and list the rest as next steps.

**Capstone starter kit** (in the starter repository): the `_template` pack, a data-synthesis prompt with a `generate_domain_data.py` template, and the Week 7b `domains/expenses/` pack to copy from.

## What the capstone includes

- A domain pack copied from `_template`: `schemas.py`, `tools.py`, `policy.yaml` (at least two roles), `workflow.yaml`, `prompts/`, and `evals/cases.yaml` with at least 5 cases (10 as stretch)
- Synthetic data only, generated with the starter kit; never confidential company data
- At least three threat-model rows for the domain (five as stretch)
- Two ADRs specific to the domain
- Cost per run from the resource meter

**Kernel gap log.** If your process needs something the kernel cannot do, do not edit `kernel/`. Write it up as an ADR ("Kernel gap: …"), then narrow the scope or work around it in the domain pack. Kernel gaps are direct input to Course 2.

## Live session: architecture clinic

- 0:00–0:20: three capstone briefs discussed in the main room as worked examples
- 0:20–1:30: breakout pods review each other's briefs with four questions: which steps use a model and why; what is the worst thing this harness could do and what stops it; what data you will synthesise; what "done" looks like
- 1:30–2:00: common design problems from the pods, and the plan for the two weeks

## Assignment

1. Copy `_template` into `domains/<your-domain>/`; write the schemas and `policy.yaml`.
2. Generate your synthetic data with the starter kit.
3. Write `workflow.yaml` and the tools, reusing the kernel's models, policy, hooks, approval and evaluation runner.
4. Run one case end to end.
