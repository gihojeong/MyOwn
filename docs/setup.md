# 세팅 — 키움 REST · KRX OpenAPI · ECOS 수집 경로

이 문서는 **수집 경로를 처음 붙이거나 키를 갈아끼울 때** 보는 문서다.
회차(개장 전·마감·주간)를 돌리는 절차는 `docs/collection-contract.md`, 응답 필드 해석은
`docs/kiwoom-report-playbook.md`에 있다.

한 줄 요약: **키는 환경변수로만 주입한다. 파일·커밋·프롬프트에 값을 쓰지 않는다.**
검증은 `python3 scripts/setup_check.py` 한 줄로 끝낸다.

---

## 0. 현재 상태 (2026-09-28 실측)

| 경로 | 상태 | 비고 |
| --- | --- | --- |
| 키움 REST `demo`(mockapi) | **정상** | 토큰 발급 · ka20001 조회 성공. 시세는 실제 시장값이다 |
| 키움 REST `real`(api) | **미구성** | 주입된 앱키가 모의투자 전용 — `8030 투자구분이 달라서 Appkey를 사용할수가 없습니다` |
| KRX `sto/stk_bydd_trd` (유가증권 전종목) | **정상** | 942행 |
| KRX `drv/fut_bydd_trd` (선물) | **정상** | 385행 |
| KRX `drv/opt_bydd_trd` (옵션) | **정상** | 16,724행 |
| KRX `idx/krx_dd_trd` (지수) | **정상** | 40행 |
| KRX `sto/ksq_bydd_trd` (코스닥 전종목) | **401 미신청** | 서비스별로 신청이 따로다 |
| ECOS | **sample 폴백** | 전용 키 없음. 원/달러·국고채는 받아지지만 1회 10행 제한 |

같은 날 `--preset close`(90항목) 실측: **77/90 성공.** 실패 13건은 전부 알려진 유형이다.

- 시간외단일가 10건 → `1504` **모의투자 미제공**(계약서 6절 5번). 코드 문제가 아니다.
- `krx_futures` · `krx_options` · `krx_stocks` 3건 → **당일 저녁 미게시**(6절 3번).
  KRX 확정치는 다음 아침 회차가 전일자로 받는다.

즉 **지금 상태로 세 회차를 돌릴 수 있다.** 아래 1~3절은 남은 구멍을 메우는 작업이다.

---

## 1. 키 4종 — 무엇을 어디서 받는가

| 환경변수 | 필수 | 발급처 | 주의 |
| --- | --- | --- | --- |
| `APP_KEY` / `APP_SECRET` | **필수** | 키움증권 [OpenAPI](https://openapi.kiwoom.com) → REST 앱키 | **실전용과 모의용이 별개 키다.** 섞이면 `8030` |
| `KIWOOM_MODE` | 선택 | — | `demo`(기본, mockapi) 또는 `real`(api). 키의 구분과 일치해야 한다 |
| `KRX_AUTH_KEY` | **필수** | [KRX OpenAPI](https://openapi.krx.co.kr) → 인증키 발급 | **서비스별로 이용신청을 따로 승인받는다**. 키 하나로 전부 열리지 않는다 |
| `ECOS_API_KEY` | 선택 | [한국은행 ECOS](https://ecos.bok.or.kr/api) (무료·즉시) | 없으면 공개 `sample` 키로 동작. 원/달러·국고채 수집에만 쓰인다 |

### 키움 — 실전(`real`)으로 올릴 때

1. 키움 OpenAPI에서 **실전투자용** REST 앱키를 따로 발급받는다(모의용 키는 재사용 불가).
2. `APP_KEY` / `APP_SECRET`을 실전 키로 교체하고 `KIWOOM_MODE=real`로 바꾼다.
3. `python3 scripts/setup_check.py`가 `real 토큰 … 발급 성공`을 찍는지 확인한다.

실전으로 올리면 얻는 것은 **시간외단일가 10항목**(`ka10087`·`ka10098`)이다. 시간외는
지수 산출에 반영되지 않아 결산 영향이 낮으므로, 이 한 항목만으로 서둘러 바꿀 이유는 없다.
계약서 5절의 **거래소 접미사(`005930_NX` / `_AL`) 재시험**은 실전 키가 들어오면 해야 할 일이다.

### KRX — 코스닥 전종목을 열 때

`sto/ksq_bydd_trd`만 401이다. KRX OpenAPI 마이페이지에서 **코스닥 일별매매정보 서비스를
추가 신청**하면 같은 키로 열린다. 승인까지 영업일 기준 시간이 걸린다.

### ECOS — 전용 키를 넣을 때

`sample` 키는 1회 10행 제한이 있다. 수집기는 항목별로 나눠 부르므로 지금은 걸리지 않지만,
연휴가 길면 조회창(`ECOS_LOOKBACK_DAYS=10`) 안에 기준일이 안 들어올 수 있다. 무료 발급이므로
넣어 두는 편이 낫다.

---

## 2. 환경변수 주입

키는 **환경 설정에 넣는다.** 세션 제목줄의 클라우드 환경 메뉴 → **Edit** → `API credentials`
항목(없으면 환경변수)에 아래 이름 그대로 등록하면, **새 세션이 그 값을 물고 뜬다.**

```
APP_KEY, APP_SECRET, KRX_AUTH_KEY, ECOS_API_KEY, KIWOOM_MODE
```

- **키 값을 대화창에 붙여넣지 마라.** 환경 설정에만 넣는다.
- 웹 콘솔에서 복사하면 제로폭 문자(U+200B 등)가 딸려오는 일이 흔하다. 수집기와 진단기가
  읽는 즉시 털어내므로 실패 원인은 아니다. 실제로 지금 `KRX_AUTH_KEY`에 1개 섞여 있다.
- 로컬에서 임시로 돌릴 때만 셸에 `export`한다. `.env` 파일을 만들어 커밋하지 마라
  (`.gitignore`가 막아 주지 않는 이름이다).

---

## 3. 검증 — 한 줄

```
python3 scripts/setup_check.py              # 사람이 읽는 표
python3 scripts/setup_check.py --json       # 기계가 읽는 JSON (예약작업용)
python3 scripts/setup_check.py --skip-krx   # KRX 게시일 탐색이 느릴 때
```

네 경로를 한 번에 본다. 종료 코드는 **필수 경로가 전부 살아 있을 때만 0**이다.

1. 환경변수 — 존재·길이·비가시 문자. **값은 출력하지 않는다.**
2. 키움 — `demo`·`real` 양쪽에 토큰을 발급해 **키의 투자구분을 판정**하고, 살아 있는 쪽으로
   지수 조회(ka20001)를 1건 실제로 쏜다. 토큰만 보면 api-id 권한을 알 수 없다.
3. KRX — 기준일이 휴장일이면 전 서비스가 0행이 되어 **미신청과 구분되지 않는다.** 그래서
   기준일에서 뒤로 걸어가며 행이 있는 날을 먼저 찾고, 그 날짜로 전 서비스를 찍는다.
   401(미신청)과 200+0행(미게시)은 다른 말이다 — 계약서 6절.
4. ECOS — 전용 키인지 `sample` 폴백인지 밝히고 원/달러 1건을 받아 본다.

기존 점검기와의 관계:

| 도구 | 보는 범위 | 쓸 때 |
| --- | --- | --- |
| `scripts/setup_check.py` | 네 경로 전부 | **세팅·키 교체 후** |
| `kiwoom_collect.py --check` | 키움 토큰 발급까지 | 회차 시작 전 5초 게이트(계약서 1절 ②) |
| `scripts/close-report/krx_probe.py` | KRX 선물·옵션 게시 여부 | 회차 중 파생이 실패했을 때 |

---

## 4. 수집 실행

```
# 마감 (평일 18:05) — 당일
python3 scripts/kiwoom_collect.py --preset close    --pause 0.25 --out data/close_$(date +%Y%m%d).json

# 개장 전 (평일 06:00) — 직전 거래일을 --date로 못박는다
python3 scripts/kiwoom_collect.py --preset premarket --date 20260925 --pause 0.25 --out data/pre.json

# 주간 (토 06:00)
python3 scripts/kiwoom_collect.py --preset weekly    --pause 0.25 --out data/weekly.json

# 단건 디버깅
python3 scripts/kiwoom_collect.py --call ka20001 --path /api/dostk/sect --body '{"mrkt_tp":"0","inds_cd":"001"}'
```

- 기준일은 **달력이 아니라 실제 거래일로 확정하라.** 2026 추석은 9/24~9/26이 휴장이었고
  그 구간에서 "직전 거래일"은 하루 앞이 아니다.
- close 결과 JSON은 약 6MB다. **Read 도구로 열지 말고** `python3 -c`로 필요한 키만 뽑아라.
- 결과물(`data/`, `kiwoom.json`, `*.log`)은 `.gitignore`가 막는다. 원자료를 커밋하지 마라.

---

## 5. 알아 두어야 하는 세 가지 함정

1. **종가는 KRX, 시세는 키움.** 키움 `cur_prc` 계열은 NXT 체결(15:40~20:00)을 포함하므로
   정규장 종가가 아니다. 종가·시가총액·상장주식수는 KRX 확정치를 쓴다(계약서 5절).
2. **지수 값의 부호는 방향 표시다.** `index_kospi.cur_prc = -6889.74`는 음수 지수가 아니라
   **6,889.74 하락**이다. 절댓값을 쓰고 부호는 `flu_rt`로 읽어라.
3. **`1504 해당 URI에서는 지원하는 API ID가 아닙니다`는 경로 문제가 아니다.** 모의투자에
   그 api-id가 없는 것이다. 같은 URI의 다른 api-id가 성공하면 그것으로 갈린다.

---

## 6. 금지

- 자격증명 값을 **출력·기록·커밋하지 마라.** 유무와 길이만 적는다.
- 주문 도구를 쓰지 마라. 이 저장소는 **읽기 전용 수집**이다.
- 실패를 뭉쳐 적지 마라. 미신청·미게시·이그레스 차단·모의 미제공은 **다른 사건**이다
  (계약서 6절의 다섯 유형).
