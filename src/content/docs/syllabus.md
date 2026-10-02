---
title: Syllabus
description: Course 1 overview, outcomes, the course map and how each week runs.
tableOfContents:
  maxHeadingLevel: 3
---

<!-- Generated from guide/guide.md by scripts/build_from_guide.py. Edit the guide, not this file. -->

Over 12 live sessions (about 14 calendar weeks, including a self-paced Week 0 and a second capstone week), learners build a production-shaped AI agent harness for supplier invoices, extract a reusable Harness Kernel from it, and apply that kernel to a process from their own work. *No hype, just what works.*

**Who it is for.** Learners who already understand how to build AI agentic workflows and want to develop the mindset of an AI Solutions Architect and Developer. The course uses n8n as its reference workflow tool; the same concepts apply if you come from Make, Zapier, Copilot Studio or similar tools. Class size: 12–15 in the founding cohort. Format: one 2-hour live online session per week, reading posted on the course site three days before, and a weekly assignment done at your own pace.

**The problem this course solves.** Many workflow builders can assemble nodes but cannot say what each one sends, returns or assumes. The course unpacks every abstraction before using it: raw API call first, then LangChain, then LangGraph.

**Why harness design matters.** On the same coding tasks, changing only the harness moved benchmark scores by 27.4 points, against 29.4 points for changing the model (Claw-SWE-Bench, June 2026, as reported in Vizuara's Harness Engineering book). That benchmark measures coding agents, not business workflows, but the lesson carries: the scaffolding around the model is an engineering decision, not an implementation detail.

## What learners build

| Build | Weeks | What it proves |
| --- | --- | --- |
| Harness 1: supplier invoice processing | 1–6 | A single, self-checking graph: invoice PDF → structured invoice → extraction audit → three-way match with purchase order and goods receipt → payment decision |
| Harness Kernel v1 | 7–9 | "Build once, use many times": the reusable core, with the invoice domain plugged in as configuration |
| Capstone: your own domain | 10–11 | The kernel applied, through configuration only, to a small process from your workplace |

Everything runs on one synthetic dataset for a fictional fast-moving consumer goods (FMCG) distributor, created in Week 0.

## By the end, learners can

1. Explain what every step of an agent sends, receives and assumes, down to the API call.
2. Decide which steps need a model and which must be plain code.
3. Build with LangGraph, Pydantic and Claude: typed state, tools, audit loops and human approval.
4. Secure an agent: untrusted input, least privilege, access control, audit trails, financial limits.
5. Test, trace and cost an agent before it ships.
6. Record design decisions as ADRs (architecture decision records) and threats in a threat model.
7. Reuse one kernel for a new domain by writing configuration, not new kernel code.

## Course 1 and Course 2

This is the first of two courses. Course 2 (Harness 2 for distribution, multi-agent coordination, MCP, and deployment to Azure) will be designed from what we learn running Course 1. See [Course 2 (coming later)](/course-2/).

## The course map

Course 1 has a self-paced Week 0, 12 live sessions in two acts and a capstone, and one build week without a session (Week 10b): about 14 calendar weeks in all. Week numbers are used everywhere (pages, recordings, polls, the chatbot); session numbers only appear here. Each act ends at a gate that learners check themselves with their own test runs.

| Session | Week | Focus | Gate |
| --- | --- | --- | --- |
| — | 0 | Set up your tools (self-paced) | Setup self-check passes |
| 1 | 1 | Unpacking the black box |  |
| 2 | 2 | Reading invoices: vision and structured output |  |
| 3 | 3 | Tools and the agent loop by hand |  |
| 4 | 4 | LangGraph fundamentals |  |
| 5 | 5 | Generate, audit, correct |  |
| 6 | 6 | Harness 1 MVP: three-way match and payment decision | **Act 1 gate:** the three worked invoices get the expected decisions |
| 7 | 7 | From notebook to package |  |
| 8 | 7b | Catch-up, a second worked domain, and the capstone brief |  |
| 9 | 8 | Kernel services |  |
| 10 | 9 | Durability, approval, tracing, evaluation | **Act 2 gate:** Harness 1 runs on Kernel v1 and passes its evaluation suite |
| 11 | 10 | Capstone sprint 1: design and the first case running |  |
| — | 10b | Capstone sprint 2: finish, evaluate, secure (build week; optional drop-in clinic) |  |
| 12 | 11 | Capstone reflection | Each learner presents their capstone |

**Act 1 (Weeks 1–6)** builds Harness 1 in notebooks, one layer at a time. **Act 2 (Weeks 7–9)** extracts the reusable kernel and re-platforms Harness 1 on it. **Week 7b** follows Week 7, the hardest transition, so nobody enters the kernel services week behind; it also shows a second, small domain pack running on the same kernel and is where everyone writes their capstone brief. The **capstone** is built over two weeks (10 and 10b).

A calendar note: schedule the course around public holidays (for example Diwali and the year-end break) and quarter-end work peaks. Holiday gaps are added to the calendar as needed; they are not part of the 14 weeks.

## How Course 1 runs

Each week follows the same rhythm: read, discuss, practise. There is no formal grading, no submission and no certificate; learners leave with a portfolio they built and can explain.

### The weekly rhythm

| When | What happens | Where |
| --- | --- | --- |
| 3 days before the session | Reading for the week is posted: concepts, the n8n bridge, and the assignment | Course site |
| Live session (2 hours) | The week's concepts are discussed, with worked examples and the security and design questions | Online, recorded |
| Rest of the week | Learners work through the assignment at their own pace and run the self-check | Colab (Weeks 1–6), Codespaces (Week 7 on) |
| After the week | The reference solution and a checkpoint branch are published, so anyone can compare or catch up | Starter repository |

### The live session

The session discusses concepts rather than marking work. A typical shape:

| Time | Segment | What happens |
| --- | --- | --- |
| 0:00–0:05 | Pulse poll | Did you finish last week's assignment? Where did you get stuck? |
| 0:05–0:20 | Sticking points | The most common problems from the poll, pods and chatbot questions, worked through |
| 0:20–0:55 | Concept + n8n bridge | This week's idea, what it replaces in n8n, and the key code walked through |
| 0:55–1:00 | Break |  |
| 1:00–1:25 | Security lens | The threat this week's build introduces, and how it is stopped |
| 1:25–1:50 | Architect's corner | The week's design decision, discussed in breakout pods, then shared |
| 1:50–2:00 | Assignment briefing | What to build, the minimum viable week, and the stretch options |

### What each week's page contains

- **Reading:** concepts and pre-reads, about 30–45 minutes.
- **Assignment:** numbered **core** steps everyone does, and optional **stretch** steps for those with more time or experience.
- **Self-check:** tests learners run themselves to confirm the core works. Nothing is submitted.
- **Minimum viable week:** the one thing to finish to stay on track in a busy week.
- **Keep for your portfolio:** the ADR, threat-model rows and resource numbers worth keeping.
- **Going deeper:** how production harnesses handle the same problem.

### Support

- **Pods of three**, assigned in Week 0, are the first place to ask for help. Each pod meets for 20 minutes a week on a fixed agenda: each person shows their self-check output and explains, in their own words, one function they wrote. Pods are rebalanced in Week 7b so that no pod has fewer than two active members.
- **Session recordings** for every live session, posted within a day.
- **The course chatbot** (live from Week 3, behind the course sign-in) answers questions from released material at any hour, links to the pages it used, and gives hints before full answers.
- **GitHub Discussions** on the starter repository for technical questions, using a template: what I ran, what I expected, the full error.
- **WhatsApp** for announcements only.
- **Catch-up.** In Weeks 1–6, every week page has an **Open solution in Colab** link once the week closes. From Week 7, `make catch-up WEEK=nn` first saves your work to a backup branch (`my-work-<date>`), then copies in only that week's folders from the published checkpoint and runs `make test`. Nothing you wrote is lost. You rehearse it once in Week 0.

### Recurring threads

- **Predict before you run.** Before executing a cell, write the type, fields and an example value you expect.
- **Self-quiz.** Every reading page ends with two short items: predict an output, and spot what is wrong in a short trace or snippet. Answers are revealed on the page.
- **n8n bridge.** Each week maps a familiar node to its code equivalent, and says what is gained and lost.
- **Security lens.** One threat per week, tied to what was just built, kept in a running threat model.
- **Resource meter.** Every stage reports tokens, cost and latency; each week adds one optimisation and measures its effect.
- **Architect's corner.** One design decision per week, recorded as a short ADR. A worked example of ADR 1 is on the course site, and pods swap ADRs in Weeks 6 and 9.
- **Break it.** A planted failure or attack to find and fix.
- **AI-assisted coding, with understanding.** AI assistants are welcome. Before relying on generated code, explain what each block does to your pod.

### Principles that recur every week

- **Failure becomes information.** A tool error, a denied approval or a crash repair returns to the model as a message, and the loop continues.
- **Code for computation, gated tools for consequences.** Matching and arithmetic live in code; payments and notes go through narrow, approved tools.
- **If it must always happen, it belongs in code, not a prompt.** Guards, masking and audit run as hooks.
- **A confident report is not evidence.** Independent checks decide, never the agent's own summary.
- **Gate on consequence, not activity.** Approve the irreversible steps; asking about every read trains people to rubber-stamp.
- **Capability lives in data.** Rules (`policy.yaml`) and steps (`workflow.yaml`) are configuration; the kernel stays unchanged across domains.
