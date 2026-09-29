import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

// Extra frontmatter for week pages. All fields are optional so that
// ordinary pages (Syllabus, Reference) use the same collection.
const weekFields = z.object({
  // Week number; 7.5 and 10.5 are Weeks 7b and 10b (weekLabel carries the display label).
  week: z.number().min(0).max(11).optional(),
  weekLabel: z.string().optional(),
  // outline = summary + outcomes only; live = the full page (reading posted 3 days before the session).
  status: z.enum(['outline', 'live']).default('outline'),
  // true once the week has closed and its reference solution is published.
  solution: z.boolean().default(false),
  summary: z.string().optional(),
  outcomes: z.array(z.string()).default([]),
  n8nBridge: z.string().optional(),
  lab: z
    .object({
      path: z.string(), // path inside harness-starter, e.g. week-02/lab.ipynb
      env: z.enum(['colab', 'codespaces']),
    })
    .optional(),
  stretch: z.string().optional(),
  selfCheck: z.string().optional(),
  mvw: z.string().optional(),
  security: z.object({ category: z.string().optional(), text: z.string() }).optional(),
  adr: z.object({ number: z.number().int(), title: z.string(), detail: z.string().optional() }).optional(),
  breakIt: z.string().optional(),
  deeper: z.array(z.string()).default([]),
  resource: z.object({ measure: z.string(), optimise: z.string() }).optional(),
  portfolio: z.array(z.string()).default([]),
  // Slides for the week: a path under /slides/ (PDF shows inline) or a Google Slides / OneDrive link.
  // One file:  slides: /slides/week-02.pdf
  // Several:   slides: [{ title: Part 1, href: /slides/week-02a.pdf }, { title: Part 2, href: https://... }]
  slides: z
    .union([z.string(), z.array(z.object({ title: z.string().optional(), href: z.string() }))])
    .optional()
    .transform((v) => (v === undefined ? [] : typeof v === 'string' ? [{ href: v }] : v)),
});

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema({ extend: weekFields }) }),
};
