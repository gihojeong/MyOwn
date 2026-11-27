// Headless smoke test: load built page, start exam, render N questions, report JS errors.
// usage: node tools/smoke.js [dist/HBM_quiz.html] [nQuestionsToVisit]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = path.resolve(process.argv[2] || 'dist/HBM_quiz.html');
  const n = +(process.argv[3] || 20);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + file); await p.waitForTimeout(1500);
  const info = await p.evaluate(() => ({ n: BANK.length, doms: ALLDOMS.length }));
  // render every figure offscreen via the page's own renderer if exposed
  const figErr = await p.evaluate(() => { const bad = []; if (typeof svgFor !== 'function') return 'figSVG n/a';
    BANK.forEach((q, i) => { try { svgFor(q); } catch (e) { bad.push(i + ':' + e.message); } }); return bad.slice(0, 20); });
  // 빈 좌표계: 좌표계(axes)는 그렸는데 곡선(curve)이 그보다 적은 그림 (DA 2026-11-22)
  const figEmpty = await p.evaluate(() => { const bad = []; BANK.forEach((q) => { window.__figStat = null; try { svgFor(q); } catch (e) {} const st = window.__figStat; if (st && st.ax > st.cv) bad.push(q.id + ' ' + q.fig[0] + ' ax' + st.ax + '/cv' + st.cv); }); return bad; });
  console.log(JSON.stringify({ info, figErr, figEmpty: figEmpty.slice(0, 50), nEmpty: figEmpty.length, errs: errs.slice(0, 20) }));
  await b.close();
})();
