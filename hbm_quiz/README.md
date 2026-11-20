# HBM 이해도 평가 — 개선 작업 공간

- `original_v8.html` : 사용자가 업로드한 원본 (수정 금지, 비교 기준)
- `template.html`    : 원본에서 문항 DB 만 `__DB_B64__` 자리표시자로 뺀 앱 코드 (DA 소유)
- `data/NN_CODE.json`: 분야별 문항 (분야 에이전트 소유). 문항당 그림(fig)·지표(metrics)·지문을 인라인으로 가짐
- `tools/build.py`   : data → `dist/HBM_quiz.html` 패킹 (그림·지표·지문 중복 제거, raw-deflate+base64)
- `tools/smoke.js`   : 헤드리스로 전 문항 그림 렌더 + JS 오류 검사 (`node tools/smoke.js`)
- `docs/agents/`     : 에이전트 헌장·기준·작업 로그
- `docs/reviews/`    : 분야별 리뷰 보고서

문항 레코드: `id, lv(B/I/A), title, stem | (ctx, j, qt), opts[4], a(0-3), exp, k(1=상황도/0=주제도), fig[name, params], metrics[[icon,label,value]...]`
