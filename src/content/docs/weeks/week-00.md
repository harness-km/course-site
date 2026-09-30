---
title: Week 0 — Set up your tools
sidebar:
  label: W0 · Set up your tools
week: 0
weekLabel: '0'
status: live
summary: Every learner arrives at Week 1 with working keys, a spend limit, their own repository, the shared course dataset and a first look at Codespaces, so the first live session is spent on ideas, not setup.
outcomes:
- A Colab notebook reads the API key from Colab Secrets and gets a reply from Claude
- A monthly spend limit and an email alert are set in the Claude Console
- The learner's own private copy of the starter repository exists, with the setup notebook saved into it from Colab
- A Codespace has been opened once and the terminal used for `git status`, `make test` and a commit
- 'The course dataset is generated and explored: suppliers, SKUs, purchase orders, goods receipts and invoices'
security:
  text: Where API keys must never appear (notebooks, screenshots, Git history, WhatsApp, GitHub Discussions); why a spend limit is a security control; why the course uses synthetic data only, never real supplier, customer or company data.
  category: Unbounded consumption
selfCheck: The last setup cell prints `Secrets OK · Claude reachable · Drive mounted · Dataset OK`, and your repository shows the saved setup notebook.
mvw: Steps 2–7. Everything else can be finished before Week 2.
portfolio:
- The practice ADR
lab:
  path: week-00/setup.ipynb
  env: colab
---

## Reading

This week you set up the tools for the whole course. Nothing is installed on your computer: everything runs in the browser. Plan on <span class="key">1–2 hours</span>. Read this page first, then work through the assignment below.

### What lives where

<!-- figure: week-00/step-01-where (designed after this page is approved) -->

Each tool holds one thing. If you know where something lives, you know where to look when it goes wrong.

- **Colab** runs your notebooks, Weeks 1–6.
- **Google Drive** holds the course dataset, so it survives a Colab reset.
- **GitHub** holds your saved work, in your own <span class="key">private</span> repository.
- **Colab Secrets** holds your API key. Nowhere else.
- **Claude Console** holds your spend limit and billing.
- **Codespaces** (VS Code in the browser) replaces Colab from <span class="key">Week 7</span>. You open it once this week as a rehearsal.

Local VS Code is optional. Nothing in the course needs it.

### Tools and costs

Each tool links to the step where you set it up.

| Tool | What it is for | Weeks | Setup time (estimate) | Cost |
| --- | --- | --- | --- | --- |
| [Google account, Colab](#step-1-google-account-and-colab) | Runs notebooks | 0–6 | 5 min | Free |
| [Google Drive](#step-6-run-the-setup-notebook) | Holds the dataset | 0–6 | none | Free |
| [GitHub](#step-2-github-account) | Saves your work | 0–11 | 10 min | Free |
| [GitHub Discussions](#step-9-meet-your-group) | Questions and answers | 0–11 | 2 min | Free |
| [Claude Console, API key](#step-3-claude-account-and-spend-limit) | Calls to Claude; spend limit | 0–11 | 15 min | About USD 15–30 for the course (estimate) |
| [Colab Secrets](#step-5-create-your-key-and-add-it-to-colab) | Holds the key | 0–6 | 2 min | Free |
| [Codespaces](#step-8-try-codespaces-once) | VS Code in the browser | 0, then 7–11 | 10 min | Free within 120 core-hours a month (about 60 hours on 2 cores) |
| [Langfuse](/weeks/week-09/) | Tracing | 9–11 | Set up in Week 9 | Hobby plan free |
| [WhatsApp](#step-9-meet-your-group) | Announcements, your pod | 0–11 | 2 min | Free |

Set a monthly spend limit of <span class="key">USD 40</span> with an email alert at <span class="key">USD 20</span>. [Appendix D](/reference/d-costs/) has the detail.

The setup notebook installs pinned versions of everything, so nothing changes mid-course. You meet each library when you need it:

- **Python 3.12**: every week
- **LangChain**, through `init_chat_model`: Week 1
- **Pydantic v2**: Week 2
- **SQLite**: Week 3
- **LangGraph**: Week 4
- **Gradio**: Week 6
- **YAML config** and **pytest**: Week 7
- **Fake model adapter**: self-checks that run without calling Claude

### GitHub in brief

GitHub keeps your work safe and shows every version of it. Six words cover most of what you need:

- **Repository (repo):** a project folder that remembers every saved version.
- **Template:** a repo you copy to start your own. The course template is `harness-starter`.
- **Private:** only you can see it. Your course repo is <span class="key">private</span>.
- **Commit:** one saved version, with a short note saying what changed.
- **Push and pull:** push sends your commits to GitHub; pull brings changes from GitHub to your copy.
- **Branch:** a separate line of work, so an experiment does not touch your main copy.

**Your own copy of the course template.** The template lives at [github.com/harness-km/harness-starter](https://github.com/harness-km/harness-starter). It is public, so you need no invitation, but you must be <span class="key">signed in</span> to GitHub to see the **Use this template** button. Using the template gives you a fresh repo of your own, with no link back to anyone else's work. [Step 2](#step-2-github-account) has the clicks.

**How your work moves.** Every save follows the same loop.

![The Git daily workflow: check the status, stage your files, commit, pull, push](/images/git/git-daily-workflow.webp)

- **Weeks 1–6:** Colab runs the loop for you. **Save a copy in GitHub** is a commit and a push in one click.
- **From Week 7:** in Codespaces you type the commands yourself. You rehearse them once in [Step 8](#step-8-try-codespaces-once).

The picture mentions teammates. In this course the other side of the loop is you, in another tool: Colab, Codespaces and GitHub stay in step.

**Branches.** You will rarely create one yourself.

![Managing branches: list, create, switch, merge and view history; local branches and their copies on GitHub](/images/git/git-branches.webp)

- `main` is your working copy.
- From Week 7, `make catch-up` first saves your work on a <span class="key">backup branch</span>, then copies in the published checkpoint. Nothing you wrote is lost.
- `origin/main` is GitHub's copy of `main`. `git pull` brings your `main` up to date with it.

**Look things up.** [Git documentation](https://git-scm.com/docs) covers every command. [GitHub Docs](https://docs.github.com) covers the website: repositories, Codespaces and Discussions.

### Keeping your key safe

<!-- figure: week-00/step-03-key (designed after this page is approved) -->

Your API key is a password that <span class="key">spends money</span>. Anyone who has it can run calls on your account.

- Keep it in <span class="key">one place</span>: Colab Secrets now, Codespaces secrets from Week 7.
- Never put it in a cell, a screenshot, WhatsApp, Discussions or any file in your repository.
- Once a key reaches Git history, treat it as public. Deleting the file does not remove it. Revoke the key in the Console and make a new one.

The spend limit is a <span class="key">security control</span>, not only a budget. It caps the cost of a leaked key, or of your own agent stuck in a loop. The alert tells you early.

### What to expect

- **Effort:** plan on <span class="key">2–3 hours of your own work for each hour of live session</span>. That is 4–6 hours a week on top of the 2-hour session, about 6–8 hours in total.
- **Setup:** 1–2 hours, once.
- **Data:** synthetic only. Every supplier, invoice and bank account is generated. Never use real company or personal data, even in your capstone.

## Assignment

Work through the nine steps in order and tick each box as you go. Your ticks are saved in this browser. Allow 1–2 hours. Stuck for more than 10 minutes? Ask in the WhatsApp group. Someone has hit the same thing before.

### Step 1: Google account and Colab

- [ ] Sign in to Google, or create an account at [accounts.google.com](https://accounts.google.com).
- [ ] Open [colab.research.google.com](https://colab.research.google.com). If a window pops up, close it. You do not need a new notebook: the course gives you one in Step 4.

**You should see:** the Colab page, with your Google picture at the top right.

### Step 2: GitHub account

- [ ] Create an account at [github.com](https://github.com).
- [ ] Turn on two-step verification. Click your profile picture (top right) → **Settings** → **Password and authentication** → **Enable two-factor authentication**.
- [ ] Open the course template: [github.com/harness-km/harness-starter](https://github.com/harness-km/harness-starter). It is public, so you need no invitation.
- [ ] Click **Use this template** → **Create a new repository**.
- [ ] Name it `harness-course`, choose **Private**, and click **Create repository**.

**You should see:** your own repository, with a padlock beside its name.

### Step 3: Claude account and spend limit

- [ ] Sign up at [platform.claude.com](https://platform.claude.com).
- [ ] Add a payment method and buy the smallest credit top-up. Card issued outside the US? Check it allows international online payments.
- [ ] Set a spend limit under **Limits**: USD 40 a month, with an email alert at USD 20.

**You should see:** the limit and the alert under Limits. You create the key itself in Step 5.

### Step 4: Open the setup notebook

- [ ] Scroll to the top of this page and click **Open lab in Colab**. The setup notebook opens in Colab.
- [ ] If Colab keeps loading, see "If something goes wrong" at the end of this assignment.

**You should see:** a notebook called `setup.ipynb`. This is the course's copy. In Step 7 you save it into your own repository.

### Step 5: Create your key and add it to Colab

- [ ] In a new browser tab, open [platform.claude.com](https://platform.claude.com) → **API keys** → **Create key**. Name it `harness-course`.
- [ ] Copy the key. It is shown only once, so go straight to the next box.
- [ ] Back in the setup notebook, click the **key icon** on the left.
- [ ] Click **Add new secret**. Name: `ANTHROPIC_API_KEY`. Value: paste your key.
- [ ] Switch **Notebook access** on.

**You should see:** the secret in the list, with Notebook access on.

### Step 6: Run the setup notebook

- [ ] Click **Runtime** → **Run all**.
- [ ] If Colab warns that the notebook is not authored by Google, click **Run anyway**.
- [ ] Allow Google Drive access when asked.

**You should see:** the last line print `Secrets OK · Claude reachable · Drive mounted · Dataset OK`.

### Step 7: Save your work to GitHub

- [ ] Click **File** → **Save a copy in GitHub**.
- [ ] The first time, GitHub asks for permission. Tick **Include private repos** and allow access.
- [ ] Choose `harness-course`, branch `main`, path `week-00/setup.ipynb`. Click **OK**.
- [ ] Remember: Colab does not save to GitHub on its own. Save again after every edit.

**You should see:** a new commit on your repository page, a few seconds old.

### Step 8: Try Codespaces once

- [ ] On your repository page, click **Code** → **Codespaces** → **Create codespace on main**. The first start takes a few minutes.
- [ ] Open a terminal: **Terminal** → **New Terminal**.
- [ ] Type each line and press Enter: `git status`, then `make test`, then `make catch-up WEEK=00`.
- [ ] Save any changes: `git add -A`, then `git commit -m "Week 0 rehearsal"`, then `git push`. If Git says "nothing to commit", that is fine.
- [ ] Delete the Codespace: go to [github.com/codespaces](https://github.com/codespaces), click **⋯** next to it, then **Delete**.

**You should see:** `make test` passing, and no Codespace left in your list.

### Step 9: Meet your group

- [ ] Join the WhatsApp group (link in your welcome email).
- [ ] Say hello to your pod.
- [ ] Post one goal in GitHub Discussions, in the **Introductions** category.

**You should see:** your post in Discussions.

### If you have time: tour the dataset

- [ ] The setup notebook created a small database for a fictional distributor: suppliers, products, purchase orders, deliveries and invoices. Pick one purchase order and follow it to what arrived and what was billed.

:::caution[If something goes wrong]
- **Colab keeps loading and never opens:** open the link in a private window (Ctrl+Shift+N) and sign in to one Google account only. If that works, sign out of your other Google accounts, or allow cookies for google.com, or pause your ad-blocker for Colab.
- **Error saying the notebook has no access to the secret:** click the key icon and switch **Notebook access** on. Each notebook needs its own permission.
- **Your repository is not in the list:** it is private. Tick **Include private repos** and allow access again.
- **Colab reset and the dataset is gone:** run the first cell again. It rebuilds the dataset.
- **Save a copy in GitHub failed:** check you are signed in to the right GitHub account and save again. Your work is still in Google Drive.
:::

### Your first ADR (practice)

An **ADR** (architecture decision record) is a half-page note about one design decision: what you had to decide, the options, what you chose, and what it will cost you. You write one each week. Together they show how your thinking grew, and they are the part of your portfolio employers read. Nobody grades them.

This week's question: **would you rebuild your favourite n8n workflow in code? Why, or why not?** There is no right answer. What matters is the reason.

- [ ] Open the [ADR template](/reference/a-c-templates/) and copy the block under "A. ADR template".
- [ ] On your repository page, click **Add file** → **Create new file**. Name it `week-00/adr-00-practice.md` and paste the template.
- [ ] Fill in the three parts, 2–3 sentences each: **Context** (the workflow and what matters: cost, speed, who maintains it), **Options considered** (keep it in n8n, or rebuild it in code, each with a pro and a con), **Decision and consequences** (your choice, the main reason, and what gets harder).
- [ ] Click **Commit changes**.

<details><summary>A short example</summary>

**ADR 0: Keep the weekly sales email in n8n**

**Context.** An n8n workflow emails the sales team a weekly summary. It breaks about once a quarter when a column name changes. Only I maintain it.

**Options considered.** 1. Keep it in n8n: quick to change, anyone can read it; no tests. 2. Rebuild in Python: tests catch a renamed column; slower to change, and only I can read it.

**Decision and consequences.** Keep it in n8n, because a quarterly fix takes ten minutes. Harder: breakages still reach users first. Revisit if it starts feeding a payment or a customer.

</details>

The threat-model template ([Appendix B](/reference/a-c-templates/)) comes in later weeks.

---
