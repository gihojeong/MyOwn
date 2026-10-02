# 주간 리뷰 빌드 파이프라인

2026-10-03 회차(대상 2026-09-28~10-02)에서 실제로 돌린 스크립트를 그대로 둔 것이다.
**날짜·예측값이 하드코딩돼 있다** — 다음 회차에서는 `score_weekly.py`의 `A`/`AM`/`PM`/`W`와
`calc_weekly.py`의 `S0`/`IDX0`/`FX`/`KO`를 그 주 값으로 바꿔 쓴다. 전량 자동화는 하지 않았다:
예측값(아침 `E`, 저녁 `E`, 80% 구간)은 Drive 예측기록·발송 메일에만 남아 있고 API에 없다.

## 실행 순서 (작업 디렉터리에서)

```bash
# 0) 수집 — 반드시 먼저. 캐시 토큰이 죽어 있을 수 있으니 ★먼저 캐시를 비운다★
rm -rf ~/.cache/kiwoom-collect
python3 scripts/kiwoom_collect.py --preset weekly --date 20261002 \
        --out kw_weekly2.json --log kw_weekly.log
# 기대치: 70항목 중 67 성공. krx_stocks/futures/options 3건 실패는 구조적 정상
# (KRX는 전일분을 익영업일 07:09~08:53 게시).

# 1) 미국 시세 추출 -> us.json
python3 scripts/weekly/extract_us.py

# 2) 국내 수집물 가공 -> calcw.json
python3 scripts/weekly/calc_weekly.py

# 3) 예측 채점 -> wk.json
python3 scripts/weekly/score_weekly.py

# 4) 메일 HTML 생성 -> weekly.html
python3 scripts/weekly/build_weekly.py

# 5) 검증 — PASS 없이는 발송하지 않는다
python3 scripts/weekly/verify_weekly.py
```

## ★토큰 무효화 — 이것 때문에 1차 시도가 6/70으로 떨어졌다

같은 `APP_KEY`로 **키움 MCP(`kiwoom-exec`)가 새 접근토큰을 발급하면 수집기가 캐시해 둔
토큰이 서버에서 무효화된다**(`8005 Token이 유효하지 않습니다`). 캐시는
`~/.cache/kiwoom-collect/token_demo.json`이다.

- 수집기의 `--check`는 **죽은 토큰에도 `token_issued=true`를 보고**하므로 사전 점검으로 못 잡는다.
- 규칙: **수집기 가동 전후로 `kiwoom_query`(MCP)를 호출하지 않는다.**
  명세 조회용 `kiwoom-spec`은 자격증명을 쓰지 않으므로 무관하다.
- 증상이 보이면 `rm -rf ~/.cache/kiwoom-collect` 후 재실행한다.
- 과제: `--check`가 실제 조회 1건으로 토큰 유효성을 검증하도록 바꾼다.

## 단위 — 틀리기 쉬운 곳

| API | 필드 | 단위 |
| --- | --- | --- |
| `ka10066` 투자자별 (`amt_qty_tp=1`) | `frgnr_invsr` `orgn` `ind_invsr` `etc_corp` … | **백만원** (억원 = /100) |
| `ka10051` 업종별 순매수 (`amt_qty_tp=0`) | `*_netprps` | **억원** |
| `ka90010` 프로그램 | `dfrt_trde_netprps` `ndiffpro_trde_netprps` | **백만원** |
| `ka20001`/`ka20003` | `trde_prica` | **백만원** |
| `ka90009` 외국인·기관 상위 | 금액 | 단위 불명 — **순위만 쓴다** |

`cur_prc` 등 가격 필드에는 **전일대비 부호가 접두**로 붙는다(`-201500`은 음수가 아니라 하락).
반드시 `abs()`를 취한다. 모의서버는 `flu_rt`/`trde_qty`/`pred_pre`를 0으로 돌려주므로
등락률은 가격에서 직접 계산한다.

투자자별 항등식: `개인 + 외국인 + 기관 + 기타법인 + 국가 + 내국인대우외국인 = 0`.
`etc_fnnc`(기타금융)는 기관의 하위 항목이므로 **기타법인(`etc_corp`)과 혼동하면 항등식이 깨진다**.

## ECOS 환율 시계열 (주간 분해에 필요)

공개 `sample` 키는 **최대 10건**이다. 주간 1회분이면 충분하다.

```bash
curl -s "https://ecos.bok.or.kr/api/StatisticSearch/sample/json/kr/1/10/731Y001/D/20260918/20261002/0000001"
```

## 검증 규칙

`verify_weekly.py`는 Outlook 금칙 태그, 태그 균형, `▲/▼` 부호 일치, `%` 포맷 누출,
필수 문구, 95KB 상한을 본다. 실패하면 **발송하지 않는다**.
