# 세팅 점검 실행 기록 (2026-09-28 KST)

점검 전용 세션에서 실행한 두 명령의 출력 전문이다. 키 값은 어디에도 적지 않으며,
환경변수는 `setup_check.py`가 원래 출력하는 대로 **길이(자수)만** 남긴다.

## 1. `env | grep -c '^APP_'`

```
2
```

`APP_KEY`, `APP_SECRET` 두 개가 셸 환경에 실려 있다는 뜻이다. 개수만 세므로 값은 노출되지 않는다.

## 2. `python3 scripts/setup_check.py --skip-krx`

종료 코드 `0`. KRX 구간은 `--skip-krx`로 건너뛰었으므로 아래 출력에 `== KRX OpenAPI ==` 절이 없다.

```
== 환경변수 ==
[OK]   APP_KEY: 설정됨 (43자)
[OK]   APP_SECRET: 설정됨 (43자)
[OK]   KIWOOM_MODE: 설정됨 (4자)
[OK]   KRX_AUTH_KEY: 설정됨 (40자), 비가시 문자 1개 포함(수집기가 자동 제거)
[WARN] ECOS_API_KEY: 미설정

== 키움 REST ==
[OK]   demo 토큰(https://mockapi.kiwoom.com): 발급 성공
[WARN] real 토큰(https://api.kiwoom.com): 투자구분 불일치 — 이 키는 다른 쪽 전용
[OK]   지수 조회(ka20001, demo): KOSPI cur_prc=6889.74

== ECOS ==
[WARN] 인증: 키 없음 — 공개 sample 키로 폴백(1회 10행 제한)
[OK]   원/달러 매매기준율(fx_usdkrw): 20260928 1352

== 판정 ==
[OK] 필수 수집 경로 전부 정상 — 회차를 돌릴 수 있다.
[WARN] 선택 항목 3건 — 없어도 돌지만 그만큼 항목이 빠진다.
  · 환경변수 / ECOS_API_KEY: 미설정
  · 키움 REST / real 토큰(https://api.kiwoom.com): 투자구분 불일치 — 이 키는 다른 쪽 전용
  · ECOS / 인증: 키 없음 — 공개 sample 키로 폴백(1회 10행 제한)

조치 방법은 docs/setup.md, 실패 유형 분류는 docs/collection-contract.md 6절.
```

## 읽는 법

- `KRX_AUTH_KEY`의 비가시 문자 1개는 `_clean_secret()`이 읽는 즉시 제거하므로 실패 원인이 아니다.
- 키움 키는 **모의(demo) 전용**이다. `real` 쪽 WARN은 return_code 8030(투자구분 불일치)이며, 키 오류가 아니다.
- `ECOS_API_KEY` 미설정은 공개 `sample` 키 폴백으로 동작하되 1회 10행 제한이 걸린다.
- KRX 5개 서비스의 이용신청 상태는 이 기록으로 알 수 없다. `--skip-krx` 없이 다시 돌려야 확인된다.
