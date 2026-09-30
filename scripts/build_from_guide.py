"""Generate the course site from guide/guide.md (the Course 1 guide, exported from the Claude Doc).

Run from the repo root:  python3 scripts/build_from_guide.py

- Week pages: src/content/docs/weeks/week-NN.md (and week-07b, week-10b). Structured labels in the guide
  become frontmatter; the rest becomes the page body.
- Hand-written reading for a week lives in src/reading/week-NN.md and is placed at the top of the body.
- `slides`, `status: live` and `solution: true` set by hand in a week file are kept when you regenerate.
- Syllabus, Course 2 and reference pages are regenerated every time (except KEEP below).
"""
import re
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
GUIDE = (ROOT / "guide/guide.md").read_text(encoding="utf-8")
DOCS = ROOT / "src/content/docs"
READING = ROOT / "src/reading"
LIVE_BY_DEFAULT = {0, 1, 2, 3, 4, 5}      # pre-launch review; before the cohort, reset to {0, 1} and release weekly

SIDEBAR = {0: "W0 · Set up your tools", 1: "W1 · Unpacking the black box", 2: "W2 · Reading invoices",
           3: "W3 · Tools and the agent loop", 4: "W4 · LangGraph fundamentals", 5: "W5 · Generate, audit, correct",
           6: "W6 · Harness 1 MVP", 7: "W7 · Notebook to package", 7.5: "W7b · Catch-up, capstone brief",
           8: "W8 · Kernel services", 9: "W9 · Durability and approval", 10: "W10 · Capstone sprint 1",
           10.5: "W10b · Capstone sprint 2", 11: "W11 · Capstone reflection"}


# ---------------------------------------------------------------- markdown helpers
def sections(text, level):
    """{heading: body} at one heading level, ignoring headings inside code fences."""
    out, cur, buf, fence = {}, None, [], False
    mark = "#" * level + " "
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith(mark):
            if cur is not None:
                out[cur] = "\n".join(buf).strip()
            cur, buf = line[len(mark):].strip(), []
        elif cur is not None:
            if not fence and re.match(r"^#{1,%d} " % (level - 1), line):
                out[cur] = "\n".join(buf).strip()
                cur, buf = None, []
                continue
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip()
    return out


def blocks(text):
    out, buf, fence = [], [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and not line.strip():
            if buf:
                out.append("\n".join(buf))
                buf = []
        else:
            buf.append(line)
    if buf:
        out.append("\n".join(buf))
    return out


def is_list(b): return bool(re.match(r"^(- |\d+\. )", b))
def is_table(b): return b.startswith("|")
def items(b): return [re.sub(r"^(- (\[ \] )?|\d+\. )", "", ln).strip() for ln in b.splitlines() if ln.strip()]
def table_rows(b): return [[c.strip() for c in ln.strip("|").split("|")] for ln in b.splitlines()[2:]]
def cap(s): return s if (not s or s.startswith("n8n") or s.startswith("`")) else s[:1].upper() + s[1:]
def one_line(s): return re.sub(r"\s*\n\s*", " ", s).strip()


H2 = sections(GUIDE, 2)
RUNS = sections(H2["How Course 1 runs"], 3)
THREADS = sections(H2["Threads that run through every week"], 3)
APPX = sections(H2["Appendices"], 3)

sec_rows = {r[0]: r for r in table_rows([b for b in blocks(THREADS["Security lens: one threat per week"]) if is_table(b)][0])}
res_rows = {r[0]: r for r in table_rows([b for b in blocks(THREADS["Resource meter: tokens, cost and latency per stage"]) if is_table(b)][0])}

# ---------------------------------------------------------------- week pages
LABEL = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$", re.S)


def week_num(label: str) -> float:
    return float(label[:-1]) + 0.5 if label.endswith("b") else float(label)


def slug_for(label: str) -> str:
    return f"week-{int(label[:-1]):02d}b" if label.endswith("b") else f"week-{int(label):02d}"


def parse_week(label, title, body):
    n = week_num(label)
    fm = {"title": f"Week {label} — {title}", "sidebar": {"label": SIDEBAR.get(n, f"W{label}")},
          "week": int(n) if n.is_integer() else n, "weekLabel": label,
          "status": "live" if n in LIVE_BY_DEFAULT else "outline"}
    body = re.sub(r"\s*\(self-paced\)$", "", body)
    out, bl, i, summary_done = [], blocks(body), 0, False
    reading_links, assignment = [], None
    while i < len(bl):
        b = bl[i]
        m = LABEL.match(b) if b.startswith("**") else None
        nxt = bl[i + 1] if i + 1 < len(bl) else ""
        if not m:
            if not summary_done:
                fm["summary"] = one_line(b)
                summary_done = True
            else:
                out.append(b)
            i += 1
            continue
        lab, rest = m.group(1).rstrip(":").strip(), m.group(2).strip()
        low = lab.lower()
        follows = not rest and (is_list(nxt) or is_table(nxt))
        step = 2 if follows else 1
        if low == "outcomes":
            fm["outcomes"] = items(nxt)
        elif low == "n8n bridge":
            fm["n8nBridge"] = cap(one_line(rest))
        elif low == "reading":
            reading_links = [cap(x.strip().rstrip(".")) for x in rest.split(";") if x.strip()]
        elif low.startswith("live session"):
            extra = lab.split(":", 1)[1].strip() if ":" in lab else ""
            out.append(f"## Live session{': ' + extra if extra else ''}\n\n" + (nxt if follows else rest))
        elif low.startswith("assignment") or low.startswith("tasks"):
            path = re.search(r"`([^`]+\.ipynb)`", lab)
            if path:
                fm["lab"] = {"path": path.group(1), "env": "colab"}
            elif "codespaces" in low or n >= 7:
                fm["lab"] = {"path": "harness/", "env": "codespaces"}
            assignment = len(out)
            out.append("## Assignment\n\n" + (nxt if follows else rest))
        elif low == "stretch":
            fm["stretch"] = cap(one_line(rest))
        elif low.startswith("self-check"):
            gate = re.search(r"\((Act \d gate)\)", lab)
            if rest:
                fm["selfCheck"] = (f"**{gate.group(1)}:** " if gate else "") + cap(one_line(rest))
            else:
                out.append(f"## Self-check{f' ({gate.group(1)})' if gate else ''}\n\n" + nxt)
        elif low == "security lens":
            key = label if label in sec_rows else None
            fm["security"] = {"text": cap(one_line(rest)), **({"category": sec_rows[key][3]} if key else {})}
        elif low.startswith("architect"):
            num = int(re.search(r"ADR (\d+)", lab).group(1))
            q = re.match(r'^"([^"]+)"\s*(.*)$', rest, re.S)
            fm["adr"] = {"number": num, "title": q.group(1) if q else one_line(rest),
                         **({"detail": one_line(q.group(2))} if q and q.group(2).strip() else {})}
        elif low == "break it":
            fm["breakIt"] = cap(one_line(rest))
        elif low == "going deeper":
            fm["deeper"] = items(nxt) if follows else [cap(one_line(rest))]
        elif low == "minimum viable week":
            fm["mvw"] = cap(one_line(rest))
        elif low.startswith("keep for your portfolio") or low.startswith("what learners keep"):
            fm["portfolio"] = [cap(x.strip().rstrip(".")) for x in re.split(r";\s*", one_line(rest)) if x.strip()]
        else:  # any other labelled block stays in the body, in guide order
            out.append(f"## {lab}\n\n{nxt}" if follows else b)
        i += step
    if label in res_rows:
        fm["resource"] = {"measure": res_rows[label][1], "optimise": res_rows[label][2]}
    if n == 0:
        fm["lab"] = {"path": "week-00/setup.ipynb", "env": "colab"}

    # Reading: hand-written notes (if any) + the guide's reading pointers.
    notes_file = READING / f"{slug_for(label)}.md"
    reading = ["## Reading"]
    if notes_file.exists():
        reading.append(notes_file.read_text(encoding="utf-8").strip())
        if reading_links:
            reading.append("### Further reading\n\n" + "\n".join(f"- {x}" for x in reading_links))
    elif reading_links:
        reading.append("\n".join(f"- {x}" for x in reading_links))
    if len(reading) > 1:
        out.insert(0, "\n\n".join(reading))
    if fm.get("stretch") and assignment is not None:
        idx = assignment + (1 if len(reading) > 1 else 0)
        out[idx] += f"\n\n**Stretch:** {fm['stretch']}"
    return fm, "\n\n".join(out)


class Dumper(yaml.SafeDumper):
    pass


Dumper.add_representer(str, lambda d, s: d.represent_scalar("tag:yaml.org,2002:str", s))

week_dir = DOCS / "weeks"
week_dir.mkdir(parents=True, exist_ok=True)
preserved = {}
for f in week_dir.glob("week-*.md"):
    parts = f.read_text(encoding="utf-8").split("---", 2)
    old = yaml.safe_load(parts[1]) if len(parts) > 2 else {}
    preserved[f.stem] = {k: old[k] for k in ("slides", "status", "solution") if k in (old or {})}
    f.unlink()
count = 0
for head, body in H2.items():
    m = re.match(r"Week (\d+b?) — (.+)$", head)
    if not m:
        continue
    label = m.group(1)
    title = re.sub(r"\s*\(self-paced\)$", "", m.group(2))
    fm, md = parse_week(label, title, body)
    keep = preserved.get(slug_for(label), {})
    if keep.get("status") == "live":
        fm["status"] = "live"
    for k in ("slides", "solution"):
        if k in keep:
            fm[k] = keep[k]
    y = yaml.dump(fm, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=100000)
    (week_dir / f"{slug_for(label)}.md").write_text(f"---\n{y}---\n\n{md}\n", encoding="utf-8")
    count += 1
print(f"weeks: {count}")

# ---------------------------------------------------------------- syllabus
ov = H2["Course overview"]
ov = re.sub(r"\*\*(What learners build|By the end, learners can|Course 1 and Course 2\.)\*\*[ \t]*",
            lambda mm: "## " + mm.group(1).rstrip(".") + "\n\n", ov)
ov = re.sub(r"\n{3,}", "\n\n", ov)
ov = ov.replace("Its draft scope is in Appendix N.", "See [Course 2 (coming later)](/course-2/).")
course_map = H2["The course map"]
runs_intro = H2["How Course 1 runs"].split("### ")[0].strip()
runs = "\n\n".join(f"### {k}\n\n{v}" for k, v in RUNS.items())
syl = f"""---
title: Syllabus
description: Course 1 overview, outcomes, the course map and how each week runs.
tableOfContents:
  maxHeadingLevel: 3
---

<!-- Generated from guide/guide.md by scripts/build_from_guide.py. Edit the guide, not this file. -->

{ov}

## The course map

{course_map}

## How Course 1 runs

{runs_intro}

{runs}
"""
(DOCS / "syllabus.md").write_text(syl, encoding="utf-8")

# ---------------------------------------------------------------- Course 2 page
n_body = H2["Appendix N: Course 2 (draft)"]
(DOCS / "course-2.md").write_text(f"""---
title: Course 2 (coming later)
description: What comes after Course 1. Designed from what the founding cohort learns.
sidebar:
  label: Course 2 · coming later
  badge:
    text: Later
    variant: note
---

<!-- Generated from guide/guide.md (Appendix N). -->

Course 2 builds on your Course 1 kernel and capstone: a second, harder harness, multi-agent coordination, and deployment to production on Azure. It is designed from what the founding cohort of Course 1 shows us, so the list below is a draft, not a syllabus.

{n_body}
""", encoding="utf-8")

# ---------------------------------------------------------------- reference pages
ref = DOCS / "reference"
ref.mkdir(exist_ok=True)
KEEP = {"harness-kernel.mdx"}
for f in ref.glob("*"):
    if f.name not in KEEP:
        f.unlink()


def page(slug, title, desc, order, body):
    fm = {"title": title, "description": desc, "sidebar": {"order": order}}
    y = yaml.dump(fm, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=100000)
    body = re.sub(r"\(Appendix ([A-N])\)", lambda mm: f"([Appendix {mm.group(1)}]({APPX_LINKS[mm.group(1)]}))", body)
    (ref / f"{slug}.md").write_text(f"---\n{y}---\n\n{body.strip()}\n", encoding="utf-8")


APPX_LINKS = {
    "A": "/reference/a-c-templates/", "B": "/reference/a-c-templates/", "C": "/reference/a-c-templates/",
    "D": "/reference/d-costs/", "E": "/reference/e-token-playbook/", "F": "/reference/f-model-selection/",
    "G": "/reference/g-failure-classification/", "H": "/reference/h-evaluating-a-harness/",
    "I": "/reference/i-reading-any-harness/", "J": "/reference/j-open-problems/", "K": "/reference/k-credits/",
    "L": "/reference/l-prompt-specs-and-skills/", "M": "/reference/m-troubleshooting-runbook/", "N": "/course-2/",
}

stack = H2["Course stack"].replace("### ", "## ")
intro, _, rest = stack.partition("\n\n|")
page("course-stack", "Course stack", "The tools used in Course 1, why each was chosen, and its enterprise equivalent.", 1,
     intro + "\n\n## What the course uses\n\n|" + rest)
page("security-map", "Security lens map", "One threat per week, mapped to the OWASP Top 10 for LLM Applications.", 3,
     THREADS["Security lens: one threat per week"])
page("resource-thread", "Resource meter", "Tokens, cost and latency per stage, and one optimisation each week.", 4,
     THREADS["Resource meter: tokens, cost and latency per stage"])
page("monitoring", "Monitoring and troubleshooting", "Logs, traces and audit: three records, one run ID.", 5,
     THREADS["Monitoring and troubleshooting in Course 1"])


def appx_h3(letter, key, slug, title, desc):
    page(slug, f"{letter}. {title}", desc, 10 + ord(letter) - ord("A"), APPX[key])


def appx_h2(letter, key, slug, title, desc):
    body = re.sub(r"^\*\*(.+?)\*\*$", r"## \1", H2[key], flags=re.M)
    page(slug, f"{letter}. {title}", desc, 10 + ord(letter) - ord("A"), body)


page("a-c-templates", "A–C. Templates and checklist", "ADR template, threat-model template and the production-readiness checklist.", 10,
     "## A. ADR template\n\n" + APPX["A. ADR template (half a page)"] +
     "\n\n## B. Threat-model template\n\n" + APPX["B. Threat-model template"] +
     "\n\n## C. Production-readiness checklist\n\n" + APPX["C. Production-readiness checklist (Course 1)"])
appx_h3("D", "D. Costs and logistics (estimates, September 2026)", "d-costs", "Costs and logistics", "What Course 1 costs, who pays, and Claude prices.")
appx_h3("E", "E. Token optimisation playbook", "e-token-playbook", "Token optimisation playbook", "Find the most expensive stage, then pull the lever that fits it.")
appx_h3("F", "F. Choosing the right model", "f-model-selection", "Choosing the right model", "The cheapest model that clears each step's accuracy threshold.")
appx_h2("G", "Appendix G: Failure classification", "g-failure-classification", "Failure classification", "Transient, recoverable and terminal failures, and how the harness responds.")
appx_h2("H", "Appendix H: Evaluating a harness", "h-evaluating-a-harness", "Evaluating a harness", "Five questions for any harness: correctness, safety, recoverability, observability, cost.")
appx_h2("I", "Appendix I: Reading any harness", "i-reading-any-harness", "Reading any harness", "A checklist for reading an unfamiliar agent codebase or framework.")
appx_h2("J", "Appendix J: Open problems", "j-open-problems", "Open problems", "What the field has not settled yet.")
appx_h2("K", "Appendix K: Credits", "k-credits", "Credits", "Sources Course 1 draws on.")
appx_h2("L", "Appendix L: Prompt specs and skills", "l-prompt-specs-and-skills", "Prompt specs and skills", "Prompts treated as code, and when a skill beats a longer prompt.")
appx_h2("M", "Appendix M: Troubleshooting runbook (local)", "m-troubleshooting-runbook", "Troubleshooting runbook", "Logs by run ID, trace, audit, replay: the same four steps every time.")
print("syllabus, course-2 and reference pages written")
