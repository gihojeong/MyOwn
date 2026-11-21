# W3 수정 라운드 지침 (FIX 에이전트, 오케스트레이터)

사용자 요청으로 **한 번에 한 에이전트만** 순차 실행한다. 각 FIX 에이전트는 지정된 분야 2–3개를 차례로 처리한다.

## 분야마다 읽을 것 (이 3개가 할 일의 전부)
1. `docs/reviews/EA_audit/<CODE>.md` — EA 감사 수정 지시 (+ 보강 권고)
2. `docs/reviews/xd3/<CODE>.md` — XD W3 지시 (조치 문항, 사실 충돌, 개념 보강). **mv 판정(이관 수용/이관 후 삭제)은 손대지 말 것 — EA Phase 2 가 처리**
3. `docs/reviews/<CODE>.md` — 분야 W2 보고서 (맥락)
공통 규칙: `docs/agents/STANDARDS.md`(특히 2.5 — refresh 판정 die = 최하단 core die), `LAYOUT_RULES.md`(그림 param·hideResult/hideNames/hideLabels/notes), `W2_COMMON.md`(작업 방식·검사 명령), `docs/agents/CONVENTIONS_W3.md`(분야 간 공통 가정값; 없으면 THERM 배치가 만든다).

## 할 일
- EA·XD 지시를 **전부** 반영 (수정/삭제/하향 재발급(prev)/근중복 정리). 계산은 스크립트로 재계산해 정답·오답 값 재현 확인.
- **보강**: EA 감사의 '보강 권고' 수량과 XD 의 '개념 보강'(문항집에서 0이 된 개념)을 신규 9xxx 로 출제. 보강 문항도 기준서 전 조건(오답=특정 오개념/계산 실수, 해설 ①–④ 대응, 그림 정답 노출 금지, 가정값 명시) 충족.
- 데이터는 분야 파일만, 보고서 `docs/reviews/<CODE>.md` 에 "W3 수정" 절 추가(반영 항목 표, 신규 목록, 남은 우려).
- 게이트: `python3 tools/validate.py --domain CODE --gate --out <scratchpad>/val_CODE.md` (공용 출력 덮어쓰기 금지; --out 지원 안 되면 실행 후 `git checkout docs/reviews/_auto_latest.md`), build/smoke 는 scratchpad 출력.
- commit 금지. 사용량 절약: 필요한 문항만 스크립트로 출력해 읽고, 파일 전체를 컨텍스트에 올리지 말 것.

## 최종 응답
분야별: 반영 건수(EA/XD), 삭제·하향·신규 수, 최종 B/I/A, 주요 정정 3개, 남은 우려. 한국어로 간결하게.
