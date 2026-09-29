# CLAUDE.md — course-site (Agent Harness Engineering)

Guidance for Claude (and anyone else) working in this repository. Read this before changing anything.

## What this is

The public website for **Agent Harness Engineering, Course 1**, at `harness.krishnamohan.co`. Built with Astro Starlight, hosted on Cloudflare. Owner and reviewer: Krishna Mohan. Claude writes and edits; Krishna reviews the preview and approves before anything goes live.

It sits in the workspace folder `agent-harness-course/` next to:

- `harness-starter/` (public template): learners' lab notebooks, the `course-tools` helper package, `make catch-up`
- `harness-solutions/` (private): notebook sources, reference solutions, `release.py`
- `design/`: review material and the figure prototype (`make_figure.py`)

## Source of truth

1. **The Course 1 guide** (a Claude Doc, exported to `guide/guide.md`) defines weeks, outcomes, assignments, threads and appendices.
2. `scripts/build_from_guide.py` turns the guide into the week pages, syllabus, Course 2 page and reference pages. Never edit generated pages by hand: edit the guide and re-run the script.
3. Hand-written content the script keeps:
   - `src/reading/week-NN.md`: each week's reading, in sections, with figure markers (see below)
   - figure sources (planned: `src/figures/`), drawn to `docs/figure-style.md`
   - slide decks (planned: `slides/week-NN.md`), designed to `docs/slides-design.md`; `locked: true` at the top protects hand edits
   - `src/content/docs/index.mdx` and `src/content/docs/reference/harness-kernel.mdx`
   - `slides`, `status: live` and `solution: true` set by hand in a week file

## Where things live

| What | Where |
| --- | --- |
| Week pages (generated) | `src/content/docs/weeks/week-NN.md`, plus `week-07b.md`, `week-10b.md` |
| Week page layout | `src/components/overrides/MarkdownContent.astro` |
| Reading notes | `src/reading/week-NN.md` |
| Figure rules | `docs/figure-style.md` |
| Slide rules | `docs/slides-design.md` |
| Acts, gates, GitHub owner, lab links | `src/data/course.mjs` |
| Frontmatter schema | `src/content.config.ts` |
| Brand colours and fonts | `src/styles/brand.css` |
| Thread indexes | `src/pages/threads/[thread].astro` (built from week frontmatter) |

## Naming

- Folders and repositories: lowercase with hyphens (`course-site`, `harness-starter`)
- Files tools look for by exact name: `CLAUDE.md`, `README.md`
- Other documents: lowercase with hyphens (`figure-style.md`, `slides-design.md`)
- Python scripts: lowercase with underscores (`build_from_guide.py`, `make_figure.py`)
- Figures: `week-NN-step-NN-name.svg` (for example `week-00-step-06-evidence.svg`)
- No spaces in any file or folder name

## Commands

Run from the `course-site` folder:

```sh
npm install                            # once, after cloning
python scripts/build_from_guide.py     # regenerate pages from guide/guide.md
npm run dev                            # preview at http://localhost:4321
npm run build                          # output in dist/; must finish with no errors
```

## Writing a week (summary; the full method is in the "course week page" skill)

- Reading is a sequence of short sections. **Each figure sits at the top of, or in the middle of, the passage that explains it**, placed with `{{figure: week-NN/<name>}}` on its own line.
- Each section: a heading, the figure, 2–4 short paragraphs, and three short lists for the figure's cards (what goes wrong, what we add, result).
- 30–45 minutes of reading in total; long detail goes in an optional "Deeper notes" block.
- End with a two-question self-quiz (predict the output; what is wrong), answers hidden in `<details>`.
- Never give away assignment solutions or the bodies of TODO functions.

## Release routine

1. **Three days before a session:** set `status: live` in the week file (the reading, assignment and slides go public). In `harness-solutions`, run `python release.py open NN ../harness-starter` and push the starter.
2. **After the week closes:** `python release.py close NN ../harness-starter`, push, then set `solution: true` in the week file.
3. Before the cohort, `LIVE_BY_DEFAULT` in `scripts/build_from_guide.py` is set to `{0, 1}` so only Weeks 0–1 start live.

## Rules

- **Synthetic data only.** No real supplier, customer, company or personal data anywhere.
- **No answer keys in `public/`** or anywhere learners can see before a week closes. The site is public until Cloudflare Access is switched on.
- **No secrets** in the repository, ever. Keys live in Colab or Codespaces secrets.
- **Audience is mostly outside India:** use US dollars and US examples in readings, figures and slides.
- **Tone:** plain British English, short sentences, no hype, no emojis, no exclamation marks. Avoid "genuinely", "honestly", "straightforward", "delve", "crucial".
- Paraphrase and credit external material (Odysseus tutorials, Vizuara's book, videos); never copy it.
- Every change goes through a pull request and Krishna's review of the Cloudflare preview.

## Open decisions

- **Currency in the dataset and guide.** The lab dataset, tax rules (GST) and guide amounts are in INR. Moving them to USD and US sales tax changes the data generator, the worked invoices (INV-A, INV-B, INV-C), the self-checks and the guide. Not started; decide before Week 2 content is final.
- ~~GitHub username for the course account~~ Decided: `harness-km`.
- Chatbot hosting and access control (live by Week 3).
