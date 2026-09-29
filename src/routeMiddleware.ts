import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

// Week pages render some sections from frontmatter; add them to the "On this page" list.
export const onRequest = defineRouteMiddleware((context) => {
  const route = context.locals.starlightRoute;
  const d = route.entry.data as Record<string, any>;
  if (typeof d.week !== 'number' || !route.toc) return;
  const live = d.status === 'live';
  const item = (slug: string, text: string, depth = 2) => ({ depth, slug, text, children: [] });
  const before = [];
  if (d.slides?.length) before.push(item('slides', 'Slides'));
  if (d.outcomes?.length) before.push(item('outcomes', 'Outcomes'));
  const after = [];
  if (live && (d.security || d.adr || d.breakIt || d.resource || d.deeper?.length)) after.push(item('threads', "This week's threads"));
  if (live && d.portfolio?.length) after.push(item('portfolio', 'Keep for your portfolio'));
  const [overview, ...rest] = route.toc.items;
  route.toc.items = [overview, ...before, ...(live ? rest : []), ...after];
});
