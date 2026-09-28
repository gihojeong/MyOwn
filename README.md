# MyOwn

KOSPI 리포트 3회차(개장 전·마감·주간)를 위한 **읽기 전용 시세 수집 저장소**다.
주문은 하지 않는다.

## 빠른 시작

```
python3 scripts/setup_check.py                                   # 키·경로 4곳 진단
python3 scripts/kiwoom_collect.py --preset close --out data/close.json
```

자격증명은 환경변수로만 받는다(`APP_KEY` `APP_SECRET` `KRX_AUTH_KEY` `ECOS_API_KEY`
`KIWOOM_MODE`). **값을 파일·커밋·프롬프트에 쓰지 마라.**

## 문서

| 문서 | 내용 |
| --- | --- |
| [`docs/setup.md`](docs/setup.md) | **세팅·키 발급·검증.** 키를 처음 붙이거나 갈아끼울 때 |
| [`docs/collection-contract.md`](docs/collection-contract.md) | 세 회차 공통 수집 계약 — 절차·소스·실패 유형 5종 |
| [`docs/kiwoom-report-playbook.md`](docs/kiwoom-report-playbook.md) | 응답 필드와 해석 규칙 |
| [`docs/kiwoom-report-integration.md`](docs/kiwoom-report-integration.md) | 리포트 생성 연계 |
| [`docs/trigger-prompts/`](docs/trigger-prompts) | 회차별 예약작업 프롬프트 |

## 스크립트

| 경로 | 역할 |
| --- | --- |
| `scripts/setup_check.py` | 키움·KRX·ECOS·환경변수 네 경로 일괄 진단 |
| `scripts/kiwoom_collect.py` | 수집기 정본. 표준 라이브러리만 쓴다 |
| `scripts/close-report/` | 마감 리포트 계산·검증·빌드 |
| `scripts/forecast_audit.py` | 예측 계보 감사 |

## 데이터 출처

- **키움 REST** — 지수·종목 시세, 투자자별 수급, 프로그램 매매, 해외 ETF 15종
- **KRX OpenAPI** — KOSPI200 선물·옵션, 전종목 확정 종가·시가총액(**종가의 정본**)
- **ECOS** — 원/달러, 국고채 3·10·30년, CD 91일, 회사채 AA− 3년
