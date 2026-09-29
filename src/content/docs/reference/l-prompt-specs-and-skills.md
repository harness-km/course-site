---
title: L. Prompt specs and skills
description: Prompts treated as code, and when a skill beats a longer prompt.
sidebar:
  order: 21
---

**Prompt specs (stretch from Week 7; recommended for the capstone).** A prompt is treated as code: it lives in `prompts/`, has a version, and is covered by the evaluation set. Each spec file states:

- Purpose (one line) and the model tier it targets
- Inputs it expects and the output schema it must return
- Rules and refusals (what it must never do)
- Two or three worked examples
- A changelog line for every edit, with the eval result before and after

**Skills (stretch, Week 10b).** A skill is a packaged, reusable instruction set the agent loads only when a task needs it (a folder with a `SKILL.md` and optional files). In Course 1 you can write one skill for your capstone domain pack and note in an ADR when a skill is better than a longer system prompt. Evaluating skills systematically is Course 2.
