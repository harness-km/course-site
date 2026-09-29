# Slides design — Agent Harness Engineering

_Status: draft for Krishna's review (29 Sep 2026)._

Each week has a slide deck on the course site, viewable in the browser and downloadable as a PDF. The deck is generated from the week's content, so the slides and the web page never disagree. Krishna can then edit the deck by hand.

## 1. How content becomes slides

1. **The week's reading is written in short sections**, each with a heading, a figure, three short lists (what goes wrong, what we add, result) and the explanation.
2. **The build writes a first draft of the deck** as a Markdown file, `slides/week-NN.md`:
   - each reading section becomes one **figure slide** (the full poster from `figure-style.md`), with the explanation as speaker notes;
   - fixed slides are added from the week page (section 3 below).
3. **Krishna reviews and edits** `slides/week-NN.md` if he wants: reorder, delete, reword, add a slide. Putting `locked: true` at the top of the file stops the build from overwriting it.
4. **Marp** (a free, open-source tool) turns the Markdown into a web deck and a PDF. A GitHub Action runs it whenever the site changes and saves the results as `/slides/week-NN/` (web) and `/slides/week-NN.pdf`.
5. The week page shows two buttons: **View slides** and **Download PDF**.

## 2. Format

| Item | Rule |
| --- | --- |
| Size | 16:9, 1600 × 900 (PDF pages are the same) |
| Background | White. No dark slides (printer friendly, same as the figures) |
| Type | Inter for everything (titles semibold, body regular), the same as the site and the figures; a monospace for code |
| Title size | 48–56 px; body 26–30 px; nothing under 18 px |
| Colours | Navy `#0d1b2a` text, amber `#c98a1f` accents (rules, step labels), pastel role colours from `figure-style.md` |
| Footer | Every slide except the title: `Week N · <week title>` on the left, slide number on the right, 16 px grey |
| Words | Maximum about 30 words of body text per slide. Anything longer goes in the speaker notes. |

## 3. Slide layouts

| Layout | When | Content |
| --- | --- | --- |
| **Title** | First slide | Course name, "Week N", week title, the one-sentence summary, instructor name |
| **Agenda** | Second slide | The live-session plan (pulse poll, sticking points, concept, break, security lens, architect's corner, briefing) with times |
| **Figure poster** | One per reading section | The full figure poster: header, diagram, three cards, takeaway, key |
| **Idea** | A point with no figure | A title and up to three short lines |
| **Code** | A short snippet | A title, at most 12 lines of code, one line of explanation |
| **n8n bridge** | Once a week | "In n8n you… / In code you…" side by side |
| **Security lens** | Once a week | The threat, where it enters, what stops it |
| **Architect's corner** | Once a week | The ADR question and the options, for pod discussion |
| **Break it** | Once a week | The challenge, with no answer |
| **Assignment briefing** | Near the end | Core steps, the minimum viable week, stretch options |
| **Self-quiz** | Last content slide | The two questions. Answers go on the following slide, so the PDF works for self-study |
| **Close** | Last slide | Next week's title and when the reading is posted |

A typical week: 10–16 slides.

## 4. What never goes on slides

- Assignment solutions or the bodies of TODO functions
- API keys, even fake ones, except in the Week 1 Break-it where the fake key is the point
- Real company or personal data

## 5. The PDF for learners

- One page per slide, no animations, so it prints cleanly
- Speaker notes are left out of the learner PDF. A separate instructor PDF with notes can be produced on request.
- The PDF is published only when the week goes live (three days before the session), like the rest of the week page

## 6. Checklist before a deck is published

- [ ] Every figure slide matches the figure on the web page
- [ ] No slide over about 30 words of body text
- [ ] Nothing under 18 px; nothing overlaps; code fits without scrolling
- [ ] Amounts in USD; names match the course
- [ ] No solutions, keys or real data
- [ ] PDF opens, prints in grayscale legibly, and the page count matches the web deck