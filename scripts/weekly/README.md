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

## 수급 이상치 — 보류하기 전에 교차검증한다

통상 범위를 벗어난 투자자별 수치를 봤을 때 **"검증 보류"는 마지막 수단**이다. 순서대로 돌린다.

1. **그 주 마지막 거래일의 마감 리포트 메일** — Gmail에서 `in:sent` + 그 날짜로 검색한다.
   그 회차가 이미 같은 수치를 다뤘을 확률이 가장 높다.
2. Drive 폴더 `1hLv3NpWB3I70y33ZSpmhYgU6MGU-0cbK` 의 `kospi_forecast_<그날>`.
3. 언론 3사 교차.

세 경로가 전부 비었을 때만 보류로 적고 분석에서 제외한다.
**교차검증을 건너뛴 보류는 보류가 아니라 누락이다.**

### 기타법인은 자기주식을 포함한다

`etc_corp`에는 자사주 매입이 들어간다. 대규모 매입·소각 국면에서 통상 범위(수백억)를
수십 배 넘기는 것은 **정상이며 모의서버 잔차가 아니다**. 개인 순매도를 기타법인이 그대로
받아내는 구조가 보이면 자사주를 먼저 의심한다.

> **2026-10-03 회차 실패 사례.** 기타법인 +14,822억(삼성전자 +5,387억 · SK하이닉스 +9,054억)을
> "통상의 수십 배"라는 이유만으로 보류 처리해 분석에서 뺐다. 같은 날 18:16 KST 마감 리포트가
> 이미 그것을 자사주 매입으로 확정하고 "자사주 1.48조가 아시아 리스크오프를 막고 7000 회복"을
> 제목에 달아 두었다. 위 1번 한 번으로 끝났을 일이고, 보류가 아니라 그 주의 핵심 발견이었다.

자사주 매입이 확인되면 그 규모를 **다음 거래일 전망의 "나머지" 블록 전제에 명시적으로 넣는다**
(매입 지속 = 상방 쿠션, 종료·소진 = 하방 리스크). 수급 절에만 적고 전망에서 빼면
분해는 맞고 예측은 틀린다.

## 검증 규칙

`verify_weekly.py`는 Outlook 금칙 태그, 태그 균형, `▲/▼` 부호 일치, `%` 포맷 누출,
필수 문구, 95KB 상한을 본다. 실패하면 **발송하지 않는다**.
