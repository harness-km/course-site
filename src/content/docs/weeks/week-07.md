---
title: Week 7 — From notebook to package
sidebar:
  label: W7 · Notebook to package
week: 7
weekLabel: '7'
status: outline
summary: Learners move Harness 1 out of a notebook into a Python package in GitHub Codespaces, and separate what is reusable (the kernel) from what is domain-specific (the invoices pack). This is the course's biggest transition, so the hardest code is provided and a catch-up week follows.
outcomes:
- 'Work in the Codespaces container first opened in Week 0: terminal, editor, tests, Git'
- Structure code as `kernel/`, `adapters/`, `interfaces/`, `domains/`
- Move rules, limits and prompts into YAML validated by Pydantic
- Run pytest tests, including the three worked invoices, from the terminal
n8nBridge: n8n credentials, environment variables and workflow settings → Codespaces secrets, a settings module, and version-controlled YAML.
lab:
  path: harness/
  env: codespaces
stretch: A Dockerfile and a GitHub Actions workflow that runs `make test` on every push; assemble the system prompt from parts in `prompts/` (base rules, domain, role); add a second model provider adapter.
selfCheck: '`make test` passes, including the three worked invoices; no domain-specific word ("invoice", "GST", "supplier") appears anywhere in `kernel/`.'
security:
  text: Supply chain and configuration. Pinned versions, secrets never in YAML or Git, and a schema that rejects tampered config (for example a negative cap).
  category: Supply chain
adr:
  number: 7
  title: What goes in the kernel vs the domain pack?
  detail: List 10 items and justify each placement.
breakIt: A config file with a price tolerance of `-1%` and an unknown role. Make the loader refuse to start.
deeper:
- 'The kernel tracker starts this week: list which kernel modules exist and which are still stubs. You will add to it in Weeks 8 and 9.'
mvw: Steps 1–3 and the INV-A test passing.
portfolio:
- ADR 7
- Threat model v0.7
- Your kernel tracker
resource:
  measure: Per-stage token budgets in `workflow.yaml`
  optimise: Budgets as configuration, reviewed like code
---

## Reading

- "ports and adapters" in one page
- The repository layout (The Harness Kernel v1)
- A Git and terminal refresher (branch, commit, push, `make`)

## Live session

- Why notebooks do not scale: hidden state, no tests, no reuse
- The dependency rule: the kernel never imports a domain; domains depend on the kernel
- A walkthrough of the provided `kernel/runtime.py`: how YAML becomes a graph
- Configuration over code: what belongs in YAML and what does not

## Assignment

1. Pull the Week 7 starter into your repository (`make catch-up WEEK=07`), open it in Codespaces and run `make test`; the stub tests pass.
2. Move the Week 6 nodes into `domains/invoices/` (schemas, tools, prompts).
3. Write `domains/invoices/policy.yaml` (price and tax tolerances, duplicate window, decision rules) and `workflow.yaml` (steps, routes).
4. Run Harness 1 through the provided `kernel/runtime.py`, reading the code as you go.
5. Complete the three provided pytest tests for INV-A, INV-B and INV-C.

**Stretch:** A Dockerfile and a GitHub Actions workflow that runs `make test` on every push; assemble the system prompt from parts in `prompts/` (base rules, domain, role); add a second model provider adapter.
