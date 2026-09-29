// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import fs from 'node:fs';
import path from 'node:path';
import { ACTS, SITE_URL } from './src/data/course.mjs';

// Build the week sidebar from the files that exist, so a missing week never breaks the build.
const WEEK_DIR = './src/content/docs/weeks';
const weekFiles = fs.existsSync(WEEK_DIR)
  ? fs.readdirSync(WEEK_DIR).filter((f) => /^week-\d{2}b?\.mdx?$/.test(f))
  : [];
const weeks = weekFiles.map((f) => {
  const src = fs.readFileSync(path.join(WEEK_DIR, f), 'utf8');
  const n = Number(f.slice(5, 7)) + (f[7] === 'b' ? 0.5 : 0);
  const outline = !/^status:\s*live\s*$/m.test(src);
  return { n, slug: `weeks/${f.replace(/\.mdx?$/, '')}`, outline };
});
const weekItems = (nums) =>
  weeks
    .filter((w) => nums.includes(w.n))
    .sort((a, b) => a.n - b.n)
    .map((w) => ({
      slug: w.slug,
      ...(w.outline ? { badge: { text: 'Soon', variant: /** @type {const} */ ('default') } } : {}),
    }));

const sidebar = [
  { label: 'Start here', items: [{ slug: 'syllabus' }, ...weekItems([0])] },
  ...ACTS.filter((a) => a.n > 0).map((a) => ({ label: a.label, items: weekItems(a.weeks) })),
  { label: 'After Course 1', items: [{ slug: 'course-2' }] },
  {
    label: 'Course design',
    collapsed: true,
    items: [
      { slug: 'reference/course-stack' },
      { slug: 'reference/harness-kernel' },
      { slug: 'reference/security-map' },
      { slug: 'reference/resource-thread' },
      { slug: 'reference/monitoring' },
    ],
  },
  {
    label: 'Appendices',
    collapsed: true,
    items: [
      'a-c-templates', 'd-costs', 'e-token-playbook', 'f-model-selection', 'g-failure-classification',
      'h-evaluating-a-harness', 'i-reading-any-harness', 'j-open-problems', 'k-credits',
      'l-prompt-specs-and-skills', 'm-troubleshooting-runbook',
    ].map((s) => ({ slug: `reference/${s}` })),
  },
  {
    label: 'Threads, all weeks',
    collapsed: true,
    items: [
      { label: 'Security lens', link: '/threads/security/' },
      { label: 'Architecture decisions (ADRs)', link: '/threads/adr/' },
      { label: 'Break it', link: '/threads/break-it/' },
      { label: 'n8n bridge', link: '/threads/n8n-bridge/' },
    ],
  },
];

export default defineConfig({
  site: SITE_URL,
  integrations: [
    starlight({
      title: 'Agent Harness Engineering',
      description:
        'Course 1: build an AI agent harness and a reusable kernel, then apply it to your own work. No hype, just what works.',
      favicon: '/favicon.svg',
      customCss: ['./src/styles/brand.css'],
      head: [
        { tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.googleapis.com' } },
        { tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' } },
        {
          tag: 'link',
          attrs: {
            rel: 'stylesheet',
            href: 'https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300..700;1,14..32,400&display=swap',
          },
        },
      ],
      components: {
        SiteTitle: './src/components/overrides/SiteTitle.astro',
        MarkdownContent: './src/components/overrides/MarkdownContent.astro',
      },
      sidebar,
      routeMiddleware: './src/routeMiddleware.ts',
      lastUpdated: false,
      pagination: true,
    }),
  ],
});
