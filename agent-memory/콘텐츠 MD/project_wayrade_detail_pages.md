---
name: WAYRADE 배트 상세페이지 작업 이력
description: WAYRADE 브랜드 야구배트 상세페이지 HTML 작업 이력, 표준 구조, 반복 패턴
type: project
---

WAYRADE 배트 상세페이지는 동일한 CSS 스코핑(#jjang-detail)과 섹션 구조를 따른다.

**Why:** 기존 CREEPY 상세페이지 구조를 템플릿으로 확립하여 이후 모델 작업 시 일관성 유지

**How to apply:** 새 WAYRADE 배트 상세페이지 요청 시 아래 표준 구조와 파일 패턴을 따른다

## 작업된 파일 목록
| 모델 | 파일 경로 | 작업일 |
|------|----------|--------|
| WAYRADE CREEPY 풀알로이 | C:\Users\jj1\.claude\output\상세페이지\상세_WAYRADE_CREEPY_풀알로이배트_20260312_고도몰.html | 2026-03-12 |
| WAYRADE 26 Scandium FIREAX | C:\Users\jj1\.claude\output\상세페이지\상세_WAYRADE_스칸듐FIREAX_풀알로이배트_20260312_고도몰.html | 2026-03-12 |

## 확립된 표준 구조 (9섹션)
1. 히어로 (이미지 + 카피 + 한줄 정의)
2. 이런 분께 맞습니다 (공감 유도, jd-bg-gray)
3. 핵심 스펙 표
4. 소재/구조 설명 (선택 — 스칸듐처럼 특수 소재일 때 추가, jd-bg-gray)
5. 실제로 잡아보면 이렇습니다 (체감 설명)
6. 타자 유형별 적합도 (3x2 그리드, jd-bg-gray)
7. 사이즈 선택 가이드
8. 비교표 (vs 경쟁/동급 배트, jd-bg-gray)
9. FAQ (details/summary 태그)
10. 이런 분께 추천합니다 (추천 포인트, jd-bg-gray)
- 배송/교환/반품 섹션 없음 (마지막은 추천 포인트로 끝남)

## 기술 규칙 (반복 적용)
- CSS 스코핑: #jjang-detail
- max-width: 860px
- CSS content 속성: 유니코드 이스케이프 사용 (\2713 등), HTML 엔티티 금지
- JavaScript 완전 금지 — FAQ는 details/summary 태그
- 폰트: 'Noto Sans KR', -apple-system 폴백
- 컬러: #1B2A4A (primary), #D4A843 (accent)
- JSON-LD: Product + FAQPage 스키마 동시 포함
- 이모지 사용 금지

## 이미지 경로 패턴
- 베이스 URL: https://chj1013.hgodo.com/data/image/CLAUDE/
- CREEPY: WAYRADE_CREEPY_detail.jpg
- 스칸듐 FIREAX: WAYRADE_SCANDIUM_FIREAX_detail.jpg
