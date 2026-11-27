---
name: hbm-quiz
description: HBM 이해도 평가 문항집(hbm_quiz/) 작업 — 문항 추가·수정·검토, 그림/디자인 수정, 빌드·검증, EA(총괄)·DA(디자인) 역할 운영. "HBM 문항", "HBM 퀴즈", "EA에게", "DA에게", 분야 코드(TSV, BSP, BUMP, SAW, COW, WARP, THERM, SIP, FA, PROD, DRAM, MET, MIX, FEOL) 언급 시 사용.
---

# HBM 이해도 평가 문항집 작업 규칙

사용자는 반도체 패키징 전문가다. "장난처럼 여기지 말 것" — 정확성 최우선. 동시에 **주간 사용량 절약**을 요구한다.

## 1. 구조 (먼저 `hbm_quiz/README.md`)
- `hbm_quiz/data/NN_CODE.json` — 분야별 문항(14개). 레코드: `id, lv(B/I/A), title, stem | (ctx, j, qt), opts[4], a, exp, k, fig[name, params], metrics, src?, vx?, prev?`
- `hbm_quiz/template.html` — 앱 코드(그림 템플릿 f_* 포함). DA 소유.
- 기준 문서 (반드시 따른다):
  - `hbm_quiz/docs/agents/STANDARDS.md` — 난이도 정의, 사실 기준(출처 등급 [S]/[V]/[R]), **용어 규약 2.5** (N단 = core N + base 1, 간극 N개 / Smile = ∪, Cry = ∩ (위에서 본 형상, 자세 명시) / front-to-back 적층 / refresh·온도 판정 = 최하단 core die / 공법명 TC-NCF·MR-MUF·HCB), 문항 요건, 부록 A 그림 params
  - `hbm_quiz/docs/agents/CONVENTIONS_W3.md` — 분야 간 공통 가정값 C1 접합층 열저항, C2 D2W HCB overlay(= pitch 의 5–10 %, pitch 명시), C3 변당 스택 수, C4 EM Ea
  - `hbm_quiz/docs/agents/LAYOUT_RULES.md` — 글자 수 상한, 그림 param, 정답 노출 방지 옵션(hideResult, hideNames, hideLabels, notes, labels)
  - `hbm_quiz/docs/reviews/_facts.md` — 사실 검증 판정(사용 금지 주장 포함)
  - `hbm_quiz/docs/reviews/SIGNOFF.md` — 최종 서명과 남은 위험
- 분야별 이력: `hbm_quiz/docs/reviews/<CODE>.md`, 감사: `docs/reviews/EA_audit/`

## 2. 문항 작성·수정 규칙 (요약 — 상세는 STANDARDS)
- 오답 하나 = 오개념 하나 또는 **특정 계산 실수로 재현되는 값**(해설에 그 계산을 적는다). "자릿수만 틀린 값"·기술 외 사유 오답 금지.
- 해설: 정답 근거 + 오답 각각의 이유, 계산은 식·대입·결과. 해설의 ①–④ 는 현재 보기 순서와 일치.
- k=1 이면 그림 수치 = 지문 수치, 그림이 정답을 보여 주면 안 됨. 가정값은 지문에 "가정/설정값"으로 명시.
- 업체 소문·[R] 출처는 정답 근거 금지. 불확실하면 출제하지 않는다.
- 새 id: `CODE-LV-9xxx` (파일 내 최대 번호 다음). 난이도 변경 시 새 id + `prev`. 삭제는 분야 보고서에 사유.
- 신규 문항의 정답 위치는 같은 분야·난이도 그룹에서 가장 적은 위치로(①–④ 각 25 % ± 3 % 유지). 수치 보기는 오름차순 유지.
- 계산 문항은 반드시 스크립트로 정답·오답 값을 재계산(`hbm_quiz/tools/num/` 재사용 가능).

## 3. 완료 게이트 (변경 후 항상)
```
cd hbm_quiz
python3 tools/validate.py --gate --out /tmp/val.md      # 차단 E 0, W 0 (공용 _auto_latest.md 덮어쓰기 피하려면 --out)
python3 tools/build.py                                   # → dist/HBM_quiz.html
node tools/smoke.js dist/HBM_quiz.html                   # figErr [], figEmpty [] (빈 좌표계 0), errs []
node tools/layout_check.js --out /tmp/layout             # figHighQ 0, 화면 결함 0 (공용 갱신은 --publish)
node tools/e2e.js dist/HBM_quiz.html                     # 구성 스크롤·클릭·응시·채점 흐름 (3개 화면 폭)
```
- **렌더 육안 점검(DA, 필수)**: `node tools/sheets.js <outDir> <LV> dist/HBM_quiz.html <CODE>` 로 바뀐 그룹의 그림을 실제 렌더한 접촉 인화지(12문항/장)를 만들고 **모든 장을 직접 본다**. 판정 항목: ① 빈 좌표계·누락 곡선·깨진 도형 ② 문항 주제와 그림 불일치(일반 주제도가 다른 주제 문항에 붙은 경우 포함) ③ 정답 노출(표·주석·flag·치수 라벨) ④ 글자 겹침·잘림. 결함 0 이 될 때까지 고친 뒤 다시 렌더해 확인한다. 자동 검사(validate·smoke·layout_check)는 ②·③ 을 잡지 못한다(2026-11-22 사용자 지적: BUMP-B-0067 빈 IMC 그래프·주제 불일치).
- **그림 품질 기준(BJ 지정 2026-11-22)**: 기준 이미지 `/mnt/project-files/hbm_quiz/ref/CVD_그림품질기준.jpg`(CVD 챔버 3D 단면 개념도) 수준을 목표로 한다. 갖출 것: ⑤ 입체감(cutaway 단면, 재료 음영·두께, 사선 투영) ⑥ 공정·물질 흐름 화살표(가스·물·열·전류) ⑦ 부위 라벨은 테두리 박스 + 리더선(끝점 점) ⑧ 결과·확대는 인셋 박스로 분리 ⑨ "개념도·과장 표시" 각주. 그림 틀: `f_chamber`(공정 챔버: CVD·ALD·식각·PVD), `f_pkg3d`(2.5D 패키지: lid·TIM·HBM·SoC·µbump·interposer·C4·underfill·BGA), `f_blade`(blade dicing: blade·flange·노즐·dressing·날 끝 인셋). 새 그림은 이 문법으로 만들고, 평면 사각형 단면·관점 카드(f_note)는 맞는 틀이 없을 때만 쓴다. **정답 노출 금지는 그대로** — 라벨이 정답이면 `hideLabels`(→ "부위 A…", 필요한 라벨만 `keepLabels`) 또는 `labels:{key:false|"글자"}`. 렌더 점검 판정에 ⑤–⑨ 를 더한다(새 그림·고친 그림 대상).
배포본은 `dist/HBM_이해도평가_v<N>.html` 로 복사해 사용자에게 보낸다.

## 4. 역할 운영 (사용자는 EA·DA 와 대화한다)
- **EA (총괄)**: 내용 품질 책임 — 기준서·검사기(`tools/validate.py`) 소유, 문항 감사, 최종 서명. "EA에게: …" 는 EA 역할로 처리.
- **DA (디자인)**: `template.html`·`layout_check.js`·LAYOUT_RULES 소유 — 화면·그림 배치(겹침 없음)·반응형·다크모드. 그림 기본 동작을 바꾸면 영향 문항을 스크립트로 확인하고 LAYOUT_RULES §7 에 기록.
- 분야 작업이 크면 분야별 서브에이전트를 쓰되 **한 번에 하나씩 순차 실행**(사용자 요청: 주간 한도 보호). 기억이 큰 기존 에이전트를 재호출하기보다 필요한 문서만 읽는 새 에이전트를 띄운다. 기계적 일괄 처리는 가벼운 모델로.
- 제출 전: EA 내용 점검 → DA 디자인 점검 → (EA 수정이 있으면) 게이트 재실행 → 공동 서명(`SIGNOFF.md` 갱신, 남은 위험 사용자 고지).

## 5. 주의
- 저장소 루트 `.gitignore` 의 `data/` 규칙 때문에 `!hbm_quiz/data/` 예외가 필요하다(이미 추가됨) — 데이터 커밋 누락 확인.
- 인라인 주석을 코드 앞에 붙일 때 같은 줄의 코드가 주석 처리되지 않게 주의(과거 구성 화면 스크롤 버그 원인).
