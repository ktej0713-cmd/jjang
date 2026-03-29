# 디자인 규칙

## 절대 금지
- 이모지 사용 금지 (어떤 상황에서도 사용하지 않는다)
- AI가 만든 티 나는 디자인 금지

## AI 디자인 티가 나는 요소 (사용 금지)
- 무의미한 아이콘/이모지 장식
- 색상 그라데이션 남발 (필요한 곳에만 최소한으로)
- 모든 요소에 둥근 모서리(border-radius) + 그림자(box-shadow) 일괄 적용
- 템플릿 느낌의 정형화된 3단/4단 카드 나열
- 과한 색상 대비와 불필요한 장식 요소
- 뻔한 히어로 섹션 + 아이콘 그리드 + CTA 버튼 조합

## 지향하는 디자인
- 실제 쇼핑몰에서 흔히 볼 수 있는 자연스러운 구성
- 정보 전달 중심, 장식 최소화
- 고도몰 에디터 호환성 우선 (테이블 레이아웃, 시스템 폰트)
- 경쟁 야구몰(야구야닷컴, 베이스볼파크 등)과 비슷한 수준의 실용적 디자인
- 고객이 보고 "쇼핑몰 이벤트 페이지"라고 느끼는 디자인

## 고도몰 + 스마트스토어 공용 HTML 규칙 (필수)

모든 상세페이지 HTML은 고도몰과 네이버 스마트스토어 양쪽에서 동작해야 한다.
스마트스토어가 더 엄격하므로 스마트스토어 기준을 충족하면 고도몰도 자동 충족된다.

### 절대 금지 (스마트스토어 에디터가 제거하거나 무력화)
- `<style>` 태그 사용 금지 — 모든 스타일은 `style=""` 인라인으로
- CSS 클래스(`class=""`) 사용 금지 — 인라인 스타일로 대체
- `<details>` / `<summary>` 태그 금지 — 항상 펼침 상태 Q/A `<div>`로 대체
- `::before` / `::after` 의사요소 금지 — `<span>` + HTML 엔티티로 대체
- `display:flex` / `display:grid` 금지 — `<table>` 레이아웃으로 대체
- `<ul>` / `<li>` 금지 — `<div>` + `<span>` 조합으로 대체
- `<script>` 태그 금지 — JS 의존 기능(아코디언 토글 등) 사용 불가
- `<html>` / `<head>` / `<body>` 태그 금지

### 허용 (양쪽 모두 정상 동작)
- `<link>` Google Fonts CDN — Noto Sans KR 로드용
- `<script type="application/ld+json">` — JSON-LD 구조화 데이터
- `<table>` 레이아웃 — 모든 그리드/카드 배치에 사용
- `linear-gradient` 인라인 스타일 — 히어로 배경 등
- `border-radius`, `box-shadow` 인라인 — 필요한 경우 허용
- HTML 엔티티 (`&#10003;`, `&#183;` 등) — 특수문자 표현에 사용

### 폰트
- `'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Google Fonts CDN으로 로드 (`<link>` 태그)

### FAQ 섹션 작성 방법
아코디언 불가 → 항상 펼침 상태로 작성:
```html
<div style="margin-bottom:8px; border:1px solid #DDDDDD;">
  <div style="padding:14px 16px; background:#F9F9F9; font-weight:700; color:#1B2A4A; font-size:14px;">
    <span style="color:#D4A843; font-weight:700; margin-right:4px;">Q.</span>질문 내용
  </div>
  <div style="padding:14px 16px; font-size:14px; color:#444444; line-height:1.8; background:#ffffff;">
    답변 내용
  </div>
</div>
```

### 파일명 규칙
- 공용 파일: `상세_{브랜드}_{상품명}_{날짜}_공용.html`
- `_고도몰.html` / `_스마트스토어.html` 구분 없이 단일 파일로 관리
