# 짱베이스볼 디자인 시스템

## 브랜드 컬러

### 프라이머리 팔레트
| 토큰 | HEX | 용도 |
|------|-----|------|
| `--primary` | `#1B2A4A` | 헤더, 주요 텍스트, CTA 배경 |
| `--primary-light` | `#2C3E6B` | 호버 상태, 서브 배경 |
| `--primary-dark` | `#0F1A30` | 강조, 푸터 배경 |
| `--accent` | `#D4A843` | 강조선, 가격, 배지, 포인트 |
| `--accent-light` | `#E8C876` | 호버 상태, 배경 틴트 |
| `--accent-dark` | `#B8922E` | 다크모드 대비 |

### 시맨틱 컬러
| 토큰 | HEX | 용도 |
|------|-----|------|
| `--success` | `#2E7D32` | 재고 있음, 할인, 긍정 |
| `--warning` | `#E65100` | 품절 임박, 주의 |
| `--danger` | `#C62828` | 품절, 에러, 삭제 |
| `--info` | `#1565C0` | 안내, 링크, 정보 |
| `--new` | `#E53935` | 신상품 뱃지, NEW 태그 |

### 그레이 스케일
| 토큰 | HEX | 용도 |
|------|-----|------|
| `--gray-900` | `#222222` | 본문 텍스트 |
| `--gray-700` | `#555555` | 서브 텍스트 |
| `--gray-500` | `#888888` | 비활성, 플레이스홀더 |
| `--gray-300` | `#CCCCCC` | 구분선, 비활성 보더 |
| `--gray-100` | `#F5F5F5` | 섹션 배경, 카드 배경 |
| `--gray-50` | `#FAFAFA` | 페이지 배경 |
| `--white` | `#FFFFFF` | 카드, 콘텐츠 영역 |

### 배경색
| 토큰 | HEX | 용도 |
|------|-----|------|
| `--bg-page` | `#F9F9F9` | 전체 페이지 배경 |
| `--bg-section` | `#F5F5F5` | 교차 섹션 배경 |
| `--bg-card` | `#FFFFFF` | 카드, 상품 영역 |
| `--bg-hero` | `linear-gradient(135deg, #1B2A4A 0%, #2C3E6B 100%)` | 히어로 섹션 |
| `--bg-accent-tint` | `#FDF8EC` | 강조 배경 (골드 틴트) |

---

## CSS 변수 표준 선언

모든 HTML 결과물에 아래 :root 변수를 포함한다:

```css
:root {
  /* 프라이머리 */
  --primary: #1B2A4A;
  --primary-light: #2C3E6B;
  --primary-dark: #0F1A30;
  --accent: #D4A843;
  --accent-light: #E8C876;
  --accent-dark: #B8922E;

  /* 시맨틱 */
  --success: #2E7D32;
  --warning: #E65100;
  --danger: #C62828;
  --info: #1565C0;
  --new: #E53935;

  /* 그레이 */
  --gray-900: #222222;
  --gray-700: #555555;
  --gray-500: #888888;
  --gray-300: #CCCCCC;
  --gray-100: #F5F5F5;
  --gray-50: #FAFAFA;

  /* 배경 */
  --bg-page: #F9F9F9;
  --bg-section: #F5F5F5;
  --bg-card: #FFFFFF;

  /* 타이포그래피 */
  --font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-size-xs: 12px;
  --font-size-sm: 13px;
  --font-size-base: 15px;
  --font-size-md: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 22px;
  --font-size-2xl: 28px;
  --font-size-3xl: 36px;

  /* 간격 */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 40px;
  --space-3xl: 60px;

  /* 라운딩 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 50%;

  /* 그림자 */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
  --shadow-md: 0 2px 8px rgba(0,0,0,0.1);
  --shadow-lg: 0 4px 16px rgba(0,0,0,0.12);
  --shadow-hover: 0 8px 24px rgba(0,0,0,0.15);

  /* 트랜지션 */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;

  /* 최대 너비 */
  --max-width: 1200px;
  --content-width: 860px;  /* 네이버 스마트스토어 호환 */
}
```

---

## 타이포그래피

### 폰트 패밀리
- 기본: `Noto Sans KR` (Google Fonts CDN, 한글 최적화)
- 로드: `<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">`
- 폴백: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- 가격/숫자 강조: `'Noto Sans KR'` 동일 (별도 숫자 폰트 불필요)

### 스마트스토어/고도몰 인라인 스타일 기준값
CSS 변수는 고도몰 스킨에서만 사용. 상세페이지/기획전 HTML은 반드시 인라인 스타일:
- `font-family: 'Noto Sans KR', -apple-system, sans-serif`
- primary: `#1B2A4A` / accent: `#D4A843`
- 본문: `font-size:15px; color:#222222; line-height:1.7`
- 섹션 제목: `font-size:22px; font-weight:700; color:#1B2A4A; border-left:4px solid #D4A843; padding-left:12px`

### 폰트 크기 스케일
| 용도 | 크기 | 굵기 | 행간 |
|------|------|------|------|
| 히어로 타이틀 | 36px (3xl) | 800 | 1.3 |
| 섹션 타이틀 | 28px (2xl) | 700 | 1.3 |
| 상품명/소제목 | 22px (xl) | 700 | 1.4 |
| 카드 타이틀 | 18px (lg) | 600 | 1.4 |
| 본문 강조 | 16px (md) | 600 | 1.6 |
| 본문 | 15px (base) | 400 | 1.7 |
| 서브 텍스트 | 13px (sm) | 400 | 1.5 |
| 캡션/뱃지 | 12px (xs) | 500~700 | 1.3 |

### 제목 스타일 표준
- 섹션 제목 좌측에 `border-left: 4px solid var(--accent)` + `padding-left: 16px`
- 섹션 제목 아래 설명은 `var(--gray-700)` + `font-size: var(--font-size-base)`

---

## 간격 시스템

### 섹션 간격
| 영역 | 값 |
|------|-----|
| 섹션 상하 패딩 | `40px 20px` (데스크톱), `32px 16px` (모바일) |
| 섹션 간 간격 | `0` (교차 배경색으로 구분) |
| 카드 내부 패딩 | `24px` (데스크톱), `16px` (모바일) |
| 카드 간 간격 | `16px` (그리드 gap) |

### 컴포넌트 간격
| 요소 | 마진/패딩 |
|------|----------|
| 제목 → 본문 | margin-bottom: 8px |
| 제목 → 서브텍스트 | margin-bottom: 16px |
| 문단 → 문단 | margin-bottom: 16px |
| 버튼 패딩 | 12px 24px (기본), 16px 32px (대형) |
| 배지 패딩 | 4px 12px |
| 입력 필드 패딩 | 12px 16px |

---

## 컴포넌트 표준

### 버튼
| 타입 | 배경 | 텍스트 | 보더 | 용도 |
|------|------|--------|------|------|
| Primary | `--primary` | white | none | 구매, CTA |
| Accent | `--accent` | `--primary-dark` | none | 장바구니, 강조 |
| Outline | transparent | `--primary` | 1px solid --primary | 보조 액션 |
| Ghost | transparent | `--gray-700` | none | 텍스트 링크형 |
| Danger | `--danger` | white | none | 삭제, 경고 |

### 카드
- 배경: `var(--bg-card)`
- 보더: `1px solid var(--gray-100)` (또는 보더 없이 그림자)
- 라운딩: `var(--radius-md)` (8px)
- 그림자: `var(--shadow-sm)`
- 호버: `var(--shadow-hover)` + `transform: translateY(-4px)`
- 트랜지션: `var(--transition-base)`

### 배지/태그
| 타입 | 배경 | 텍스트 | 용도 |
|------|------|--------|------|
| NEW | `--new` | white | 신상품 |
| BEST | `--accent` | `--primary-dark` | 베스트셀러 |
| SALE | `--success` | white | 할인 |
| 품절 | `--gray-300` | `--gray-700` | 품절 상품 |
| 카테고리 | `--bg-accent-tint` | `--accent-dark` | 카테고리 라벨 |

### 표 (테이블)
- 헤더 배경: `var(--primary)`, 텍스트: white
- 행 배경: 교차 `var(--bg-card)` / `var(--gray-50)`
- 보더: `1px solid var(--gray-100)`
- 셀 패딩: `12px 16px`
- 폰트: `var(--font-size-sm)` ~ `var(--font-size-base)`

### 아코디언
- 헤더 배경: `var(--gray-50)`
- 보더: `1px solid var(--gray-100)`
- 라운딩: `var(--radius-md)`
- 아이콘: `+` / `-` 토글 (우측 정렬)
- 콘텐츠 패딩: `20px`

---

## 레이아웃

### 그리드 시스템
| 디바이스 | 컬럼 | 거터 | 최대 너비 |
|---------|------|------|----------|
| 데스크톱 (1200px+) | 4열 | 16px | 1200px |
| 태블릿 (768~1199px) | 2열 | 16px | 100% |
| 모바일 (~767px) | 1열 | 12px | 100% |

### 상품 그리드
| 디바이스 | 상품 열 | 상품 카드 너비 |
|---------|--------|--------------|
| 데스크톱 | 4열 | ~280px |
| 태블릿 | 3열 | ~240px |
| 모바일 | 2열 | ~48% |

### 네이버 스마트스토어 호환
- 상세페이지 콘텐츠 최대 너비: `860px`
- 이미지 최대 너비: `860px` (2x 기준 `1720px` 원본 권장)
- 좌우 패딩: `20px` (모바일 안전 영역)

---

## 반응형 브레이크포인트

```css
/* 모바일 우선 (Mobile First) */
/* 기본: ~767px (모바일) */

@media (min-width: 768px) {
  /* 태블릿 */
}

@media (min-width: 1024px) {
  /* 소형 데스크톱 */
}

@media (min-width: 1200px) {
  /* 대형 데스크톱 */
}
```

---

## 아이콘

### 사용 원칙
- 외부 아이콘 라이브러리 미사용 (CDN 의존성 최소화)
- CSS/SVG 인라인 또는 유니코드 이모지 활용
- 자주 쓰는 아이콘:

| 용도 | 표현 |
|------|------|
| 체크/완료 | ✓ 또는 ✅ |
| 경고 | ⚠️ |
| 별점 | ★ ☆ |
| 화살표 | ← → ↑ ↓ |
| 배송 | 📦 |
| 전화 | 📞 |
| 카트 | 🛒 |

---

## 이미지

### 상세페이지 이미지 규격
| 용도 | 사이즈 | 비고 |
|------|--------|------|
| 대표 이미지 | 860 x 860px | 정사각형, 흰 배경 |
| 상세 컷 | 860 x auto | 가로 860 고정, 세로 자유 |
| 플레이스홀더 | 860 x 500px | 회색 배경 + 텍스트 |
| 썸네일 | 300 x 300px | 리스트/검색 결과 |

### 배너 이미지 규격
| 위치 | 사이즈 (PC) | 사이즈 (모바일) |
|------|------------|----------------|
| 메인 배너 | 1920 x 600px | 720 x 480px |
| 카테고리 배너 | 1200 x 300px | 720 x 300px |
| 기획전 배너 | 1200 x 400px | 720 x 400px |
| 팝업 배너 | 500 x 600px | 360 x 480px |
| 띠 배너 | 1920 x 80px | 720 x 60px |

### 이미지 텍스트 안전 영역
- 배너 좌우 20% 영역은 핵심 텍스트 배치 금지 (모바일 크롭 대비)
- 텍스트는 중앙 60% 영역에 집중

---

## 고도몰 스킨 적용 규칙

### 스타일 우선순위
1. `:root` CSS 변수로 전역 정의
2. 고도몰 기본 스타일 오버라이드 시 `!important` 최소 사용
3. 선택자 특수성(specificity)으로 우선순위 확보
4. 섹션별 고유 ID 기반 스코핑 (예: `#sec02 .product-card`)

### 파일 구조
```
/skin/
  /css/
    jjang-variables.css    ← :root 변수 (이 파일을 최상단에 로드)
    jjang-components.css   ← 공통 컴포넌트
    jjang-layout.css       ← 레이아웃/그리드
    jjang-pages.css        ← 페이지별 스타일
  /js/
    jjang-common.js        ← 공통 스크립트
```

### 금지 사항
- 고도몰 템플릿 태그 `{변수명}` 훼손 금지
- 인라인 스타일 남용 금지 (CSS 변수 사용)
- 하드코딩 색상값 금지 (반드시 `var(--토큰)` 사용)
- `*` 와일드카드 선택자 금지

---

## 업데이트 이력
- 2026-03-05: 초기 디자인 시스템 작성 (컬러, 타이포, 간격, 컴포넌트, 레이아웃, 이미지 규격)
