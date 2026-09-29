// Single place for course-wide settings. Edit these, not the components.
export const SITE_URL = 'https://harness.krishnamohan.co';

// GitHub owner (user or org) and the public starter template repo.
// TODO: replace with the real GitHub account before launch.
export const GITHUB_OWNER = 'harness-km';
export const STARTER_REPO = 'harness-starter';
export const STARTER_BRANCH = 'main';

export const ACTS = [
  { n: 0, label: 'Start here', weeks: [0] },
  {
    n: 1,
    label: 'Act 1 · Harness 1: Supplier invoices',
    weeks: [1, 2, 3, 4, 5, 6],
    gate: 'The three worked invoices get the expected decisions: INV-A approved, INV-B partial, INV-C blocked as a duplicate.',
  },
  {
    n: 2,
    label: 'Act 2 · The Harness Kernel',
    weeks: [7, 7.5, 8, 9],
    gate: 'Harness 1 runs on Kernel v1 and passes its evaluation suite (at least 14 of 15).',
  },
  { n: 3, label: 'Capstone · Your own domain', weeks: [10, 10.5, 11] },
];

// "7b" for 7.5, "10b" for 10.5
export const weekLabel = (w) => (Number.isInteger(w) ? String(w) : `${Math.floor(w)}b`);

export const actForWeek = (w) => ACTS.find((a) => a.weeks.includes(w));
export const isGateWeek = (w) => {
  const act = actForWeek(w);
  return Boolean(act?.gate) && act.weeks.at(-1) === w;
};

export const labUrl = (lab) => {
  if (!lab) return null;
  const base = `${GITHUB_OWNER}/${STARTER_REPO}`;
  return lab.env === 'colab'
    ? `https://colab.research.google.com/github/${base}/blob/${STARTER_BRANCH}/${lab.path}`
    : `https://codespaces.new/${base}?quickstart=1`;
};
export const solutionUrl = (lab) => {
  if (!lab || lab.env !== 'colab') return null;
  const path = lab.path.replace(/^week-/, 'solutions/week-');
  return `https://colab.research.google.com/github/${GITHUB_OWNER}/${STARTER_REPO}/blob/${STARTER_BRANCH}/${path}`;
};
export const repoFileUrl = (path) =>
  `https://github.com/${GITHUB_OWNER}/${STARTER_REPO}/blob/${STARTER_BRANCH}/${path}`;
