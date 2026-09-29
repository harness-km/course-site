# Agent Harness Engineering — course site

Static site for harness.krishnamohan.co, built with Astro Starlight and hosted on Cloudflare.

## Source of truth: the guide

Week pages, the Syllabus and the Reference pages are generated from `guide/guide.md`, a markdown export of the Course 1 Guide (a Claude Doc). To update the site:

1. Export the guide as markdown and save it over `guide/guide.md`.
2. Run `python3 scripts/build_from_guide.py`.
3. Review the diff and open a pull request.

Hand-written pages that the script leaves alone: `index.mdx`, `reference/harness-kernel.mdx`, and the weekly reading notes in `src/reading/week-NN.md` (the script places them at the top of each week's body, under "Reading"). Weeks in `LIVE_BY_DEFAULT` are generated as `live` (currently 0–5 for review; before the cohort, set it to `{0, 1}` and release weekly).

## How content is organised

| What | Where |
| --- | --- |
| Home page | `src/content/docs/index.mdx` |
| Syllabus | `src/content/docs/syllabus.md` (generated) |
| Course 2 (coming later) | `src/content/docs/course-2.md` (generated from Appendix N) |
| Weekly reading notes | `src/reading/week-NN.md` (hand-written; self-quiz at the end) |
| Week pages | `src/content/docs/weeks/week-00.md` … `week-11.md`, plus `week-07b.md` and `week-10b.md` (generated) |
| Reference pages | `src/content/docs/reference/*.md` (Course design pages plus Appendices A–M) |
| Thread indexes (security, ADR, break it, n8n) | Built automatically from week frontmatter: `src/pages/threads/[thread].astro` |
| Acts, gates, GitHub repo for lab links | `src/data/course.mjs` |
| Brand colours and fonts | `src/styles/brand.css` |

## Week pages

Each week is one Markdown file. The frontmatter holds the structured parts (summary, outcomes, n8n bridge, lab, stretch, self-check, minimum viable week, security lens, ADR, break it, going deeper, resource meter, keep for your portfolio); the body holds the Reading, Live session and Assignment. The template in `src/components/overrides/MarkdownContent.astro` lays every week out the same way.

**Releasing a week:** change `status: outline` to `status: live` in the week file three days before the session (the reading is posted then). **Closing a week:** add `solution: true` to show the "Open solution in Colab" button once the solution is published in the starter repository. Outline weeks show only the summary and outcomes, carry a "Soon" badge in the sidebar, and are left out of the thread indexes.

## Adding slides to a week

1. Put the file in `public/slides/`, for example `public/slides/week-02.pdf` (25 MB maximum per file; PDF previews inline, .pptx downloads).
2. In `src/content/docs/weeks/week-02.md`, add one line to the block at the top: `slides: /slides/week-02.pdf`
3. For Google Slides or OneDrive, use the share link instead: `slides: https://docs.google.com/presentation/d/…/edit`
4. Several decks: `slides: [{ title: Part 1, href: /slides/week-02a.pdf }, { title: Part 2, href: /slides/week-02b.pdf }]`

Slides show even on outline weeks, so add them when you want learners to see them. The site is public until Cloudflare Access is switched on, so keep answer keys out of `public/`. Re-running the guide generator keeps slide links and any week you set to `live` by hand.

## Workflow

1. Claude edits files on a branch and opens a pull request.
2. Cloudflare builds a preview link for the pull request.
3. Krishna reviews the preview and merges; the live site updates in about a minute.

## Local commands

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # output in dist/
```
