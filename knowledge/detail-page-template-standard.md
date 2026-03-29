# 상세페이지 HTML 표준 템플릿 (2026-03-29 확정)

> 윌슨 A2000 CLASSIC 1786 상세페이지를 기준으로 확정된 표준.
> 모든 상세페이지는 이 형식을 따른다.
> 개선안 반영: 시맨틱 태그 인라인 스타일 필수, 모바일 테이블 스크롤, SEO alt, Google Fonts, 전문가 출처 구체화

---

## 0. 스마트스토어 호환성 체크리스트 (최우선)

모든 HTML은 스마트스토어 기준 충족 시 고도몰도 자동 충족된다.

### 절대 금지
- `<style>` 태그, `class` 속성
- `display:flex`, `display:grid` → `<table>` 레이아웃으로 대체
- `<details>/<summary>` → 항상 펼침 상태 div
- `<ul>/<li>` → div+span 조합
- `<script>` (JSON-LD 포함) → 고도몰 관리자에서 별도 입력
- `::before`/`::after` 의사요소
- `<html>/<head>/<body>` 태그

### 허용 (양쪽 모두 정상)
- `<link>` Google Fonts CDN
- `<h1>/<h2>/<h3>/<p>/<strong>/<a>` (반드시 인라인 style 지정)
- `<table>/<thead>/<tbody>/<tr>/<th>/<td>`
- `<img>` (max-width:100% 필수)
- `<div>/<span>`
- `display: inline-block`, `display: block`
- `linear-gradient` 인라인
- `border-radius`, `box-shadow` 인라인
- `overflow-x: auto` (모바일 테이블 스크롤)

### 시맨틱 태그 인라인 스타일 필수
h1/h2/h3/p 태그는 스마트스토어에서 허용되지만, 브라우저 기본 스타일이 적용되므로 **반드시 인라인 style을 지정**해야 의도한 디자인대로 렌더링된다.
```html
<!-- 올바른 예 -->
<h2 style="font-size: 24px; font-weight: 800; margin: 0 0 4px 0;">제목</h2>
<!-- 잘못된 예 (브라우저 기본 마진/크기 적용됨) -->
<h2>제목</h2>
```

---

## 1. 전체 구조 규칙

### 최상단 필수 요소
```html
<!-- JSON-LD 스키마는 고도몰 관리자에서 별도 입력 (스마트스토어는 script 태그 전면 차단) -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```
- Google Fonts `<link>`를 항상 포함 (상세페이지 단독으로도 폰트 렌더링 보장)

### 시맨틱 HTML 필수
- `<h1>`: 상품명 (히어로 내, 페이지당 1개)
- `<h2>`: 섹션 제목
- `<h3>`: 서브 제목 (체감 설명, FAQ 질문 등)
- `<p>`: 본문 텍스트
- `<strong>`: 강조
- `<div>`만으로 구성하지 않는다. AI 크롤러가 h 태그 계층으로 콘텐츠 중요도를 판단한다.
- **모든 시맨틱 태그에 인라인 style 필수** (margin, font-size, color 등)

### SEC 마커 체계
```html
<!-- [SEC:이름] -->
  내용
<!-- [/SEC:이름] -->
```
- 번호(SEC01, SEC02) 대신 이름 기반 사용
- 열기 + 닫기 태그 쌍으로 작성
- 수정 시 섹션을 이름으로 찾기 쉬움

### JSON-LD
- 본문에 포함하지 않는다
- 고도몰 관리자에서 별도 입력 (스마트스토어는 script 태그 전면 차단)
- 최상단에 주석으로 안내

### 래퍼
```html
<div style="max-width: 860px; margin: 0 auto; font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Malgun Gothic', 'Dotum', sans-serif; color: #1a1a1a; line-height: 1.7; font-size: 16px;">
```
- 기본 폰트 크기: 16px
- 최대 너비: 860px
- 폴백 폰트에 맑은고딕, 돋움 포함

---

## 2. 섹션별 표준 구조 (11개)

### SEC:히어로
- 상품 이미지 (max-width: 860px, display: block)
  - **alt 텍스트에 SEO 키워드 포함** (예: "윌슨 A2000 1786 내야 글러브 11.5인치")
  - "상세 1", "상세 2" 같은 일반적 alt 금지
- 브랜드 컬러 배너 (브랜드별 공식 컬러 적용)
  - 브랜드 태그 (12px, letter-spacing: 1.5px)
  - `<h1>` 상품명 (36px, font-weight: 800)
  - 핵심 카피 1줄 + 주요 스펙 나열
- 한줄 소개 박스 (border-top: 3px solid accent)
  - 상품 포지셔닝을 1~2문장으로 요약

### SEC:상황
- `<h2>` 제목 + `<p>` 부제목
- ▸ 기호로 4개 항목 나열
- 각 항목: border-bottom 구분, 16px, 좌측 패딩 24px

### SEC:스펙
- `<h2>` 제목 + `<p>` 부제목
- 테이블: `<thead>/<tbody>` 구분 필수 (모든 테이블에 통일)
- th(브랜드 컬러 배경) + td(교차 배경 #f8f8f8)
- th width: 28%, font-size: 14px
- td font-size: 15px, font-weight: 500

### SEC:체감
- `<h2>` 제목 + `<p>` 부제목 (스펙만으로는 알 수 없는...)
- 3개 카드: border: 1px solid #f2f2f2, padding: 24px
- 각 카드: `<h3>` 19px + `<p>` 16px
- **디자인 옵션**: 기본은 흰 카드, 브랜드 특성에 따라 다크 배경 + 영문 태그 변형 허용
  - 예: 프리미엄 브랜드 → 다크 테마 카드, 엔트리 브랜드 → 밝은 카드

### SEC:추천대상
- `<h2>` 포지션별 적합도
- border-left: 3px solid accent 카드
- `<strong>` 포지션 -- 적합도 + `<span>` 설명

### SEC:사이즈
- `<h2>` 제목 + `<p>` 부제목
- 테이블: 현재 상품 행 강조 (배경색 + 2px border)
- 하단 사이즈 선택 팁 박스 (border-left: 4px solid primary)

### SEC:비교표
- `<h2>` 제목 + `<p>` 부제목
- 현재 상품 열 헤더: accent 컬러 배경, 강조 표시
- `<thead>/<tbody>` 구분
- **모바일 가로 스크롤 래퍼 필수**:
  ```html
  <div style="overflow-x: auto; -webkit-overflow-scrolling: touch;">
    <table style="min-width: 600px;">...</table>
  </div>
  ```

### SEC:FAQ
- `<h2>` 제목 + `<p>` 부제목
- `<h3>` Q. 질문 (17px, 배경 #f8f8f8)
- `<p>` 답변 (16px, line-height: 1.75)
- 4~5개 항목

### SEC:구매가이드
- `<h2>` 제목 + `<p>` 부제목
- 넘버링 (accent 배경 28x28px 원형)
- `<strong>` 가이드 제목 + `<p>` 설명
- 3개 항목 (포지션→사이즈, 웹타입, 가죽등급)

### SEC:전문가
- 배경: #f8f8f8, border-left: 4px solid primary
- "전문가 한마디 (EXPERT TIP)" 라벨
- 인용문 스타일 (15px, line-height: 1.8)
- 출처: "-- 짱베이스볼 글러브 상담팀 | 날짜 기준" (구체적 팀명 사용)

### SEC:서머리
- 브랜드 컬러 배경 + 핵심 카피
- 키워드 태그 (inline-block, border: 1px solid rgba 스타일)
- 추천 포인트 3개 (border-left: 3px solid accent)
- CTA: 채널톡 문의 버튼
  ```html
  <a href="https://8k27y.channel.io" style="display: inline-block; background: {primary}; color: #ffffff; font-size: 15px; font-weight: 600; padding: 12px 32px; text-decoration: none;" target="_blank">채널톡 문의하기</a>
  ```

---

## 3. 섹션 제목 패턴 (통일)

```html
<h2 style="font-size: 24px; font-weight: 800; color: {primary}; letter-spacing: -0.01em; margin: 0 0 4px 0; line-height: 1.25; padding: 0 0 0 14px; text-align: left; border-left: 4px solid {accent};">섹션 제목</h2>
<p style="color: #5a5a5a; font-size: 16px; margin: 0 0 28px 0; padding: 0 0 0 18px; text-align: left;">부제목/설명</p>
```
- 모든 섹션에 제목 + 부제목 쌍으로 작성
- 좌측 accent 바 4px
- 제목: 24px, 800 weight
- 부제목: 16px, #5a5a5a

---

## 4. 폰트 크기 표준

| 용도 | 크기 | 굵기 |
|------|------|------|
| 히어로 타이틀 (h1) | 36px | 800 |
| 섹션 제목 (h2) | 24px | 800 |
| 서브 제목 (h3) | 19px | 700 |
| 포지션/추천 제목 | 17px | 700 |
| 본문 (p) | 16px | 400 |
| 부제목 | 16px | 400 |
| 스펙 테이블 td | 15px | 500 |
| 스펙 테이블 th | 14px | 600 |
| 브랜드 태그 | 12px | 700 |
| 출처/캡션 | 14px | 400 |

---

## 5. 컬러 적용 규칙

- `{primary}`: 브랜드 메인 컬러 → 섹션 제목, 테이블 헤더, CTA, 서머리 배경
- `{accent}`: 브랜드 포인트 컬러 → 좌측 바, 강조 행, 태그
- 본문 텍스트: #1a1a1a (래퍼 기본)
- 서브 텍스트: #5a5a5a
- 배경 교차: #ffffff / #f8f8f8
- 구분선: #f2f2f2

### 브랜드별 컬러 매핑
| 브랜드 | primary | accent |
|--------|---------|--------|
| 짱베이스볼 (기획전/이벤트) | #1B2A4A | #D4A843 |
| 윌슨 (Wilson) | #002D72 | #E31837 |
| 유니 (Yooni) | #1A1A1A | #C8956C |
| 미즈노 (Mizuno) | - | - |
| SSK | - | - |

---

## 6. 섹션 간격

- 각 섹션 padding: 48px 28px
- 섹션 구분: border-bottom: 1px solid #f2f2f2 (배경색 교차 #fff/#f9f9f9도 허용)
- 카드 간격: margin-bottom: 10~12px
- 제목→부제목: margin: 0 0 4px 0
- 부제목→콘텐츠: margin: 0 0 28px 0

---

## 7. 이미지 규칙

### alt 텍스트 표준
- 형식: `{브랜드} {모델명} {포지션} {핵심키워드}`
- 예: `유니 YN0 외야 글러브 13인치 세토스티어`
- 금지: "상세 1", "이미지", "사진", "IMG_001" 등 의미 없는 alt

### 이미지 스타일
```html
<img alt="SEO 키워드 포함 설명" src="URL" style="width: 100%; max-width: 860px; display: block; margin: 0 auto;">
```

---

## 8. 구매가이드 카테고리별 변형

구매가이드 섹션은 상품 카테고리에 따라 내용을 변경한다:
- **글러브**: 포지션→사이즈, 웹타입, 가죽등급
- **배트**: 소재(나무/알루미늄/복합), 길이-무게 비율, 그립감
- **보호장비**: 포지션별 필수장비, 사이즈 측정법, 인증 규격
- **의류/신발**: 사이즈차트, 소재 특성, 시즌별 선택
