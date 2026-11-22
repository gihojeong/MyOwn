// 렌더 점검용 접촉 인화지(contact sheet): 지정 난이도 문항의 그림을 실제 렌더해 12장씩 묶은 PNG 로 저장 (DA 2026-11-22)
// usage: node tools/sheets.js <outDir> [lv=B] [dist/HBM_quiz.html] [domainCode]
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const out = path.resolve(process.argv[2] || '/tmp/sheets'), LV = process.argv[3] || 'B';
const file = path.resolve(process.argv[4] || 'dist/HBM_quiz.html'), DOM = process.argv[5] || '';
fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1500, height: 1200 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  await p.goto('file://' + file); await p.waitForTimeout(800);
  const ids = await p.evaluate(([LV, DOM]) => BANK.filter(q => q.lv === LV && (!DOM || q.id.startsWith(DOM + '-'))).map(q => q.id), [LV, DOM]);
  const index = [];
  for (let k = 0; k < ids.length; k += 12) {
    const chunk = ids.slice(k, k + 12);
    await p.evaluate((chunk) => {
      document.body.innerHTML = '<div id="grid" style="display:grid;grid-template-columns:repeat(3,480px);gap:8px;padding:8px;background:#fff"></div>';
      const g = document.getElementById('grid');
      chunk.forEach(id => { const q = BANK.find(x => x.id === id); const d = document.createElement('div');
        d.style.cssText = 'border:1px solid #999;font:12px sans-serif';
        const st = (typeof stemOf === 'function' ? stemOf(q) : (q.stem || '')).slice(0, 110);
        d.innerHTML = `<div style="background:#eee;padding:3px"><b>${q.id}</b> ${q.title}<br><span style="color:#555">${st}</span></div><div class="stage-wrap" style="width:480px">${svgFor(q)}</div>`;
        g.appendChild(d); });
      document.querySelectorAll('svg.stage').forEach(sv => { try { figPost(sv); } catch (e) {} });
    }, chunk);
    await p.waitForTimeout(150);
    const n = String(k / 12 + 1).padStart(3, '0'); const f = path.join(out, `sheet_${LV}_${n}.png`);
    await (await p.$('#grid')).screenshot({ path: f }); index.push([f, chunk]);
  }
  fs.writeFileSync(path.join(out, 'index.json'), JSON.stringify(index, null, 1));
  console.log(JSON.stringify({ n: ids.length, sheets: index.length, out })); await b.close();
})();
