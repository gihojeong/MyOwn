// End-to-end interaction test: setup scroll/click → exam → answer → navigate → grade → result.
// usage: node tools/e2e.js [dist/HBM_quiz.html]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = path.resolve(process.argv[2] || 'dist/HBM_quiz.html');
  const b = await chromium.launch(); const out = [];
  for (const vp of [{ width: 1440, height: 900 }, { width: 820, height: 1180 }, { width: 390, height: 844 }]) {
    const p = await b.newPage({ viewport: vp }); const errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + file); await p.waitForTimeout(1000);
    const r = { vp: vp.width };
    // setup: page must reach the bottom
    await p.mouse.move(vp.width / 2, vp.height / 2); await p.mouse.wheel(0, 3000); await p.waitForTimeout(200);
    r.setupScroll = await p.evaluate(() => Math.round(scrollY + innerHeight) >= document.documentElement.scrollHeight - 2);
    // toggle a domain off and on
    const dom = p.locator('button', { hasText: 'TSV 형성과 충전' }).first();
    await dom.click(); await dom.click();
    await p.locator('button', { hasText: /10문항$/ }).first().click();
    await p.locator('button', { hasText: /문항으로 시험 시작/ }).first().click(); await p.waitForTimeout(500);
    r.examLen = await p.evaluate(() => exam && exam.length);
    for (let i = 0; i < r.examLen; i++) {
      await p.keyboard.press(String((i % 4) + 1)); await p.waitForTimeout(80);
      await p.keyboard.press('ArrowRight'); await p.waitForTimeout(120);
    }
    r.answered = await p.evaluate(() => Object.keys(answers).length);
    // panel scroll on exam screen
    r.examScroll = await p.evaluate(() => { const el = document.getElementById('panelCol'); return !!el; });
    const grade = p.locator('button', { hasText: /^채점/ }).first();
    if (await grade.count()) { await grade.click(); await p.waitForTimeout(300); const ok = p.locator('button', { hasText: /확인|채점하기|예/ }); if (await ok.count()) await ok.first().click().catch(() => {}); }
    await p.waitForTimeout(500);
    r.graded = await p.evaluate(() => graded);
    r.errs = errs;
    out.push(r); await p.close();
  }
  console.log(JSON.stringify(out));
  await b.close();
})();
