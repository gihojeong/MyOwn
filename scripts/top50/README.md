# Top50 ETF 루틴 — 채점 파이프라인

`score_top50.py` 하나로 전일 예측 채점이 끝난다. 서술·용어·예측력 블록은
`docs/common-report-guide.md`, 수집·단위·함정은 `docs/collection-contract.md` 8절이
정본이다. 이 README는 **이 루틴에만 있는 규약**만 적는다.

## 실행

```bash
rm -rf ~/.cache/kiwoom-collect                      # 계약 8-1
python3 scripts/kiwoom_collect.py --preset premarket --date 20261002 \
        --pause 0.25 --codes "$(cat codes.txt)" --out kw.json
python3 scripts/top50/score_top50.py kw.json forecast.psv \
        --cash 0.025 --futures -0.0582 --k200-ret 0.41 \
        --krx-ret 005930=0.000,005935=-1.711,000660=0.436 > score.json
```

- `forecast.psv` 는 Drive `top50etf_forecast_<기준일>` 의 `[STOCK TABLE]` 본문을 그대로 붙인
  파이프 구분 텍스트다. 머리행(`code|name|...`)은 자동으로 건너뛴다.
- Drive 평문 파일을 base64 없이 통째로 읽는 방법은 계약 8-3h 에 있다.
- `--codes` 는 51 BM + 8 워치 = 59종목. 285항목 중 284항목 성공이 정상이고
  실패 1건은 `krx_futures_today`(전 회차 구조적 미게시)다.

## 수익률 — 이 루틴에서 가장 틀리기 쉬운 곳

**일간 수익률은 같은 응답 안에서 닫는다.** `cur_prc − base_pric` 을 `base_pric` 으로 나눈다.
어제 회차가 기록해 둔 종가를 분모로 쓰면 안 된다 — 키움 통합가는 스냅샷마다 재생성되므로
2026-10-02 실측에서 **59종목 중 41종목**이 어긋났고 최대 1.65% 벌어졌다(계약 8-3g).
스크립트는 `drift_n` · `drift_max` 로 이 괴리를 매 회차 보고한다.

키움의 `cur_prc` 는 **전부 통합가(KRX+NXT)** 다(계약 8-3e). 거래소 정규장 확정 등락률을
아는 종목만 `--krx-ret` 로 덮어쓴다. 그 출처는 ① `krx_stocks` ② 당일 마감 회차가 Drive
`kospi_forecast_<다음거래일>` 에 남긴 기록(언론 3사 이상 교차) 둘뿐이다.

## 3분해 규약

```
모델 NAV = (1−cash) × 정규화 주식슬리브 + cash × 0 + 선물명목비율 × KOSPI200 수익률
액티브   = 배분 + (1−cash) × [섹터배분 + 종목선택]
배분     = (1−cash−1) × BM + 선물명목비율 × KOSPI200 수익률
섹터배분 = Σ (wp − wb) × (rb − BM)            ... Brinson–Fachler
종목선택 = Σ wp × (rp − rb)                   ... 상호작용 합산
```

- 비중은 **정규화 슬리브 기준**(Σwp = 100)으로 계산한 뒤 `(1−cash)` 를 곱한다.
- **BM 밖 섹터**(분모 없음)는 효과 전액을 배분으로 계상한다.
  BM 밖 종목이지만 섹터는 BM에 있는 경우는 통상 처리대로 배분·종목에 나뉘어 들어간다.
- 스크립트는 `residual` 이 1e−4 를 넘으면 **단정**으로 멈춘다. 항등식이 닫히지 않은 분해를
  리포트에 쓰지 않기 위해서다.

## 원장 기재

`top50etf_ledger` 에 한 행을 추가한다 — 일간 액티브 · 누적 · 3분해 · 종목 적중 · 구간 적중.
정보비율은 **n ≥ 20 이 되기 전까지 수치를 성과 판정으로 쓰지 않는다**(n=4 에서 신뢰구간이 ±8).

2026-10-05 리허설에서 정한 추가 기재 항목:

| 항목 | 이유 |
| --- | --- |
| 최빈 시나리오 실현 여부 | 편향 판정에 필요한데 기록이 없었다 |
| 거래비용 차감 후 액티브 | 4회차 모두 총액 기준이었다. 왕복 25bp 가정 시 회차당 −0.0038%p |
| 통합가 드리프트(`drift_n`/`drift_max`) | 분모 오염 감시 |
| 회차별 3분해 | 9/29·9/30 은 분해가 없어 손실원 비교가 안 됐다 |

## 리허설 규칙

리허설에서는 **메일을 보내지 않고 `kospi_forecast_*` · `top50etf_forecast_*` ·
`top50etf_ledger` 에 쓰지 않는다.** 정시 회차의 중복 발송 방지 장치가 Drive 기록을 보고
판단하므로, 리허설 기록을 남기면 정시 회차가 발행을 거부한다.
