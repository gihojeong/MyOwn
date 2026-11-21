// Layout / overlap checker for every question (DA).
// usage: node tools/layout_check.js [--help] [--html FILE] [--out PREFIX | --publish] [--baseline] [--no-screen] [--limit N]
//   (a) figure: renders svgFor(q) for all questions at 1:1 user-unit scale inside one page and measures
//       E1 text overflow  : foreignObject text exceeds its own box (scrollHeight/scrollWidth) by > 3 px
//       E2 text–text      : rendered text ink rects of two labels intersect (> 3 px both ways)
//       E3 clipped        : text ink outside the final viewBox (fitStage = getBBox + 8 px) or outside the 860×592 sheet
//       E4 pill–pill      : two label backgrounds (rounded rects that carry text) intersect (> 3 px)
//       E5 line×text      : a line segment (leader / axis / curve) passes through another label's text ink
//       E6 table overflow : HTML table taller/wider than its foreignObject
//   (b) screen: renders the real question screen (graded, with explanation) at 1440×900, 820×1180, 390×844 and checks
//       S1 horizontal page scroll, S2 panels overlapping, S3 figure squeezed (< 200 px tall on desktop),
//       S4 metric / option text clipped, S5 title clipped.
// Writes $TMPDIR/hbm_layout_check/_layout_latest.{md,json} by default; docs/reviews/ only with --publish. Always compares with docs/reviews/_layout_baseline.json.
// Exit code 1 when the number of questions with high-severity figure defects (E1–E4, E6) or screen defects grows vs baseline.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const argv = process.argv.slice(2), opt = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const HTML = path.resolve(ROOT, opt('--html', 'dist/HBM_quiz.html'));
const BASE = argv.includes('--baseline');
const PUBLISH = argv.includes('--publish');
if (argv.includes('--help') || argv.includes('-h')) {
  console.log(`usage: node tools/layout_check.js [options]
  --html <file>     검사할 빌드 파일 (기본 dist/HBM_quiz.html)
  --out <prefix>    결과 파일 접두 경로 (<prefix>.md / <prefix>.json). 기본: $TMPDIR/hbm_layout_check/_layout_latest
  --publish         공용 docs/reviews/_layout_latest.{md,json} 갱신 (--baseline 과 함께면 _layout_baseline)
  --baseline        기준선으로 기록 (비교 안 함). 공용 기준선은 --publish 를 함께 줄 때만 바뀐다
  --limit <N>       앞 N 문항만 검사
  --no-screen       문항 화면(뷰포트별) 검사 생략
  -h, --help        이 도움말
비교 기준은 항상 docs/reviews/_layout_baseline.json. 고위험 결함 문항·화면 결함 문항이 기준선보다 늘면 exit 1.`);
  process.exit(0);
}
const LIMIT = +opt('--limit', 0);
const NAME = BASE ? '_layout_baseline' : '_layout_latest';
// 공용 파일은 --publish 로만 갱신. 기본은 임시 디렉터리 (다른 에이전트의 결과를 덮어쓰지 않도록)
const OUT = opt('--out', null) ? path.resolve(opt('--out')) : PUBLISH ? path.join(ROOT, 'docs/reviews', NAME) : path.join(process.env.TMPDIR || require('os').tmpdir(), 'hbm_layout_check', NAME);

function figProbe(limit) {
  const TOL = 3;
  const host = document.createElement('div');
  host.style.cssText = 'position:absolute;left:0;top:0;width:860px;height:592px;';
  document.body.appendChild(host);
  const inter = (a, b) => Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) > TOL && Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t)) > TOL;
  const segHits = (x1, y1, x2, y2, r) => { // Liang–Barsky on rect shrunk by 2
    const R = { l: r.l + 2, r: r.r - 2, t: r.t + 2, b: r.b - 2 }; if (R.r <= R.l || R.b <= R.t) return false;
    let t0 = 0, t1 = 1; const dx = x2 - x1, dy = y2 - y1;
    for (const [p, q] of [[-dx, x1 - R.l], [dx, R.r - x1], [-dy, y1 - R.t], [dy, R.b - y1]]) {
      if (p === 0) { if (q < 0) return false; } else { const t = q / p; if (p < 0) { if (t > t1) return false; if (t > t0) t0 = t; } else { if (t < t0) return false; if (t < t1) t1 = t; } }
    }
    return (t1 - t0) * Math.hypot(dx, dy) > 3;
  };
  const N = limit ? Math.min(limit, BANK.length) : BANK.length;
  const res = [];
  for (let qi = 0; qi < N; qi++) {
    const q = BANK[qi];
    host.innerHTML = svgFor(q);
    const sv = host.querySelector('svg');
    if (window.figPost) try { window.figPost(sv); } catch (e) {}
    sv.setAttribute('viewBox', '50 230 860 592'); sv.style.cssText = 'width:860px;height:592px;min-width:0;display:block';
    const H = sv.getBoundingClientRect(), ox = 50 - H.left, oy = 230 - H.top;
    const toU = (r) => ({ l: r.left + ox, r: r.right + ox, t: r.top + oy, b: r.bottom + oy });
    let bb = null; try { const g = sv.getBBox(); bb = { l: g.x - 8, t: g.y - 8, r: g.x + g.width + 8, b: g.y + g.height + 8 }; } catch (e) {}
    const kids = [...sv.querySelectorAll('foreignObject, line')];
    const labels = [], lines = [], issues = [];
    kids.forEach((el, k) => {
      if (el.tagName === 'foreignObject') {
        const div = el.firstElementChild; if (!div) return;
        const box = { l: +el.getAttribute('x'), t: +el.getAttribute('y') }; box.r = box.l + +el.getAttribute('width'); box.b = box.t + +el.getAttribute('height');
        const tbl = div.querySelector('table');
        if (tbl) {
          const tr = toU(tbl.getBoundingClientRect());
          if (tr.b - box.b > TOL || tr.r - box.r > TOL) issues.push(['E6', 'table ' + Math.round(tr.b - box.b) + 'px taller than box']);
          labels.push({ k, ink: tr, bg: tr, text: '[table]', table: 1 });
          return;
        }
        const txt = div.textContent.trim(); if (!txt) return;
        const rg = document.createRange(); rg.selectNodeContents(div);
        const ink = toU(rg.getBoundingClientRect());
        // own background = preceding rect that contains the fo box
        let bg = null; const pv = el.previousElementSibling;
        if (pv && pv.tagName === 'rect') { const x = +pv.getAttribute('x'), y = +pv.getAttribute('y'), w = +pv.getAttribute('width'), h = +pv.getAttribute('height');
          if (x <= box.l + 3 && x + w >= box.r - 3 && y <= box.t + 1 && y + h >= box.b - 1) bg = { l: x, t: y, r: x + w, b: y + h, pill: +pv.getAttribute('rx') > 0 }; }
        const ovH = div.scrollHeight - div.clientHeight, ovW = div.scrollWidth - div.clientWidth;
        const lim = bg || box;
        const out = Math.max(ink.t < lim.t - TOL ? lim.t - ink.t : 0, ink.b > lim.b + TOL ? ink.b - lim.b : 0, ink.l < lim.l - TOL ? lim.l - ink.l : 0, ink.r > lim.r + TOL ? ink.r - lim.r : 0);
        if ((bg && out > 0) || ovH > TOL || ovW > TOL) issues.push(['E1', `"${txt.slice(0, 28)}" overflow ${Math.round(Math.max(out, ovH, ovW))}px`]);
        if (bb && (ink.l < bb.l || ink.t < bb.t || ink.r > bb.r || ink.b > bb.b)) issues.push(['E3', `"${txt.slice(0, 28)}" clipped by viewBox`]);
        else if (ink.l < 50 - 2 || ink.t < 230 - 2 || ink.r > 910 + 2 || ink.b > 822 + 2) issues.push(['E3', `"${txt.slice(0, 28)}" outside sheet`]);
        labels.push({ k, ink, bg: bg && bg.pill ? bg : null, text: txt });
      } else if (el.tagName === 'line') {
        lines.push({ k, x1: +el.getAttribute('x1'), y1: +el.getAttribute('y1'), x2: +el.getAttribute('x2'), y2: +el.getAttribute('y2') });
      }
    });
    for (let i = 0; i < labels.length; i++) for (let j = i + 1; j < labels.length; j++) {
      const a = labels[i], b = labels[j];
      if (inter(a.ink, b.ink)) issues.push(['E2', `"${a.text.slice(0, 20)}" × "${b.text.slice(0, 20)}"`]);
      else if (a.bg && b.bg && inter(a.bg, b.bg)) issues.push(['E4', `"${a.text.slice(0, 20)}" × "${b.text.slice(0, 20)}"`]);
    }
    lines.forEach((ln) => labels.forEach((lb) => { if (lb.table || !segHits(ln.x1, ln.y1, ln.x2, ln.y2, lb.ink)) return;
      // pill 위를 지나는 선은 pill 배경에 가려진다(E7, 참고) — 맨 글자 위를 지나는 선만 E5
      if (lb.bg && ln.k < lb.k) issues.push(['E7', `pill covers line: "${lb.text.slice(0, 24)}"`]); else issues.push(['E5', `line × "${lb.text.slice(0, 24)}"`]); }));
    if (issues.length) res.push({ i: qi, id: q.id, fig: q.fig[0], lv: q.lv, issues });
  }
  host.remove();
  return { n: N, res };
}

function screenProbe(limit) {
  const N = limit ? Math.min(limit, BANK.length) : BANK.length;
  const out = [];
  const R = (el) => el && el.getBoundingClientRect();
  const ov = (a, b) => a && b && a.width && b.width && Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2;
  const desk = innerWidth > 1180;
  for (let qi = 0; qi < N; qi++) {
    const q = BANK[qi];
    exam = [qi]; answers = { [qi]: (q.a + 1) % 4 }; graded = true; startAt = Date.now();
    window.history.replaceState(null, '', '#q' + qi); render(); stopTimer();
    const iss = [];
    const sw = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth);
    const vw = Math.min(innerWidth, screen.width); if (sw > vw + 1) iss.push(['S1', 'page h-scroll ' + (sw - vw) + 'px']);
    const side = R(document.getElementById('side')), main = R(document.getElementById('main')), pan = R(document.getElementById('panelCol'));
    if (ov(main, pan) || ov(side, main) || ov(side, pan)) iss.push(['S2', 'panels overlap']);
    const fr = document.getElementById('figRow');
    if (desk && fr && fr.getBoundingClientRect().height < 200) iss.push(['S3', 'figure ' + Math.round(fr.getBoundingClientRect().height) + 'px']);
    document.querySelectorAll('.metric .l, .metric .v, .opt > span:last-child').forEach((e) => { if (e.scrollWidth > e.clientWidth + 2) iss.push(['S4', 'clipped: ' + e.textContent.slice(0, 24)]); });
    const h1 = document.querySelector('#main h1'); if (h1 && (h1.scrollWidth > h1.clientWidth + 2)) iss.push(['S5', 'title clipped']);
    const m = document.getElementById('main'); if (desk && m && m.scrollHeight > m.clientHeight + 4 && getComputedStyle(m).overflowY === 'hidden') iss.push(['S3', 'main column content cut ' + (m.scrollHeight - m.clientHeight) + 'px']);
    if (iss.length) out.push({ i: qi, id: q.id, fig: q.fig[0], issues: iss });
  }
  return { n: N, res: out };
}

(async () => {
  const t0 = Date.now();
  const b = await chromium.launch();
  const errs = [];
  const mk = async (w, h) => {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1, isMobile: w < 500, hasTouch: w < 500, reducedMotion: 'reduce' });
    p.on('pageerror', (e) => errs.push(String(e)));
    await p.goto('file://' + HTML);
    await p.evaluate(async () => { try { await Promise.all(['400 16px "Noto Sans KR"', '700 16px "Noto Sans KR"', '800 16px "Noto Sans KR"'].map((f) => document.fonts.load(f, '가A'))); await document.fonts.ready; } catch (e) {} });
    return p;
  };
  const p = await mk(1440, 900);
  const fig = await p.evaluate(figProbe, LIMIT);
  await p.close();
  const screens = {};
  if (!argv.includes('--no-screen')) for (const [w, h] of [[1440, 900], [820, 1180], [390, 844]]) {
    const ps = await mk(w, h); screens[w + 'x' + h] = await ps.evaluate(screenProbe, LIMIT); await ps.close();
  }
  await b.close();

  // ── aggregate ──
  const HIGH = ['E1', 'E2', 'E3', 'E4', 'E6'];
  const byFig = {}, total = {}, figN = {};
  fig.res.forEach((r) => {
    const f = (byFig[r.fig] = byFig[r.fig] || { q: 0, high: 0, E1: 0, E2: 0, E3: 0, E4: 0, E5: 0, E6: 0, E7: 0 });
    f.q++; if (r.issues.some((x) => HIGH.includes(x[0]))) f.high++;
    r.issues.forEach((x) => { f[x[0]]++; total[x[0]] = (total[x[0]] || 0) + 1; });
  });
  const highQ = fig.res.filter((r) => r.issues.some((x) => HIGH.includes(x[0]))).length;
  const anyQ = fig.res.filter((r) => r.issues.some((x) => x[0] !== 'E7')).length;
  const scr = {}; Object.entries(screens).forEach(([k, v]) => { const c = {}; v.res.forEach((r) => r.issues.forEach((x) => c[x[0]] = (c[x[0]] || 0) + 1)); scr[k] = { q: v.res.length, codes: c }; });
  const summary = { when: new Date().toISOString(), n: fig.n, figHighQ: highQ, figAnyQ: anyQ, codes: total, byFig, screens: scr, jsErrors: errs.slice(0, 20), secs: Math.round((Date.now() - t0) / 1000) };
  // per-fig totals (questions per fig) for rates
  const json = { summary, fig: fig.res, screens: Object.fromEntries(Object.entries(screens).map(([k, v]) => [k, v.res])) };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT + '.json', JSON.stringify(json));
  let base = null; try { if (!BASE) base = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs/reviews/_layout_baseline.json'), 'utf8')).summary; } catch (e) {}
  const L = [];
  L.push(`# 레이아웃 검사 ${BASE ? '기준선 (baseline)' : '최신'} — ${summary.when.slice(0, 16)}`, '');
  L.push(`검사기: \`tools/layout_check.js\` · 문항 ${fig.n} · ${summary.secs}s · JS 오류 ${errs.length}`, '');
  L.push('## 상황도 (figure) 결함', '', '| 코드 | 의미 | 건수' + (base ? ' | baseline' : '') + ' |', '|---|---|---:' + (base ? '|---:' : '') + '|');
  const DESC = { E1: '글자가 자기 상자/pill 밖으로 넘침', E2: '라벨 글자끼리 겹침', E3: 'viewBox 밖으로 잘림', E4: 'pill 배경끼리 겹침', E5: '선이 맨 글자(배경 없는 라벨)를 관통', E6: '표가 상자보다 큼', E7: '(참고) pill 이 선 위에 얹혀 선을 가림 — 치수·표식 pill 은 의도된 배치' };
  Object.keys(DESC).forEach((k) => L.push(`| ${k} | ${DESC[k]} | ${total[k] || 0}${base ? ' | ' + ((base.codes || {})[k] || 0) : ''} |`));
  L.push('', `**고위험(E1–E4, E6) 결함 문항: ${highQ} / ${fig.n}**${base ? ` (baseline ${base.figHighQ})` : ''} · 결함 하나라도 있는 문항(E5 포함): ${anyQ}${base ? ` (baseline ${base.figAnyQ})` : ''}`, '');
  L.push('### 그림 종류별', '', '| fig | 문항(결함) | 고위험 문항 | E1 | E2 | E3 | E4 | E5 | E6 | E7 |' + (base ? ' baseline 고위험 |' : ''), '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|' + (base ? '---:|' : ''));
  Object.keys(byFig).sort().forEach((f) => { const v = byFig[f]; L.push(`| ${f} | ${v.q} | ${v.high} | ${v.E1} | ${v.E2} | ${v.E3} | ${v.E4} | ${v.E5} | ${v.E6} | ${v.E7} |` + (base ? ` ${((base.byFig || {})[f] || {}).high || 0} |` : '')); });
  L.push('', '## 문항 화면 (screen) 결함 — 채점 후(해설 표시) 상태', '', '| 뷰포트 | 결함 문항 | 코드별 |' + (base ? ' baseline |' : ''), '|---|---:|---|' + (base ? '---|' : ''));
  Object.entries(scr).forEach(([k, v]) => L.push(`| ${k} | ${v.q} | ${JSON.stringify(v.codes)} |` + (base ? ` ${base.screens && base.screens[k] ? base.screens[k].q + ' ' + JSON.stringify(base.screens[k].codes) : '-'} |` : '')));
  L.push('', 'S1 가로 스크롤 · S2 패널 겹침 · S3 그림 영역 찌그러짐/본문 잘림 · S4 지표·보기 글자 잘림 · S5 제목 잘림', '');
  L.push('## 고위험 결함 예시 (그림 종류별 최대 5문항)', '');
  const ex = {}; fig.res.forEach((r) => { const h = r.issues.filter((x) => HIGH.includes(x[0])); if (!h.length) return; (ex[r.fig] = ex[r.fig] || []).length < 5 && ex[r.fig].push(`- ${r.id} (#${r.i}): ` + h.slice(0, 3).map((x) => x[0] + ' ' + x[1]).join(' · ')); });
  Object.keys(ex).sort().forEach((f) => { L.push(`**${f}**`, ...ex[f], ''); });
  L.push('전체 목록은 같은 이름의 `.json` 참조 (`fig[]`: 문항별 결함, `screens{}`: 뷰포트별).');
  fs.writeFileSync(OUT + '.md', L.join('\n') + '\n');
  console.log(JSON.stringify({ n: fig.n, figHighQ: highQ, figAnyQ: anyQ, codes: total, screens: scr, errs: errs.length, secs: summary.secs, out: OUT }));
  let fail = errs.length > 0;
  if (base) {
    if (highQ > base.figHighQ) { console.error(`REGRESSION: figure high-severity questions ${highQ} > baseline ${base.figHighQ}`); fail = true; }
    Object.entries(scr).forEach(([k, v]) => { if (base.screens && base.screens[k] && v.q > base.screens[k].q) { console.error(`REGRESSION: screen ${k} ${v.q} > baseline ${base.screens[k].q}`); fail = true; } });
  }
  process.exit(fail ? 1 : 0);
})();
