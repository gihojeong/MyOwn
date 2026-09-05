# 키움 수집기 사용 지침 — KOSPI 리포트 예약작업용

예약작업(Routine) 프롬프트가 이 문서를 가리킨다. 지침을 여기에 두는 이유는, 트리거
프롬프트를 세 개나 고치지 않고도 수집 항목과 주의사항을 바꿀 수 있게 하기 위해서다.

## 실행

예약작업 세션에는 저장소가 붙지 않으므로(`folders: []`) 스크립트를 URL로 받는다.
앱키는 환경변수(`APP_KEY` / `APP_SECRET` / `KIWOOM_MODE`)로 이미 주입돼 있다.
건드리지도, 출력하지도 마라.

```bash
curl -fsSL -o kiwoom_collect.py \
  https://raw.githubusercontent.com/gihojeong/MyOwn/master/scripts/kiwoom_collect.py

# 마감 리포트(47건) / 개장 전 브리핑(37건) / 주간 리뷰(26건)
python3 kiwoom_collect.py --preset close     --date <오늘YYYYMMDD>       --pause 0.3 --out kiwoom.json
python3 kiwoom_collect.py --preset premarket --date <직전거래일YYYYMMDD> --pause 0.3 --out kiwoom.json
python3 kiwoom_collect.py --preset weekly    --date <지난주금요일YYYYMMDD> --pause 0.3 --out kiwoom.json
```

순차 호출이라 3~6분 걸린다. **백그라운드로 던지고 그동안 Drive 읽기와 요인 분석용 웹
검색을 병렬로 진행하라.**

`summary.failed`가 빈 배열이면 전량 성공이다. 실패 항목이 있으면 **그 항목만** 웹 경로로
보완한다. 성공한 항목을 웹에서 다시 찾지 마라 — 시간 낭비이고, 웹 수치가 API 확정치와
어긋나면 **API가 옳다**(차이는 각주로 남겨라). 수집기가 아예 안 돌면(토큰 실패·네트워크)
그 사실을 리포트 말미에 명시하고 웹 경로로 전환한다.

## 결과 JSON의 어느 키가 어느 항목인가

경로는 `results.<키>.data`.

| 리포트 항목 | 키 | 내용 |
| --- | --- | --- |
| [A] 지수 | `index_kospi` `index_kosdaq` `index_kospi200` | 종가·전일대비·등락률·시가·고가·저가·거래대금·상승/보합/하락 종목수. **`inds_cur_prc_tm` 배열에 시간별 지수가 들어 있어 장중 궤적을 별도 조회 없이 그릴 수 있다** |
| [A] 업종 | `sector_indices_kospi` | 전업종지수 |
| [A-2] 시간외 | `after_hours_rank_rise` `after_hours_rank_fall` | 시간외 단일가 등락률 상·하위 |
| [A-2] 시간외 종목 | `after_hours_<종목명>` | `ovt_sigpric_cur_prc`(체결가) · `ovt_sigpric_flu_rt`(등락률) · `ovt_sigpric_acc_trde_qty`(거래량). 18:05 실행이면 확정돼 있다 |
| [B] 투자자별 | `investor_intraday_<투자자>` | 외국인·기관계·투신·연기금·보험·은행·국가·기타법인의 종목별 순매수(백만원). 시장 합계는 `netprps_amt` 합산 |
| [B] 3주체 원자료 | `investor_after_close` | 종목 단위 약 1,200행(연속조회로 전량 수신) |
| [B] 프로그램매매 | `program_trades_kospi` `program_trades_kosdaq` | 차익 `dfrt_trde_netprps` · 비차익 `ndiffpro_trde_netprps` |
| [B] 연속 순매수 | `investor_streak_5d` (주간은 `_20d`도) | 추세 지속인지 전환인지 판정용 |
| [B] 매매 상위 | `foreign_institution_top` | 외국인·기관 매매 상위 |
| [C] 업종 수급 | `sector_investor_flows_kospi` | 업종별 유출입 |
| [D] 관심종목 | `candle_daily_<종목명>` (주간은 `candle_weekly_`) | 일봉 600행 — 종가·시가·고저·거래량·거래대금 |
| [D] 종목 수급 | `investor_by_stock_<종목명>` | 종목별 투자자·기관 매매 |
| [D-2] 순위 | `amount_top` `change_rate_top_rise` `change_rate_top_fall` | 거래대금 상위, 등락률 상·하위 |

## 과거 사고가 구조적으로 막히는 지점

- **기타법인 잔차 역산 불필요** — `investor_after_close` 응답에 `etc_corp`가 직접 있다.
  프롬프트에 남아 있는 "3주체 합이 0으로 닫히지 않으면 잔차를 기타법인 몫으로 역산하라"는
  지시는 **무시하고** API 실측값을 그대로 써라.
- **삼성전자 우선주 누락 불가** — 보통주(005930)와 우선주(005935)를 처음부터 따로 받는다.
  2026-08-25에 우선주를 "확인 불가"로 두고 0%로 가정해 헤드라인이 92%→81%로 틀어진 사고가
  재발할 수 없다.
- **등락률 부호 오류 불가** — 키움 등락률에는 부호가 정확히 들어 있다.
  companiesmarketcap의 무부호 등락률이나 '마감' 제목을 단 장중 스냅샷 기사를 등락률
  소스로 쓸 이유가 이제 없다.

## 금융투자·사모펀드는 별도 계산

`ka10063`(=`investor_intraday_*`)에는 **금융투자와 사모펀드 코드가 없다.** 그 둘은
`investor_after_close`의 종목별 `fnnc_invt` / `samo_fund` 필드를 합산해서 구하라.

## 수집기에 없는 것 — 웹 경로 그대로 조사

KOSPI200 선물·베이시스·미결제, 원/달러, 국고채 금리, 공매도, **시가총액·상장주식수**,
해외 증시·지표.

[D-2] 시총 비중 계산의 시총·상장주식수는 stockdigging.com 등 기존 경로로 확보하되,
**등락률만은 반드시 키움 값을 써라.**
