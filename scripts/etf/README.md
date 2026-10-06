# 반도체 ETF 보유내역 추적

목적 하나다. **주요 반도체 ETF가 수량을 늘린 종목을 찾아 한국 종목으로 옮긴다.**
규격 정본은 `docs/collection-contract.md` **9절**, 서술·지면 규율은
`docs/common-report-guide.md` **[G7-5]** 다. 여기에는 실행만 적는다.

## 왜 비중이 아니라 수량인가

비중은 가격만 올라도 늘어난다. 비중 차이로 뽑으면 그냥 많이 오른 종목 목록이 나오고
그건 이미 가격에 있다. 그래서 가격 효과를 걷어낸다.

```
Δa_i = w_i,t − w_i,t−1 × (1+r_i) ÷ (1+r_P)       가격 보정 비중 변화
x_i  = (Q_i,t ÷ Q_i,t−1) ÷ (S_t ÷ S_t−1) − 1      초과 수량 변화 (S = 좌수)
```

두 값의 부호가 같을 때만 신호로 쓴다. 어긋나면 데이터를 먼저 의심한다.

## 실행

```bash
python3 scripts/etf/etf_holdings.py --fetch --tickers SOXX,SMH,XSD,SOXQ --out snap_YYYYMMDD.json
python3 scripts/etf/etf_holdings.py --delta snap_<이전>.json snap_YYYYMMDD.json
```

`--fetch` 는 ETF마다 iShares CSV를 먼저 시도하고 실패하면 stockanalysis HTML로 내려간다.
표준에러에 소스·기준일·종목수·좌수를 한 줄씩 찍는다. 그 줄을 리포트 데이터 신뢰도 박스에 옮겨라.

## 소스 상태 (2026-10-05 실측)

| 소스 | 결과 |
| --- | --- |
| iShares `latest-holdings.csv` | 200 / 6.4KB. Weight + **Quantity** + **좌수** 전부. 1순위 |
| stockanalysis `/etf/<티커>/holdings/` | 200. Weight + Shares. 좌수 없음 → `Δa` 만 |
| iShares 구 `<숫자>.ajax?fileType=csv` | HTML 반환. 쓰지 마라 |
| iShares `?asOfDate=` | 무시됨. **과거 스냅샷을 못 받는다** |
| VanEck SMH | 302 쿠키 루프. 쓸 수 없다 |
| KRX 정보데이터시스템 OTP | 본문 `LOGOUT`. 세션 없이는 안 된다 |
| stockanalysis `/quote/krx/<코드>/holdings/` | 200이나 두 달 지난 월말치 + 상위 10행. **변화 측정 불가** |

## 장부

스냅샷은 **Drive `etf_semis_weights`** 에 쌓는다. 저장소에 넣지 마라 —
4개 루틴이 동시에 쓰면 커밋이 충돌한다(기존 장부 규칙과 같다).
보관은 최근 10영업일 + 매월 말일.

★과거분을 어디서도 못 받으므로, 스냅샷을 거른 회차는 그 구간의 변화를 영구히 잃는다.★
