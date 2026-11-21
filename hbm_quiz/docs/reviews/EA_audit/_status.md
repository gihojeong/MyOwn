# EA 감사 진행 상황

갱신: 2026-11-21 (EA 2차 세션)

| 분야 | 상태 | 판정 | 파일 |
|---|---|---|---|
| BUMP | 완료(1차 세션) | 합격(수정 후) | BUMP.md |
| FA | 완료(1차 세션) | 합격(수정 8+3) | FA.md |
| THERM | 완료 | 조건부 — refresh 판정 die(base→core) 정정, A-9004 정답 재검 | THERM.md |
| SAW | 완료 | 합격(경미 4) | SAW.md |
| PROD | 완료 | 합격(경미 5) | PROD.md |
| MET | 완료 | 합격(수정 4) | MET.md |
| FEOL | 완료 | 합격(수정 2) — A-9013 기하 조건 정정 | FEOL.md |
| SIP | 완료 | 조건부 — A-9034 전류 가정 2자릿수 과대, 고급 3 하향 | SIP.md |
| DRAM | 완료 | 합격(수정 3) | DRAM.md |
| WARP | 완료 | 합격(수정 3) — I-0247 그림 Tg 불일치 | WARP.md |
| BSP | 완료 | 합격(경미 2) — 고급 수량 보강 불필요 | BSP.md |
| TSV | 완료 | 합격(경미 1 + XD) — A-9044 정답 논리 정상 | TSV.md |
| MIX | 완료 | 합격(XD 1) — 고급 57 % 수용 | MIX.md |
| COW | 완료 | 합격(경미 3) | COW.md |

## W3 XD 점검 항목 (감사 중 발견)
1. HCB 입자 Poisson 예산 4분야 중복: SAW-A-9004 · MET-A-9007 · MIX-A-9015 · COW-A-9001 → 보유 COW-A-9001 + MIX-A-9015, SAW·MET 는 고유 판단으로 변경 또는 삭제.
2. TSV KOZ 모델 중복: TSV-A-9029 ↔ FEOL-A-9001, TSV-A-9041 ↔ FEOL-A-0028 → TSV 보유.
3. MIX 보유 판정 일반론 군(MIX-A-0051·0052·0100, 상대 DRAM-A-0074, PROD-A-0023·0036·0037·0053, FEOL-A-0015)이 양쪽 모두 삭제됨 → '판단 태도' 일반론이라 의도된 손실로 판정(손실 확인 완료).
4. FEOL-I-0001·A-0001(reveal 선택비 → tip height 산포 → non-wet + short)을 "BSP 이관 A-0003 근중복" 으로 삭제 → BSP 에 해당 개념 문항이 실제로 있는지 확인.
5. refresh/온도 구간 판정 die 통일: THERM(A-0003·A-9004)·DRAM(A-9044)이 base die 또는 불명확 → "최하단 core die" 기준으로 통일(셀 없는 base die 로 판정 금지). STANDARDS 2.5 에 한 줄 추가 후보.

## 검사기(validate.py) 변경 — 이번 세션
1. `f_stack` + `hideResult` 이면 `h_um` 을 K1 수치 비교에서 제외(생략·값 모두 무관, 높이 칸은 "?"). → **SIP 는 "?" 칸 우회로 넣은 h_um 을 원복해도 됨.**
2. 스키마 키 추가(DA 2026-11-21, LAYOUT_RULES §4·§7): `f_sip.msg`, `f_warp.hideNames/hideResult`, `f_bs.notes`, `f_saw.notes`, `f_bump.hideLabels/hideResult`, `f_rel.tcCycles`.
3. `f_hcb` opt-in: `off_nm`/`tol_nm`/`dish_nm` 이 없으면 "기본값" 불일치로 보지 않음. `E_FIG_HIDE_RESULT`(f_hcb)는 `tol_nm` 이 있을 때만(판정 표시가 그때만 그려짐).
4. 신규 `W_FIG_NAME_LEAK`: 정답이 Smile/Cry 인데 f_warp 에 hideNames 없음, 정답이 Kirkendall 인데 f_bump(kirkendall) 에 hideLabels 없음. 현재 전체 1건(MET-B-9014).
- 갱신 후 전체: E 0 / W 1(MET-B-9014) / I 1762.
- `W_FIG_UNKNOWN_KEY` 를 vx 로 면제한 문항: **COW-A-9039**(f_warp.hideNames) 1건 — 이제 키가 스키마에 있으므로 vx 제거 지시.
- 관찰(미반영, Phase 2 일괄 후보): k=0 그림의 flag 가 "조건: …" 인 문항 62건(PROD 34, WARP 14, COW 7, DRAM 5, TSV 1, BSP 1) — 기준서 3.6 은 k=0 flag "주제: …". 검사기 W 로 넣으면 진행 중 게이트에 영향이 있어 Phase 2 기계 수정(또는 k=1 전환 판정)으로 처리 제안.
