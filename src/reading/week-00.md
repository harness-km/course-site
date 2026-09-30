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
