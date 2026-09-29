# Figure style — Agent Harness Engineering

_Status: draft for Krishna's review (29 Sep 2026). Reference figure: `week-00-step-06-evidence.svg`._

Every diagram in the course uses one visual system, so a learner who has read one figure can read them all. The figures are code-drawn SVG, not generated images: every label is exact, every figure looks the same, and a fix is a one-line edit.

## 1. Principles

1. **One idea per figure.** A figure shows the architecture at one step of the story, with the new part clearly marked.
2. **Colour means role.** A colour always means the same kind of part, in every week (section 3). The key at the bottom of every figure says so.
3. **Printer friendly.** A white background, pastel fills, no large dark areas. Every figure must read clearly when printed in grayscale: roles differ in outline and icon as well as colour.
4. **Text is exact and readable.** No label smaller than 14 px at 1600 px width. No label crosses a line or a box edge.
5. **Same look on the web, in slides and on paper.** The site shows each figure on its own white panel in both light and dark themes.

## 2. Canvas and frame

| Element | Rule |
| --- | --- |
| Canvas | 1600 × 900 (16:9) for the full "poster"; the web figure uses the diagram area only, at the same scale |
| Margins | 40 px on all sides |
| Header | Step title in bold 40 px navy, a thin vertical divider, a one-line subtitle in 24 px, and on the right the week and step in 15 px amber capitals (for example `WEEK 0 · STEP 6 OF 7`) with `Agent Harness Engineering · course.krishnamohan.co` in 13 px grey beneath it. A 4 px amber rule underneath. No dark header bar (saves ink). |
| Diagram area | Below the header, about 440 px high |
| Three cards | Under the diagram, equal width: **What goes wrong** (rose), **What we add** (green), **Result** (blue). Each card: a round outlined icon, a heading in 16 px capitals in the card's accent colour, and up to three bullets in 17 px, each under 45 characters. |
| Takeaway | One sentence in a light navy-tint band, italic 20 px, centred |
| Key (legend) | One line across the bottom, 15 px. First a small swatch and label for each role (section 3), then a thin divider, then a short sample and label for each line style (section 6): Flow of work, Call and reply, Reads data, Writes evidence. |

On the **web page**, only the diagram area and the key are drawn as the image. The header, cards and takeaway are real text on the page (searchable, readable on a phone, read aloud by screen readers). In **slides and print**, the full poster is used.

## 3. Colour by role

| Role | Used for | Fill | Outline |
| --- | --- | --- | --- |
| Input | What arrives: an invoice PDF, a user message | `#EEF1F5` | `#9AA8BA` |
| Model | Claude, or any model call | `#FDEBD3` (orange) | `#E3A456` |
| Harness step | A step the harness runs: prompt, lookups, tools, the loop | `#EEE8FA` (lilac) | `#A38FD9` |
| Check | Anything that verifies: schema validation, the auditor, tests | `#E4F4E7` (green) | `#76BD86` |
| Rule in code | A deterministic decision or permission: match rules, policy check, limits | `#FBE4E7` (rose) | `#E0939F` |
| Data | Tables and stores: purchase orders, receipts, suppliers, checkpoints | `#E3EEFA` (blue) | `#7FAEDD` |
| Decision | The outcome: payment decision, reply to the user | `#FDF3C9` (yellow) | `#DDBB4C` |
| Person | A human in the loop: approver, reviewer | `#DDF2EF` (teal) | `#62B8AD` |
| Evidence | Logs, traces, audit, cost records | `#EEF6F6` | `#6FA9AF`, dashed |

Text and icons: navy `#0d1b2a` for names, `#1f2d3d` for body, `#5a6878` for descriptions. Connectors: slate `#5b6b80`. Brand amber `#c98a1f` is used sparingly: the header rule, the step label, and connectors that write evidence.

**Marking what is new in a step:** the new parts get a 4 px outline instead of 2.5 px, and a small amber "NEW" tag at their top-right corner. Parts that fail in this step get a rose "✕" badge at their top-right corner. Never rely on colour alone.

## 4. Boxes

- **Component box:** rounded corners (12 px radius), 2.5 px outline, an icon on the left (34 px, line style), a bold name (20 px) and a one-line description (16 px). Usual size 200–290 × 80–90 px.
- **Data store:** a cylinder with a line icon and a one- or two-line name (17 px bold).
- **Person:** a component box in the Person colour with the person icon.
- **Evidence:** a full-width dashed band with an icon, "Evidence:" in bold and the record types separated by " · ".
- **Group (kernel, framework):** a dashed amber outline around the parts it contains, with a label chip on its top edge.
- **Condition chip:** a small grey rounded label on a connector, for example `HOLD or over $5,000`.

## 5. Icons

Line icons, 1.8 px stroke on a 24 px grid, drawn in navy, embedded in the SVG (no external files or fonts). One icon per concept, always the same:

| Concept | Icon | Concept | Icon |
| --- | --- | --- | --- |
| Document or PDF | page with folded corner | Model | sparkle |
| Prompt | clipboard | Schema or validation | checklist |
| Tools or lookups | database | Rules in code | gear |
| Auditor | shield with tick | Policy or permission | padlock |
| Decision about money | dollar in a circle | Person | head and shoulders |
| Purchase orders | cart | Receipts | receipt |
| Suppliers | two people | Logs and audit | page with tick |
| What goes wrong | warning triangle | What we add | light bulb |
| Result | target | | |

## 6. Connectors and layout

- Main flow runs **left to right** in one row. Supporting parts sit above (model, checks, policy) or below (data, people).
- Line styles, each shown in the key:

| Line | Meaning |
| --- | --- |
| Solid slate arrow | **Flow of work**: the next step in the run |
| Solid slate, double-headed | **Call and reply**: a step asks a model or checker and gets an answer back |
| Dashed slate arrow | **Reads data**: a lookup that changes nothing |
| Dashed amber arrow | **Writes evidence**: a record written to the log, trace or audit |
- 3 px lines, small solid arrowheads. Arrows start and end 4 px outside boxes.
- Arrows never cross a label and never pass through a box. Reroute rather than overlap.
- At least 40 px between boxes in a row.

## 7. Words

- Names are the ones used in the course (Prompt, Schema check, Lookups, Match rules, Policy check, Payment decision). The same part keeps the same name in every figure.
- Short: names of 1–3 words, descriptions of 2–4 words, bullets under 45 characters.
- **Currency and places:** US dollars and US examples throughout (audience is mostly outside India). Figures, readings and slides use USD. (The dataset, the tax rules and the guide still use INR and GST. Changing them is a separate decision, listed in `CLAUDE.md`.)
- Plain English, British spelling, no hype, no exclamation marks.

## 8. Placement on the page

A figure appears **at the top of, or in the middle of, the passage that explains it**, never after it. The reader sees the picture, then reads why. In the reading source, a figure is placed with one line on its own:

```
{{figure: week-00/step-06-evidence}}
```

## 9. Checklist before a figure is used

- [ ] One idea; the new part is marked with the thick outline and "NEW" tag
- [ ] Every colour matches its role; the key is present
- [ ] Reads in grayscale (print preview)
- [ ] No text under 14 px; nothing overlaps; nothing clipped
- [ ] Names match the course; amounts in USD
- [ ] Web version: diagram and key only; cards and takeaway as page text
