---
name: brand-design
description: 짱베이스볼 브랜드 디자인 시스템 기반으로 상세페이지, 기획전, 배너, 카드뉴스 HTML을 생성합니다. Use when user says "디자인 만들어줘", "배너 만들어줘", "기획전 HTML", "카드뉴스", "브랜드 디자인", or asks to create any visual HTML content for 짱베이스볼.
triggers:
  - "브랜드 디자인"
  - "배너 만들어줘"
  - "카드뉴스 만들어줘"
  - "기획전 디자인"
  - "/brand-design"
---

# 짱베이스볼 브랜드 디자인 스킬

이 스킬은 짱베이스볼 브랜드 디자인 시스템을 기반으로 HTML 결과물을 생성합니다.

## 브랜드 컬러 시스템 (인라인 스타일 기준값)

```
Primary (네이비):
  #1B2A4A — 헤더, 주요 텍스트, CTA 배경
  #2C3E6B — 호버, 서브 배경
  #0F1A30 — 강조, 푸터

Accent (골드):
  #D4A843 — 강조선, 가격, 배지, 포인트
  #E8C876 — 호버, 배경 틴트
  #B8922E — 다크 대비
  #FDF8EC — 골드 틴트 배경

Semantic:
  #2E7D32 — 재고있음/할인 (success)
  #E65100 — 품절임박/주의 (warning)
  #C62828 — 품절/에러 (danger)
  #E53935 — NEW 뱃지 (new)

Gray:
  #222222 — 본문 텍스트
  #555555 — 서브 텍스트
  #888888 — 비활성
  #CCCCCC — 구분선
  #F5F5F5 — 섹션 배경
  #F9F9F9 — 페이지 배경
  #FFFFFF — 카드 배경
```

## 폰트 (필수)

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```
- `font-family: 'Noto Sans KR', -apple-system, sans-serif`

## HTML 하드룰 (스마트스토어 + 고도몰 공용)

### 절대 금지
- `<style>` 태그 금지 → 모든 스타일은 `style=""` 인라인
- `class=""` 금지 → 인라인 스타일로 대체
- `display:flex` / `display:grid` 금지 → `<table>` 레이아웃으로
- `<ul>` / `<li>` 금지 → `<div>` + `<span>` 조합
- `<details>` / `<summary>` 금지 → 항상 펼침 상태 `<div>` FAQ
- `::before` / `::after` 금지 → `<span>` + HTML 엔티티
- `<script>` 금지
- `<html>` / `<head>` / `<body>` 금지
- 이모지 금지

### 허용
- `<link>` Google Fonts CDN
- `<script type="application/ld+json">` JSON-LD 구조화 데이터
- `<table>` 레이아웃
- `linear-gradient` 인라인
- `border-radius`, `box-shadow` 인라인
- HTML 엔티티 (`&#10003;` 등)

## 타이포그래피 스케일 (인라인)

| 용도 | 인라인 스타일 |
|------|--------------|
| 히어로 타이틀 | `font-size:36px; font-weight:800; line-height:1.3` |
| 섹션 타이틀 | `font-size:28px; font-weight:700; line-height:1.3` |
| 상품명/소제목 | `font-size:22px; font-weight:700; line-height:1.4` |
| 카드 타이틀 | `font-size:18px; font-weight:600; line-height:1.4` |
| 본문 강조 | `font-size:16px; font-weight:600; line-height:1.6` |
| 본문 | `font-size:15px; font-weight:400; line-height:1.7; color:#222222` |
| 서브 텍스트 | `font-size:13px; font-weight:400; line-height:1.5; color:#555555` |
| 캡션/뱃지 | `font-size:12px; font-weight:700; line-height:1.3` |

## 섹션 제목 표준

```html
<div style="margin:40px 0 20px; border-left:4px solid #D4A843; padding-left:12px;">
  <div style="font-size:22px; font-weight:700; color:#1B2A4A; font-family:'Noto Sans KR',sans-serif;">섹션 제목</div>
  <div style="font-size:14px; color:#555555; margin-top:4px;">서브 설명</div>
</div>
```

## 히어로 섹션 표준

```html
<div style="background:linear-gradient(135deg,#1B2A4A 0%,#2C3E6B 100%); padding:60px 20px; text-align:center; font-family:'Noto Sans KR',sans-serif;">
  <div style="font-size:36px; font-weight:800; color:#ffffff; line-height:1.3;">메인 타이틀</div>
  <div style="font-size:16px; color:#D4A843; margin-top:12px;">서브 카피</div>
</div>
```

## 스펙 표 표준

```html
<table style="width:100%; border-collapse:collapse; font-family:'Noto Sans KR',sans-serif; font-size:14px;">
  <tr>
    <td style="background:#1B2A4A; color:#ffffff; font-weight:700; padding:12px 16px; width:30%;">항목</td>
    <td style="padding:12px 16px; background:#ffffff; border-bottom:1px solid #F5F5F5;">내용</td>
  </tr>
  <!-- 짝수 행: background:#F9F9F9 -->
</table>
```

## FAQ 섹션 표준 (항상 펼침 - 아코디언 금지)

```html
<div style="margin-bottom:8px; border:1px solid #DDDDDD;">
  <div style="padding:14px 16px; background:#F9F9F9; font-weight:700; color:#1B2A4A; font-size:14px; font-family:'Noto Sans KR',sans-serif;">
    <span style="color:#D4A843; font-weight:700; margin-right:4px;">Q.</span>질문
  </div>
  <div style="padding:14px 16px; font-size:14px; color:#444444; line-height:1.8; background:#ffffff; font-family:'Noto Sans KR',sans-serif;">
    답변
  </div>
</div>
```

## 배지/태그 표준

```html
<!-- NEW 뱃지 -->
<span style="background:#E53935; color:#ffffff; font-size:11px; font-weight:700; padding:3px 8px;">NEW</span>

<!-- BEST 뱃지 -->
<span style="background:#D4A843; color:#0F1A30; font-size:11px; font-weight:700; padding:3px 8px;">BEST</span>

<!-- 카테고리 라벨 -->
<span style="background:#FDF8EC; color:#B8922E; font-size:12px; font-weight:600; padding:4px 10px; border:1px solid #E8C876;">카테고리</span>
```

## 이미지 플레이스홀더 표준

```html
<div style="width:100%; max-width:860px; background:#F5F5F5; text-align:center; padding:80px 20px; color:#888888; font-size:14px; font-family:'Noto Sans KR',sans-serif;">
  [이미지: 상품명 - 860x860px]
</div>
```

## 레이아웃 그리드 (table 기반)

### 2컬럼
```html
<table style="width:100%; border-collapse:collapse;">
  <tr>
    <td style="width:50%; padding:8px; vertical-align:top;">[왼쪽]</td>
    <td style="width:50%; padding:8px; vertical-align:top;">[오른쪽]</td>
  </tr>
</table>
```

### 3컬럼
```html
<table style="width:100%; border-collapse:collapse;">
  <tr>
    <td style="width:33.3%; padding:8px; vertical-align:top;">[1]</td>
    <td style="width:33.3%; padding:8px; vertical-align:top;">[2]</td>
    <td style="width:33.3%; padding:8px; vertical-align:top;">[3]</td>
  </tr>
</table>
```

## 콘텐츠 최대 너비

- 상세페이지: `max-width:860px; margin:0 auto`
- 기획전/배너: `max-width:1200px; margin:0 auto`

## 디자인 타입별 워크플로우

### 상세페이지
1. 10단계 표준 구조 적용 (히어로+1줄정의 > 필요상황 > 스펙표 > 체감설명 > 포지션별추천 > 사이즈가이드 > 비교표 > FAQ > 추천포인트 > 배송없음)
2. 가격 하드코딩 금지 (플랫폼 관리)
3. 배송/교환/반품 섹션 제외
4. 파일명: `상세_{브랜드}_{상품명}_{날짜}_공용.html`

### 기획전
1. 히어로 배너 (네이비 그라디언트 + 골드 포인트)
2. 상품 그리드 (4열 table)
3. CTA 버튼 (`background:#1B2A4A; color:#ffffff`)
4. 파일명: `기획전_{주제}_{날짜}.html`

### 배너
- PC: 1920×600px 기준 / 모바일: 720×480px
- 핵심 텍스트 중앙 60% 영역에 배치
- 좌우 20%는 텍스트 금지 (모바일 크롭 대비)

### 카드뉴스
- 1:1 비율 (860×860px)
- 상단 브랜드 컬러 띠 + 하단 로고 영역

## 출력 규칙

1. 결과물은 `C:/Users/NO/.claude/output/` 에 HTML 파일로 저장
2. 저장 후 파일 경로 안내
3. 이모지 절대 사용 금지
4. 야구 용어는 커뮤니티 실사용 표현 적용
5. 과장 광고 표현 금지

## 검증 체크리스트

생성 후 반드시 확인:
- [ ] `<style>` 태그 없음
- [ ] `class=""` 없음
- [ ] `display:flex` / `display:grid` 없음
- [ ] `<ul>/<li>` 없음
- [ ] `<details>/<summary>` 없음
- [ ] Noto Sans KR CDN `<link>` 포함
- [ ] 가격 하드코딩 없음
- [ ] 이모지 없음
- [ ] max-width:860px 적용 (상세페이지)
