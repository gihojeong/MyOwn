# 루틴 프롬프트 교체본 (routine/)

이 폴더는 ★스케줄 루틴의 프롬프트 전문★ 을 보관한다.
상위 폴더의 `*.live-*.txt` 는 회차별 수집 항목·해석 규율 문서이고, 이것과 다르다.

| 파일 | 대상 루틴 | trigger id |
|---|---|---|
| `premarket.routine-20261017.txt` | KOSPI 개장 전 브리핑 (평일 05:53) | `trig_011Xk4Dwx4WVGFBmDfPbdfUt` |
| `close.routine-20261017.txt` | KOSPI 마감 리포트 (평일 17:30) | `trig_01PMVsmiPUb6GmNGm9QhdWhU` |
| `weekly.routine-20261017.txt` | KOSPI 주간 리포트 (토 07:00) | `trig_011KQ8Sa3V4HkbaharfftbUW` |
| `research-digest.addendum-20261017.txt` | BJ투자 모닝 리서치 브리프 (매일 05:47) | `trig_01FSGeLAnEoxoVKaa5cuH6b1` |

## 2026-10-17 판에서 고친 것

세 KOSPI 루틴은 규격 문서를 `master` 에서 curl 로 받으므로 문서가 프롬프트를 이긴다.
그래서 프롬프트의 "안전망" 문구는 ★문서를 못 받은 날에만★ 작동하는데, 그 문구가 낡아 있었다.

1. **8050** — "수집기가 12회 재시도한다" → 핀 연결(`_PINNED`/`_drop_conn`, 커밋 `0ae3326`,
   제안 P53)로 재시도 91회 → 0회. `[retry]` 줄이 안 나오는 것이 정상이라고 명시.
   "포털에 IP 재등록" 권고를 철회(정정 22).
2. **장부 처분** — 마감·주간에 남아 있던 "구판 trash" → P32 의 rename(보관판) 방식.
   `base64` 로 전사하지 말고 `read_file_content` 로 원문을 읽으라는 경고 추가(교훈 35).
3. **저장소 동기화** — 상주 세션(개장 전·마감)에 0.5단계 `git pull --ff-only` + `grep -c`
   확인 2줄. 주간은 매 회차 새 세션이므로 확인만.
4. **증시자금 블록** — 개장 전에만 있던 의무를 마감·주간에도 넣었다(P52: 가중 0, 서술 전용).
5. **주간의 낡은 판정 요청 제거** — P10·P15·P17·P18 은 이미 결정됐다. 대신 이 회차의 실제
   임무(갭 계수 구간 재추정 · P51 5블록 판정 · 아침 편향 추이로 z 재검토)로 바꿨다.
   브랜치 폴백(`ccr-9241c52a-m2aesm`)도 분기 해소로 제거.
6. **주간에 수집 명령 명시** — `--preset weekly` 가 프롬프트에 없어 암묵이었다.

## 적용

`mcp__Claude_Code_Remote__update_trigger` 의 `prompt` 로 전문을 교체한다.
상주 세션에 묶인 루틴은 ★그 세션에서만★ 편집되는 경우가 있으니, 거부되면 해당 루틴의
대화나 `https://claude.ai/code/routines/<trigger id>` 에서 붙여 넣는다.
