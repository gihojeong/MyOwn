# MyOwn — 키움 REST API KOSPI MCP 서버

Claude 데스크탑 앱에서 **키움증권 REST API**로 코스피 지수와 국내 종목 시세를
직접 조회하기 위한 MCP(Model Context Protocol) 서버입니다.

- 의존성 없음 — 파이썬 3.9+ 표준 라이브러리만 사용 (`pip install` 불필요)
- 실행 파일 하나로 등록 — `kospi_mcp_server.py`
- 조회 전용 — 주문 계열 경로(`/api/dostk/ordr`, `/crdordr`)는 서버가 차단

```
Claude 데스크탑 앱  ──stdio(JSON-RPC)──▶  kospi_mcp_server.py  ──HTTPS──▶  api.kiwoom.com
```

---

## 1. 준비: 키움 앱키 발급

1. [키움 REST API 포털](https://openapi.kiwoom.com/)에 로그인
2. **API 사용신청**에서 신청 → **앱키(App Key)** 와 **시크릿키(Secret Key)** 발급
3. 모의투자로 먼저 시험하려면 모의투자 신청도 함께 (`KIWOOM_ENV=mock`)

## 2. 설치 (한 줄)

저장소를 받은 뒤, 등록 명령을 실행합니다.

```bash
git clone https://github.com/gihojeong/MyOwn.git
cd MyOwn
python3 kospi_mcp_server.py install
```

앱키와 시크릿키를 물어본 뒤 Claude 데스크탑 설정 파일에 서버를 등록합니다
(기존 설정은 병합하고 `.bak` 백업을 남깁니다). 시크릿키는 입력 중 화면에
표시되지 않습니다.

| OS | 설정 파일 |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

모의투자 서버로 붙이려면 `--env mock`, 값을 미리 넘기려면
`--app-key ... --app-secret ...` 을 씁니다.

등록 후 **Claude 데스크탑 앱을 완전히 종료했다가 다시 실행**하세요.

### 수동 등록

`install`을 쓰지 않고 직접 적어도 됩니다 (`examples/claude_desktop_config.json` 참고):

```json
{
  "mcpServers": {
    "kiwoom-kospi": {
      "command": "/usr/bin/python3",
      "args": ["/절대경로/MyOwn/kospi_mcp_server.py"],
      "env": {
        "KIWOOM_APP_KEY": "발급받은-앱키",
        "KIWOOM_APP_SECRET": "발급받은-시크릿키",
        "KIWOOM_ENV": "real"
      }
    }
  }
}
```

> `command`는 **절대경로**로 적으세요. 데스크탑 앱은 셸 PATH를 상속하지 않는
> 경우가 많아 `python3`만 적으면 실행에 실패합니다.
> macOS/Linux는 `which python3`, Windows는 `where python` 으로 확인합니다.

## 3. 연결 확인

앱을 열기 전에 터미널에서 먼저 검증하는 편이 빠릅니다.

```bash
export KIWOOM_APP_KEY=...  KIWOOM_APP_SECRET=...  KIWOOM_ENV=real

python3 kospi_mcp_server.py check          # 토큰 발급 성공 여부
python3 kospi_mcp_server.py kospi          # 코스피 현재가
python3 kospi_mcp_server.py stock 005930   # 삼성전자 현재가
python3 kospi_mcp_server.py search 삼성전자 # 종목코드 검색
python3 kospi_mcp_server.py tools          # 도구 목록
```

Claude 앱에서는 이렇게 물으면 됩니다.

> 지금 코스피 지수 알려줘
> 삼성전자 현재가랑 PER 알려줘
> 코스피 최근 10일 추이 보여줘

## 4. 제공 도구

| 도구 | TR | 설명 |
|---|---|---|
| `get_kospi_index` | `ka20001` | 코스피/코스닥/코스피200 등 지수 현재가 |
| `get_index_daily` | `ka20009` | 지수 일별 추이 |
| `list_index_codes` | — | 지수 이름·업종코드 목록 (네트워크 호출 없음) |
| `search_stock` | `ka10099` | 종목명·코드 검색 (1시간 캐시) |
| `get_stock_price` | `ka10001` | 종목 현재가, PER/PBR/시가총액 |
| `get_stock_quote` | `ka10004` | 호가 잔량 |
| `get_stock_daily_chart` | `ka10081` | 일봉 |
| `get_top_volume` | `ka10030` | 당일 거래량 상위 |
| `check_connection` | — | 토큰 발급으로 자격증명 점검 |
| `kiwoom_raw` | 임의 | 문서에 있는 조회 TR을 그대로 호출 |

지수 지정자는 `kospi`, `kosdaq`, `kospi200`, `코스피`, `코스닥` 같은 별칭이나
3자리 업종코드(`001`, `101`, `201` …)를 그대로 받습니다.

## 5. 환경변수

| 변수 | 기본값 | 설명 |
|---|---|---|
| `KIWOOM_APP_KEY` | (필수) | 앱키 |
| `KIWOOM_APP_SECRET` | (필수) | 시크릿키 |
| `KIWOOM_ENV` | `real` | `real` = api.kiwoom.com, `mock` = mockapi.kiwoom.com |
| `KIWOOM_BASE_URL` | — | 베이스 URL 직접 지정 (시험용) |
| `KIWOOM_INDEX_SCALE` | `auto` | 지수 배율. `auto` / `100` / `1` |
| `KIWOOM_TOKEN_CACHE` | `~/.kospi-mcp/token.json` | 토큰 캐시 경로. `none`이면 캐시 안 함 |
| `KIWOOM_CA_BUNDLE` | — | 사내 프록시용 CA 번들 경로 |

## 6. 동작 방식

- **토큰**: `POST /oauth2/token` (`grant_type=client_credentials`, `appkey`, `secretkey`)
  으로 발급하고 만료 60초 전에 선제 재발급합니다. 401을 받으면 한 번 재발급 후
  재시도합니다. 토큰은 홈 디렉터리에 `0600` 권한으로 캐싱됩니다.
- **TR 호출**: `POST <리소스경로>` + 헤더 `authorization: Bearer …`, `api-id`,
  `cont-yn`, `next-key`. 응답 본문의 `return_code`가 0이 아니면 오류로 처리합니다.
- **호출 간격**: 같은 TR은 최소 1초 간격을 지키고, 429/5xx는 지수 백오프로 재시도합니다.

### 지수 배율 주의

키움은 지수를 소수점 없는 정수로 주는 경우가 있습니다(`252050` = `2520.50`).
기본값 `auto`는 **원본에 소수점이 없을 때만** 100으로 나눕니다. 표시값이
100배 또는 1/100배로 어긋나면 `KIWOOM_INDEX_SCALE`을 `1` 또는 `100`으로
고정하세요. 모든 도구는 요약과 함께 **원본 JSON을 그대로 첨부**하므로 실제
필드명과 값을 눈으로 확인할 수 있습니다.

## 7. 테스트

네트워크 없이 도는 단위 테스트입니다 (가짜 전송 계층 사용).

```bash
python3 -m unittest discover -s tests -t .
```

## 8. 문제 해결

| 증상 | 확인 |
|---|---|
| 앱에 도구가 안 보임 | 앱 완전 종료 후 재실행. `command`가 절대경로인지 확인 |
| `토큰 발급 실패` | 앱키/시크릿키, `KIWOOM_ENV`(실전 키로 mock 서버에 붙으면 실패) |
| `return_code=...` 오류 | 해당 TR 사용 권한과 요청 필드명을 키움 문서에서 확인 |
| 지수값이 이상함 | `KIWOOM_INDEX_SCALE`을 `1` 또는 `100`으로 고정 |
| 서버가 죽음 | 로그는 stderr로 나갑니다. 터미널에서 직접 실행해 확인 |

## 9. 보안

- 앱키·시크릿키는 저장소에 커밋하지 마세요. `.env`와 `token.json`은 `.gitignore`에 있습니다.
- 설정 파일에는 키가 평문으로 들어가므로 `install`이 `0600`으로 권한을 조입니다.
- 이 서버는 **조회 전용**입니다. 주문 TR은 `kiwoom_raw`에서도 차단됩니다.

## 라이선스

MIT
