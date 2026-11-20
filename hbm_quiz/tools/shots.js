// Screenshot matrix for design review.
// usage: node tools/shots.js <outDir> [dist/HBM_quiz.html]
// viewports × themes × screens (setup / question short / question long / graded+explanation / result) + one shot per figure type.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const out = path.resolve(process.argv[2] || 'docs/agents/da_shots/after');
const file = path.resolve(process.argv[3] || 'dist/HBM_quiz.html');
fs.mkdirSync(out, { recursive: true });
const VPS = { d1440: [1440, 900], d1920: [1920, 1080], tab: [820, 1180], phone: [390, 844] };
(async () => {
  const b = await chromium.launch();
  const errs = [];
  async function page(vp, theme) {
    const ctx = await b.newContext({ viewport: { width: VPS[vp][0], height: VPS[vp][1] }, deviceScaleFactor: 1, colorScheme: theme, reducedMotion: 'reduce', isMobile: vp === 'phone', hasTouch: vp === 'phone' });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(vp + theme + ': ' + e));
    await p.goto('file://' + file); await p.waitForTimeout(700);
    return p;
  }
  // representative questions (chosen inside the page so indices match the build)
  const p0 = await page('d1440', 'light');
  const pick = await p0.evaluate(() => {
    const len = q => stemOf(q).length + q.opts.join('').length * 2 + q.exp.length;
    const by = {}; BANK.forEach((q, i) => { const f = q.fig[0]; (by[f] = by[f] || []).push(i); });
    const perFig = {}; Object.keys(by).forEach(f => { const a = by[f].slice().sort((x, y) => len(BANK[x]) - len(BANK[y])); perFig[f] = a[a.length - 1]; });
    const all = BANK.map((q, i) => i).sort((x, y) => len(BANK[x]) - len(BANK[y]));
    const shortB = all.find(i => BANK[i].lv === 'B' && BANK[i].fig[0] === 'f_tsv');
    const midI = all.filter(i => BANK[i].lv === 'I' && BANK[i].fig[0] === 'f_therm')[0];
    const longA = all.filter(i => BANK[i].lv === 'A').pop();
    return { perFig, shortB, midI, longA };
  });
  await p0.close();
  const setQ = async (p, list, cur, opt) => p.evaluate(([list, cur, opt]) => {
    exam = list; startAt = Date.now(); answers = {}; graded = false;
    if (opt.graded) { list.forEach(i => answers[i] = (BANK[i].a + 1) % 4); answers[list[0]] = BANK[list[0]].a; graded = true; }
    else if (opt.ans != null) answers[cur] = opt.ans;
    location.hash = 'q' + cur; render();
  }, [list, cur, opt]);
  const snap = async (p, name) => { await p.waitForTimeout(650); await p.screenshot({ path: path.join(out, name + '.png') }); };
  for (const vp of Object.keys(VPS)) for (const theme of ['light', 'dark']) {
    const p = await page(vp, theme); const t = vp + '_' + theme;
    await snap(p, t + '_1setup');
    const L = [pick.shortB, pick.midI, pick.longA];
    await setQ(p, L, pick.shortB, {}); await snap(p, t + '_2q_B');
    await setQ(p, L, pick.midI, { ans: 1 }); await snap(p, t + '_3q_I_selected');
    await setQ(p, L, pick.longA, {}); await snap(p, t + '_4q_A_long');
    await setQ(p, L, pick.longA, { graded: true }); await snap(p, t + '_5graded_long');
    if (vp === 'phone' || vp === 'tab') { await p.screenshot({ path: path.join(out, t + '_5graded_long_full.png'), fullPage: true }); }
    await p.evaluate(() => { history.push({ t: Date.now() - 864e5, lv: 'ALL', n: 3, right: 1, pct: 33.3, unans: 0, used: 60000, limit: 270000, timeout: false });
      history.push({ t: Date.now(), lv: 'ALL', n: 3, right: 2, pct: 66.7, unans: 0, used: 90000, limit: 270000, timeout: false }); location.hash = 'result'; render(); });
    await snap(p, t + '_6result');
    if (vp === 'd1440') {
      for (const [f, i] of Object.entries(pick.perFig)) { await setQ(p, [i], i, {}); await snap(p, t + '_fig_' + f); }
      await setQ(p, [pick.longA], pick.longA, {}); await p.evaluate(() => openLB(BANK[exam[0]])); await snap(p, t + '_7lightbox');
    }
    await p.context().close();
  }
  console.log(JSON.stringify({ pick, errs }));
  await b.close();
})();
