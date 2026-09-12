# KOSPI 리포트 예약작업 — 키움 REST API 연동

KOSPI 마감 리포트·개장 전 브리핑·주간 리뷰 예약작업이 지금은 AlphaSquare·언론 기사·
Investing.com을 페치해 데이터를 모은다. 이 경로는 리포트 프롬프트에 기록된 것만으로도
아래 실패가 반복됐다.

- `companiesmarketcap.com` 등락률에 부호가 없어 -6.46%를 +6.46%로 읽음
- 마감시황 제목을 단 기사가 실제로는 15시 장중 스냅샷 (삼성전자 +0.78% vs 확정 +1.17%)
- 삼성전자우를 확인 불가로 두고 0%로 가정 → 헤드라인 수치가 92%에서 81%로 어긋남

키움 OpenAPI는 이 항목들을 확정 종가·공식 수급으로 직접 준다. 교차검증 대상이 아니라
1차 소스로 쓸 수 있고, 부호 누락이나 장중 스냅샷 오인이 구조적으로 발생하지 않는다.

## 현재 상태 — 예약작업에서는 아직 동작하지 않는다

예약작업은 클라우드 환경에서 새 컨테이너로 뜨는데, 그 환경의 네트워크 정책이
키움 도메인을 막고 있다. 실측:

```
$ curl https://mockapi.kiwoom.com/oauth2/token
curl: (56) CONNECT tunnel failed, response 403

$ curl "$HTTPS_PROXY/__agentproxy/status"
"recentRelayFailures": [
  {"kind":"connect_rejected","host":"api.kiwoom.com:443",
   "detail":"gateway answered 403 to CONNECT (policy denial or upstream failure)"},
  {"kind":"connect_rejected","host":"mockapi.kiwoom.com:443", ...}
]
```

더미 키로도 동일하게 CONNECT 단계에서 403이 난다. 즉 자격증명 문제가 아니라
TLS 터널 자체가 정책으로 거부된다.

### 필요한 조치 (환경 소유자만 가능)

claude.ai/code 메시지 입력창 위쪽 줄의 **클라우드 아이콘**(현재 환경 이름이 적혀 있다)을
눌러 환경 선택기를 열고, 해당 환경에 마우스를 올렸을 때 나타나는 **설정 아이콘**을 누른다.
환경 설정에는 전용 URL이 없다.

1. **네트워크 허용** — **Network access**를 `Custom`으로 바꾸고 **Allowed domains**에
   한 줄에 하나씩 적는다.

   ```text
   api.kiwoom.com
   mockapi.kiwoom.com
   ```

   **Also include default list of common package managers**를 반드시 체크한다.
   체크하지 않으면 적은 도메인만 허용되어 기존 예약작업이 쓰는 AlphaSquare·언론사
   페치가 전부 끊긴다. GitHub 트래픽은 별도 프록시를 타므로 이 목록과 무관하다.

2. **자격증명 주입** — 예약작업이 뜨는 컨테이너에는 로컬 PC의 `.claude.json`이 없다.
   같은 대화상자의 **Environment variables**에 `.env` 형식으로 적는다.

   ```text
   APP_KEY=발급받은_앱키
   APP_SECRET=발급받은_시크릿
   KIWOOM_MODE=demo
   ```

   `KRX_AUTH_KEY`(한국거래소)를 함께 넣으면 KOSPI200 선물·옵션까지 수집된다. 키움 REST
   OpenAPI에는 국내 파생이 아예 없어서(2026-09-05 확인: `spec_groups`에 선물·옵션 그룹 없음,
   실시간 스트림 21종도 전부 주식·ETF·ELW·업종, 선물 종목코드를 시세 API에 직접 넣어도 빈 응답)
   이 한 항목만 외부 소스를 쓴다. 없으면 그 두 항목만 건너뛴다.

   `ECOS_API_KEY`(한국은행)는 선택이다. 없으면 공개 `sample` 키로 동작하고,
   이 수집기의 질의는 sample의 1회 10행 제한 안에 들어가므로 결과가 같다.
   발급은 무료·즉시(https://ecos.bok.or.kr/api)이며, 넣어 두면 조회 창을
   넓혀도 잘리지 않는다.

   Pro·Max 플랜의 **API credentials** 기능은 이 용도에 쓸 수 없다. 그쪽은 키를
   요청 **헤더**에 붙여주는 방식인데, 키움 `/oauth2/token`은 `appkey`/`secretkey`를
   요청 **body**로 받기 때문이다.

두 설정 모두 **세션 시작 시점에 한 번 읽힌다.** 이미 돌고 있는 세션에는 반영되지 않으므로,
변경 후에는 새 세션에서 검증해야 한다.

참조: https://code.claude.com/docs/en/cloud-environments

## 수집기

`scripts/kiwoom_collect.py` — 표준 라이브러리만 쓴다. 예약작업 컨테이너는 매번
새로 뜨므로 `uv sync`(약 140MB)나 MCP 기동 없이 즉시 실행되어야 한다.
`urllib`은 `https_proxy`와 `SSL_CERT_FILE`을 자동으로 따르므로 프록시 환경에서
추가 설정이 필요 없다.

```bash
# 자격증명·도달성 점검 (토큰 발급까지만)
python3 scripts/kiwoom_collect.py --check

# 마감 리포트 (평일 18:05) — 89건
python3 scripts/kiwoom_collect.py --preset close --out data/close_$(date +%Y%m%d).json

# 개장 전 브리핑 (평일 06:00) — 80건. --date에 직전 거래일을 넘긴다
python3 scripts/kiwoom_collect.py --preset premarket --date 20260904 --out data/pre.json

# 주간 리뷰 (토 06:00) — 69건
python3 scripts/kiwoom_collect.py --preset weekly --out data/weekly.json

# 임의 API 단건 (스펙 확인·디버깅)
python3 scripts/kiwoom_collect.py --call ka20001 --path /api/dostk/sect \
    --body '{"mrkt_tp":"0","inds_cd":"001"}'
```

자격증명은 환경변수로만 받는다. 인자로 받으면 프로세스 목록과 셸 히스토리에 남는다.

개별 호출이 실패해도 전체를 중단하지 않고 결과 JSON에 `error`로 남긴다. 리포트에서
"확인 불가"가 **데이터 부재**를 뜻하는지 **수집 실패**를 뜻하는지 구분하기 위해서다.
`summary.failed`에 실패한 항목 이름이 모인다.

관심종목은 `WATCHLIST` 상수(삼성전자·삼성전자우·SK하이닉스·SK스퀘어·두산에너빌리티·
LG에너지솔루션·삼성전기·현대차)이며 `--codes 005930:삼성전자,000660:SK하이닉스` 형태로
덮어쓸 수 있다. 삼성전자 보통주와 우선주를 따로 두는 이유는 자사주 소각 국면에서
둘의 등락률이 갈리기 때문이다.

## 리포트 항목 ↔ API 매핑

요청 파라미터는 전부 `spec_show` / `kiwoom_help`로 확인한 값이다. 추측으로 채운 항목은 없다.

| 리포트 항목 | API | preset | 비고 |
| --- | --- | --- | --- |
| [A] KOSPI/KOSDAQ/K200 종가·시가·고저·등락률·거래대금·상승하락 종목수 | `ka20001` ×3 | 전부 | `inds_cur_prc_tm`에 시간별 지수가 동봉되어 **장중 궤적**도 함께 |
| [C] 업종별 등락 | `ka20003` | 전부 | 전업종지수 |
| [B] 외국인·기관계·투신·연기금·보험·은행·기타법인 순매수 | `ka10063` ×7 | 전부 | 투자자별로 나눠 호출해야 세부주체가 분리됨 |
| [B] 3주체 항등식 검산 원자료 | `ka10066` | 전부 | 종목 단위 행. **`etc_corp`가 응답에 있어 기타법인 잔차 역산이 불필요** |
| [C] 업종별 유출입 | `ka10051` | 전부 | |
| [B] 외국인·기관 순매수 상위 | `ka90009` | 전부 | |
| [B] 최근 5·20거래일 연속 순매수 | `ka10131` | 전부 | 오늘 수급이 추세 지속인지 전환인지 판별 |
| [D-2] 거래대금 상위 | `ka10032` | close, premarket | |
| [D-2] 등락률 상하위 | `ka10027` ×2 | close, premarket | 상승률·하락률 각각 |
| [A-2] 시간외 단일가 등락 상하위 | `ka10098` ×2 | close | |
| [A-2] 관심종목 시간외 체결 | `ka10087` ×8 | close | 18:05 실행이라 시간외(18:00 종료) 데이터가 확정돼 있음 |
| [D] 관심종목 일봉 | `ka10081` ×8 | close, premarket | |
| [D] 관심종목 종목별 투자자 | `ka10059` ×8 | close, premarket | |
| [D] 관심종목 주봉 | `ka10082` ×8 | weekly | |
| [D-2] 시가총액·상장주식수·PER/PBR·52주 고저 | `ka10001` ×8 | 전부 | `mac`(억원) · `flo_stk`(천주). 웹 조사가 필요 없어졌다 |
| [B] 종목별 공매도 추이 | `ka10014` ×8 | 전부 | 최근 10여 거래일 수량·비중·잔고·평균가 |
| [E] 미국 증시·원자재·금리 대용 ETF, 반도체 개별주 | `usa20590` ×12 | 전부 | SPY·QQQ·DIA·SOXX·GLD·USO·TLT·UUP + NVDA·TSM·MU·AVGO |
| [E] 원/달러·국고채 3/10/30년·CD91·회사채AA- | ECOS `731Y001` `817Y002` ×6 | 전부 | 키움 밖. 한국은행 확정치 |

**끝내 못 채우는 것**: KOSPI200 선물·베이시스·미결제약정. 키움 REST OpenAPI는
국내주식과 미국주식만 다루고 파생 시세가 없다(`spec_groups` 확인). 한국거래소
OpenAPI(`data-dbg.krx.co.kr`)에 파생 일별시세가 있지만 별도 무료 키가 필요하고,
이 한 항목 때문에 의존처를 늘리는 것보다 웹 경로를 유지하는 편이 낫다고 봤다.

**해외 지수를 ETF로 대신하는 이유**: 키움 해외주식 API에 지수 시세가 없다.
SPY/QQQ/DIA/SOXX로 방향과 등락폭은 정확히 읽히지만 배당·추적오차 탓에 지수
등락률과 소수점 단위로 어긋나므로, 리포트에는 "SPY 기준"임을 밝히도록
playbook에 명시해 두었다.

**키움 환율(`ust31301`)을 쓰지 않는 이유**: 모의투자에서 거절되고
(2026-09-05 실측 `RC9000`), 실전에서도 "환전 적용 고시환율"이라 시장 종가와 다르다.
원/달러는 ECOS 매매기준율을 쓴다.

## 검증 상태

- 오류 경로(자격증명 누락·placeholder·잘못된 mode·네트워크 차단): 확인함
- preset 작업 테이블 구성(close 81 / premarket 71 / weekly 61, 이름 중복 없음): 확인함
- **실제 API 응답: 2026-09-04 기준일로 전량 성공(81/81, 71/71, 61/61)** — 해외·공매도·
  종목정보·ECOS 블록까지 포함해 실측 확인했다.
- 시세·수급·해외주식 계열은 demo(모의투자) 키로도 실전과 같은 실측값을 준다.
  demo 모드에서 거절되는 것은 환율 조회·주문가능금액 조회다. 그 외 미지원 API는
  `DemoUnsupportedError`("모의투자에서 지원하지 않는 API입니다")로 인증 실패와 구분된다.
  시세·수급 계열이 demo에서 실전과 동일한 값을 주는지는 첫 실행에서 확인이 필요하다.
  실계좌 정보를 쓰지 않는 시장 리포트이므로, demo로 충분하다면 실전 키는 필요 없다.

## 대안 — 네트워크를 열 수 없는 경우

로컬 PC(키움 MCP와 앱 키가 이미 설정돼 있음)에서 Windows 작업 스케줄러로 이 수집기를
17:5x에 돌려 결과 JSON을 Google Drive에 올리고, 18:05 예약작업은 Drive에서 읽는다.
클라우드에서 키움에 직접 붙지 않으므로 허용 목록이 필요 없고 앱 키도 로컬에 머문다.
대신 그 시각에 PC가 켜져 있어야 한다.
