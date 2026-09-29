---
title: Week 0 — Setup and orientation
sidebar:
  label: W0 · Setup and orientation
week: 0
weekLabel: '0'
status: live
summary: Every learner arrives at Week 1 with working keys, a spend limit, their own repository, the shared course dataset, a first look at Codespaces, and a Python baseline, so the first live session is spent on ideas, not setup.
outcomes:
- A Colab notebook reads the API key from Colab Secrets and gets a reply from Claude
- A monthly spend limit is set in the Anthropic Console
- The learner's own copy of the starter repository exists, with a first notebook saved into it from Colab
- A Codespace has been opened once and the terminal used for `git status` and `make test`
- 'The course dataset is generated and explored: suppliers, SKUs, purchase orders, goods receipts and invoices'
- A self-assessed Python baseline, with the prep pack done if needed
security:
  text: Where API keys must never appear (notebooks, screenshots, Git history, WhatsApp, GitHub Discussions); why a spend limit is a security control; why the course uses synthetic data only, never real supplier, customer or company data.
  category: Unbounded consumption
selfCheck: The last setup cell prints `Secrets OK · Claude reachable · Drive mounted · Dataset OK`, and your repository shows the saved setup notebook.
mvw: Tasks 3–7. Everything else can be finished before Week 2.
portfolio:
- The practice ADR
lab:
  path: week-00/setup.ipynb
  env: colab
---

## Reading

This reading sets up the whole course. It explains what an agent harness is, walks through the business process Harness 1 automates, and covers how the course runs, how to keep your API key safe, and what the offline self-checks can and cannot tell you. Nothing here needs code yet. Read it before you run the setup notebook, so each step makes sense when you get to it.

### What an agent harness is

When people say "the agent", they usually mean the model. The model is one component. It reads text (and images) and writes text back, one request at a time. It cannot open a file, query a database, remember yesterday, ask a manager for approval or notice that it made an arithmetic mistake.

The **harness** is everything around the model that makes it useful and safe:

- **Tools** that let it look things up or act, each with a narrow, defined job.
- **State** that records where a piece of work has got to, so a crash does not lose it.
- **Checks** in plain code that confirm what the model produced before anyone relies on it.
- **Approvals** that pause the work before an irreversible step, such as a payment.
- **Logging and tracing** so you can see afterwards what happened, what it cost and who decided.

In n8n you already build harnesses: the AI node is the model, and the IF branches, Wait nodes and error workflows around it are the harness. In this course you build each piece yourself, in Python, and see what it sends and receives: a raw API call in Week 1, then LangChain, then LangGraph. The aim is not to avoid frameworks. It is to be able to say what a framework does for you, and what it hides.

### Procure-to-pay in one page

Harness 1 automates one slice of a finance process called **procure-to-pay**: everything from deciding to buy something to paying for it. You do not need a finance background; you need to know five documents and one check. The course dataset belongs to a fictional FMCG distributor, **Nilgiri Distributors Pvt Ltd** in Bengaluru, and we will follow one order through it.

1. **Purchase order (PO).** Nilgiri agrees to buy goods at an agreed price. On 18 August 2026 it raised **PO-1001** to Sahyadri Beverages Pvt Ltd (Mysuru): 120 cases of Instant Coffee 100g at ₹450 a case, and 80 cases of Soda Water 500ml at ₹300 a case.
2. **Goods receipt note (GRN).** The warehouse records what actually arrived. **GRN-5001**, dated 23 August, shows all 120 and all 80 cases received.
3. **Supplier invoice.** The supplier asks to be paid. **INV-A** is Sahyadri's invoice SBP/26-27/0412, dated 2 September, quoting PO-1001. It bills ₹54,000 for the coffee and ₹24,000 for the soda water: a taxable value of ₹78,000, plus tax of ₹14,040, for a total of **₹92,040**.
4. **Three-way match.** Before paying, accounts payable checks that the three documents agree: the invoice bills only what was ordered, at the ordered price, and only what was received. For INV-A they all agree.
5. **Payment.** The supplier is paid, into the bank account held in Nilgiri's **supplier master** (its own record of each supplier), never into an account printed on the invoice.

That last rule matters later. Anyone can print a bank account on a PDF. The supplier master is the source of truth, and changing it is a controlled, approved action.

The dataset contains 40 invoices. INV-A is clean; many of the others break one agreement on purpose (a price above the PO, a duplicate, a wrong tax calculation, a changed bank account). By Week 6 your harness will reach the right decision on each.

### GST basics, as a teaching simplification

Indian invoices carry **GST** (Goods and Services Tax). The course uses a simplified version of the rules. It is enough to check arithmetic and spot inconsistencies; it is not compliance guidance.

- When the supplier and the buyer are in the **same state**, the tax is split into two equal halves: **CGST** (central) and **SGST** (state). INV-A is Mysuru to Bengaluru, both Karnataka, at 18%: CGST 9% (₹7,020) plus SGST 9% (₹7,020).
- When they are in **different states**, the whole tax is one **IGST** (integrated) amount. Deccan Personal Care Ltd in Pune (Maharashtra) bills Nilgiri with IGST only.
- Each registered business has a **GSTIN**, a 15-character tax ID. The first two digits are the state code (29 is Karnataka, 27 Maharashtra, 33 Tamil Nadu). The next ten characters follow the shape of a PAN (five letters, four digits, one letter), then one more character, a fixed `Z`, and a final check character. Sahyadri's GSTIN is `29GHTWA4257Z1ZH`; Nilgiri's is `29AAECN4821K1Z6`.

So the first two digits of the supplier's GSTIN, compared with the buyer's, tell you which kind of tax to expect. In Week 2 you will turn the GSTIN shape into a validator.

### How the course runs

The reading is posted three days before each live session and takes 30 to 45 minutes. The session is two hours of discussion, not a lecture: sticking points from the pulse poll first, then the concept, the security question and one design decision. Come having read the page; you do not need to have started the assignment.

The assignment has numbered **core** steps and optional **stretch** steps. The **self-check** is a set of tests you run yourself at the end of a notebook to confirm the core works. The **minimum viable week** names the one thing to finish if work gets busy, so you stay on track without doing everything.

There is no submission, no grading and no certificate. You leave with a portfolio: your code, a short ADR (architecture decision record) each week, a threat model that grows with the build, and your own cost numbers. Your first ADR is a practice one: would you rebuild your favourite n8n workflow in code, and why? Half a page is enough.

Your **pod of three** is the first place to ask for help. In the weekly 20-minute pod meeting, each person shows their self-check output and explains one function they wrote. Explaining your own code is the quickest way to find out whether you understand it, especially if an AI assistant helped write it.

### Keys, spend limits and synthetic data

Your Anthropic API key is a password that spends money. Anyone who has it can run calls on your account until the account stops them. Keep it in exactly one place: **Colab Secrets** now, Codespaces secrets from Week 7. Never paste it into a cell, a screenshot, a WhatsApp message, a GitHub Discussion or a file in your repository. Once a key reaches Git history, treat it as public, even if you delete the file later: the history keeps it, and so does anyone's clone.

A **monthly spend limit** in the Anthropic Console (suggested USD 40, with an alert at USD 20) is a security control, not only a budgeting one. It caps the damage from two failures you cannot fully rule out: a leaked key, and your own agent stuck in a loop calling the model again and again (unbounded consumption). It does not prevent the mistake; it limits what the mistake costs, and the alert tells you early.

The course uses **synthetic data only**. Every supplier, GSTIN and bank account in the dataset is generated from a fixed seed, so everyone has identical data and nobody's real records reach a model provider. Do not substitute real supplier, customer or company data, even in your capstone, where you will generate synthetic cases for your own process. Sending real invoices to an external API is a data-protection decision for your organisation, not for a course notebook.

### What the fake model is, and is not

From Week 1, most self-checks run against a **fake model** included in the course helpers. It never calls the network, costs nothing and gives the same answer every time. It answers from the dataset's answer key: asked to read an invoice, it returns that invoice's known transcription; asked for structured output, it returns the invoice as an ideal reader would extract it.

That makes it good at one job: checking that **your code handles responses correctly**. Does it read the right field, raise an error when a reply is cut off, log a validation failure instead of hiding it?

It is not a model, and it cannot tell you how well real Claude reads a blurred scan or follows your prompt. Real Claude can behave differently, and sometimes will. That is why self-checks accept `live=True` to repeat the check against Claude, and why the setup self-check this week talks to Claude directly: it has to prove your key works.

### Saving your work to GitHub

Colab notebooks live in Google Drive and do not sync to GitHub on their own. When you finish a session of work, use **File → Save a copy in GitHub** and choose your repository and the week's folder (`week-00/setup.ipynb` this week). Each save becomes a commit: your portfolio and your backup. If you forget, your repository shows the old version. From Week 7 you work in Codespaces with Git directly; this week's single visit is a rehearsal, so the terminal, `git status` and `make test` are not new when it matters.

### Self-quiz

**1. Predict the output.** A new invoice arrives from Deccan Personal Care Ltd. Nilgiri's GSTIN starts with `29`.

```python
invoice = {"supplier_gstin": "27EHUUJ8019V1ZC", "taxable_total": 10000, "gst_rate": 18}
same_state = invoice["supplier_gstin"][:2] == "29"
print(same_state)
```

What does the cell print, and which tax amounts (CGST, SGST, IGST) and total should the invoice show?

<details><summary>Answer</summary>

It prints `False`: the supplier's state code is 27 (Maharashtra), not 29 (Karnataka). An inter-state supply carries IGST only, so the invoice should show CGST ₹0, SGST ₹0, IGST ₹1,800 (18% of ₹10,000), and a total of ₹11,800. An invoice from this supplier showing CGST and SGST would be worth a closer look.

</details>

**2. What is wrong with this trace?** A clerk's notes on an invoice for PO-1001:

```text
PO-1001:   Instant Coffee 120 cases @ 450;  Soda Water 80 cases @ 300
Invoice:   Instant Coffee 120 cases @ 450;  Soda Water 80 cases @ 300   total 92,040
GRN:       Instant Coffee 100 cases;        Soda Water 80 cases
Decision:  PO and invoice agree on quantity and price. Approve 92,040.
```

<details><summary>Answer</summary>

The clerk did a two-way match (PO against invoice) and ignored the goods receipt. The GRN shows only 100 cases of coffee arrived, so 20 cases (₹9,000 before tax) are billed but not received. A three-way match would hold the invoice or approve only what was received. Harness 1 has to check all three documents, in code, every time.

</details>

## Assignment

1. Take the readiness self-check on the course site; if unsure, work through the prep pack first.
2. Create or confirm a Google account and open Google Colab.
3. Create a GitHub account. On the `harness-starter` repository, click **Use this template → Create a new repository** to make your own copy.
4. In the Anthropic Console, create an API key and set a monthly spend limit (suggested: USD 40 for Course 1, with an email alert at USD 20).
5. In Colab, open **Secrets** (key icon, left sidebar) → **Add new secret** → name `ANTHROPIC_API_KEY` → paste the key → turn on **Notebook access**.
6. Run `week-00/setup.ipynb`. It mounts Google Drive, generates the course dataset, checks the secret, calls Claude and prints versions.
7. Save the notebook into your repository: **File → Save a copy in GitHub**, choose your repository and the `week-00/` folder. When GitHub asks for authorisation, tick the option to include private repositories. Save again after every edit: Colab does not sync on its own. This is how every Colab assignment is kept.
8. The setup notebook creates `distributor.db` for the course's fictional FMCG distributor (in Codespaces: `make data`): about 500 SKUs, 8 suppliers, purchase orders, goods receipt notes (GRNs) and 40 sample supplier invoices as PDFs. The generator uses a fixed seed, so everyone gets identical data, and it saves the database to your Google Drive so it survives a Colab reset; every lab's first cell re-creates it if it is missing.
9. Work through the dataset tour: pick one purchase order and follow it to what arrived (GRN) and what was billed (invoice).
10. Open your repository in a Codespace once (**Code → Codespaces → Create codespace**), run `git status` and `make test` in the terminal, then make catch-up WEEK=00 as a rehearsal (it saves a backup branch and changes nothing else). Commit anything you changed, then delete the Codespace; Week 7 starts with a fresh one.
11. Join the WhatsApp group (link in your welcome email), meet your pod, and post one goal in the Introductions category of GitHub Discussions.

**Business primer: procure-to-pay in one page.** Purchase order (what we agreed to buy, at what price) → goods receipt (what actually arrived) → supplier invoice (what we are asked to pay) → three-way match (do all three agree?) → payment. Harness 1 automates the invoice-to-payment decision.

**Templates introduced:** the ADR template and the threat-model template (Appendices A and B). Practice ADR: "Why I would or would not rebuild my favourite n8n workflow in code."
