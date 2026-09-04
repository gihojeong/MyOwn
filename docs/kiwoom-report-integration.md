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

1. **네트워크 허용** — 환경의 네트워크 정책에 `api.kiwoom.com`, `mockapi.kiwoom.com` 추가.
   실시간 시세 WebSocket까지 쓰려면 `:10000` 포트도 함께.
2. **자격증명 주입** — 예약작업이 뜨는 컨테이너에는 로컬 PC의 `.claude.json`이 없다.
   환경 변수로 `APP_KEY`, `APP_SECRET`, `KIWOOM_MODE`를 설정해야 한다.

환경 설정은 https://code.claude.com/docs/en/claude-code-on-the-web 참조.

## 수집기

`scripts/kiwoom_collect.py` — 표준 라이브러리만 쓴다. 예약작업 컨테이너는 매번
새로 뜨므로 `uv sync`(약 140MB)나 MCP 기동 없이 즉시 실행되어야 한다.
`urllib`은 `https_proxy`와 `SSL_CERT_FILE`을 자동으로 따르므로 프록시 환경에서
추가 설정이 필요 없다.

```bash
# 자격증명·도달성 점검 (토큰 발급까지만)
python3 scripts/kiwoom_collect.py --check

# 마감 리포트용 묶음
python3 scripts/kiwoom_collect.py --preset close --out data/kiwoom_$(date +%Y%m%d).json

# 임의 API 단건 (스펙 확인·디버깅)
python3 scripts/kiwoom_collect.py --call ka20001 --path /api/dostk/sect \
    --body '{"mrkt_tp":"0","inds_cd":"001"}'
```

자격증명은 환경변수로만 받는다. 인자로 받으면 프로세스 목록과 셸 히스토리에 남는다.

개별 호출이 실패해도 전체를 중단하지 않고 결과 JSON에 `error`로 남긴다. 리포트에서
"확인 불가"가 **데이터 부재**를 뜻하는지 **수집 실패**를 뜻하는지 구분하기 위해서다.

## 리포트 항목 ↔ API 매핑

`--preset close`에 이미 들어간 것 (요청 파라미터를 스펙으로 확인함):

| 리포트 항목 | API | 비고 |
| --- | --- | --- |
| [A] KOSPI/KOSDAQ/K200 종가·시가·고저·등락률·거래대금·상승하락 종목수 | `ka20001` 업종현재가 | `inds_cur_prc_tm`에 시간별 지수가 함께 와서 **장중 궤적**도 한 번에 |
| [B] 외국인·기관계·투신·연기금·보험·은행·기타법인 순매수 | `ka10063` 장중투자자별매매 | 투자자별로 따로 호출해야 세부주체가 분리됨 |
| [B] 3주체 항등식 검산 원자료 | `ka10066` 장마감후투자자별매매 | 종목 단위 행. `etc_corp`(기타법인)가 응답에 직접 있어 **잔차 역산이 불필요** |

파라미터 확인 후 추가할 것:

| 리포트 항목 | API |
| --- | --- |
| [A-2] 시간외 단일가 등락 상하위 | `ka10098` 시간외단일가등락율순위, `ka10087` 시간외단일가 |
| [B] 프로그램 매매 차익/비차익 | `ka90010` 일자별, `ka90005` 시간대별 |
| [B] 외국인·기관 순매수 상위 10 | `ka90009` 외국인기관매매상위 |
| [B] 최근 5거래일 외국인 누적 | `ka10131` 기관외국인연속매매현황 |
| [C] 업종별 유출입 | `ka10051` 업종별투자자순매수, `ka20003` 전업종지수 |
| [D] 개별종목 종가·등락률 | `ka10081` 주식일봉차트 |
| [D-2] 시총 상위 30 분해 | `ka10032` 거래대금상위, `ka10027` 전일대비등락률상위 |

## 검증 상태

- 오류 경로(자격증명 누락·placeholder·잘못된 mode·네트워크 차단): 확인함
- preset 작업 테이블 구성(11건): 확인함
- **실제 API 응답: 미검증** — 네트워크가 열리기 전까지 호출 자체가 불가능하다.
  허용 후 `--check` → `--preset close` 순으로 한 번 돌려 응답 필드를 대조해야 한다.
- demo(모의투자) 모드는 환율 조회·주문가능금액 조회가 거절된다. 그 외 미지원 API는
  `DemoUnsupportedError`("모의투자에서 지원하지 않는 API입니다")로 인증 실패와 구분된다.
  시세·수급 계열이 demo에서 실전과 동일한 값을 주는지는 첫 실행에서 확인이 필요하다.

## 대안 — 네트워크를 열 수 없는 경우

로컬 PC(키움 MCP와 앱 키가 이미 설정돼 있음)에서 Windows 작업 스케줄러로 이 수집기를
17:5x에 돌려 결과 JSON을 Google Drive에 올리고, 18:05 예약작업은 Drive에서 읽는다.
클라우드에서 키움에 직접 붙지 않으므로 허용 목록이 필요 없고 앱 키도 로컬에 머문다.
대신 그 시각에 PC가 켜져 있어야 한다.
