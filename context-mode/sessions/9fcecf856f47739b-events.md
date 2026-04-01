# Session Resume

Events: 5 | Timestamp: 2026-04-01T05:29:20.957Z

## Project Rules

- C:\Users\jj1\.claude\CLAUDE.md
#### 사용자 프로필

##### 역할
- 짱베이스볼(jjangbaseball.com) 대표 겸 MD
- 야구용품 이커머스 운영 (고도몰5 + 네이버 스마트스토어)
- Claude Code로 상세페이지 제작, SEO, 프로모션, 개발 업무 수행

##### 커뮤니케이션 선호
- 언어: 모든 대화/코드 주석은 **한국어**로 진행
- 문체: 표와 불릿 적극 활용, 간결하고 명확하게
- 결과물: 바로 복사해서 사용 가능한 완성도
- 설명보다 실행 우선 — 코드 예시나 결과물을 먼저 보여줄 것

##### 작업 원칙 (모든 프로젝트 공통)
1. 보안 최우선 (SQL 인젝션, XSS 방지)
2. 코드 수정 시 한국어 주석 필수
3. 과장 광고 표현 절대 금지
4. "보통 쇼핑몰에서는" 같은 일반론 금지
5. 막연한 트렌드, 해외 사례만 나열, 실행 불가능한 아이디어 금지

##### 도메인 지식
- 야구 용어는 커뮤니티(엠엘비파크, 디시야갤)에서 실제 사용하는 표현 기준
- 가격 비교 대상: 오픈마켓(네이버/쿠팡/11번가/지마켓) 중심
- 야구야닷컴/베이스볼파크는 경쟁사가 아닌 참고 대상


- C:\Users\jj1\CLAUDE.md
#### 짱베이스볼 프로젝트

##### 기본 환경
- 플랫폼: 고도몰5 (PHP + Symfony 기반)
- OS: Windows 11
- 상세페이지: 고도몰 + 네이버 스마트스토어 공용 HTML (인라인 스타일, 860px 기준)

##### 프로젝트 구조 (지도)
```
.claude/
  jjang.md          — MD팀 운영 가이드라인 (통신 프로토콜, 에러 복구)
  agents/           — 커스텀 에이전트 (MD팀 6명 + 개발팀 4명)
  rules/            — 모듈형 규칙 5종
    brand-voice.md    — 브랜드 톤앤매너
    copywriting.md    — 카피라이팅 8단계 구조
    design-rules.md   — 디자인 금지/허용 규칙
    design-system.md  — 컬러/타이포/컴포넌트 표준
    security.md       — 보안 규칙
    seo-standards.md  — SEO 메타/구조화데이터 표준
  tasks/jjang-md-team/ — 태스크 추적 (backlog, 개별 태스크)
  knowledge/        — 지식 베이스 (시즌캘린더, 브랜드, 경쟁사, 캠페인이력)
  output/           — 생성 결과물 (상세페이지/기획전 HTML)
```

##### 에이전트 팀: jjang-md-team
```
Lead MD (opus) ─── 방향성 결정, 오케스트레이션
  ├─ 소싱 MD (sonnet) ─── 상품/브랜드, 가격전략
  ├─ 콘텐츠 MD (sonnet) ─── 상세페이지, 카피/설명
  ├─ 구조 MD (sonnet) ─── 카테고리, SEO/노출
  ├─ 프로모션 MD (sonnet) ─── 기획전, 배너/푸시
  └─ 고객검증 MD (opus) ─── 야구인 관점 PASS/FAIL
개발팀: PHP개발자(sonnet), 스킨디자이너(sonnet), 테스터(haiku), SEO전문가(sonnet)
```

##### 능력 경계선 (사용 가능한 도구)

###### 스킬 (슬래시 커맨드)
- `/상세페이지` — 상세페이지 HTML 자동 생성
- `/brand-design` — 브랜드 디자인 시스템 기반 HTML 생성
- `/godomall-seo` — 고도몰 SEO 필드(검색키워드, SEO태그, 네이버EP3.0) 자동 생성
- `/verify-html` — 상세페이지 HTML 고도몰/스마트스토어 호환성 검증
- `/품질체크` — 상세페이지 100점 채점
- `/price-check` — 오픈마켓 가격 비교표 생성
- `/nano-banana` — AI 이미지 생성 (Gemini Flash/Pro)
- `/기획전` — 기획전 HTML 생성 워크플로우
- `/seo`, `/seo-audit`, `/seo-page` — SEO 분석 도구

###### 외부 도구
- 고도몰5 관리자: 상품 등록/수정, SEO 필드 입력, 스킨 편집
- 네이버 스마트스토어: 상품 상세 HTML 입력 (인라인 스타일만 허용)
- 채널톡: 고객 문의 (https://8k27y.channel.io)
- Google Fonts CDN: Noto Sans KR 로드

###### 자동화
- Hooks: 코어 파일 보호(PreToolUse), PHP 문법 검사(PostToolUse), 컨텍스트 재주입(SessionStart/compact)
- Persistent Memory: 세션 간 학습 유지
- 태스크 추적: pending → assigned → in_progress → review → completed

##### 상세페이지 생산 프로토콜

###### 섹션 구조 (검증 완료된 패턴)

**필수 섹션 (모든 상품)**
```
SEC:히어로   — 상품 이미지 + 다크 배너(브랜드/상품명/1줄 정의)
SEC:상황     — "이런 상황에서 필요합니다" 2x2 table
SEC:스펙     — 제품 사양표 (좌 다크헤더 / 우 값)
SEC:체감     — 실사용 관점 3포인트 (스펙 나열 아님)
SEC:비교표   — 경쟁 제품 or 대안 방법 비교 table
SEC:FAQ      — 항상 펼침 Q&A (4~5개, 아코디언 금지)
SEC:전문가   — 다크 배경, 짱베이스볼 상담팀의 실전 팁
SEC:서머리   — 추천포인트 3개 + 채널톡 CTA 버튼 (마지막 섹션)
```

**선택 섹션 (카테고리별)**
```
SEC:추천대상 — 대상별 활용 (사회인/유소년/엘리트) → 글러브, 훈련장비
SEC:사이즈   — 사이즈 가이드 + 착용감 팁 → 글러브, 신발
SEC:구매가이드 — 구매 전 체크포인트 → 글러브 (고가 상품)
SEC:컬러     — 컬러 상세 설명 → 컬러 배리에이션 상품
```

**카테고리별 기본 조합**
| 카테고리 | 섹션 순서 |
|---------|----------|
| 글러브 | 히어로→상황→스펙→체감→추천대상→사이즈→비교표→FAQ→구매가이드→전문가→서머리 |
| 배트 | 히어로→상황→스펙→체감→추천대상→사이즈→비교표→FAQ→전문가→서머리 |
| 신발 | 히어로→상황→스펙→체감→추천대상→사이즈→비교표→FAQ→전문가→서머리 |
| 훈련장비 | 히어로→상황→스펙→체감→추천대상→비교표→FAQ→전문가→서머리 |
| 소품/소모품 | 히어로→상황→스펙→체감→비교표→FAQ→전문가→서머리 |
| 관리용품 | 히어로→상황→스펙→체감→비교표→FAQ→전문가→서머리 |

###### HTML 골격 규칙
- 최상위: `<div style="max-width:860px; margin:0 auto; font-family:'Noto Sans KR',...">`
- 섹션 배경색: 흰색(#ffffff) ↔ 회색(#F9F9F9) 교차, 전문가만 다크(#1B2A4A)
- 섹션 패딩: `padding: 48px~52px 28px~32px`
- 섹션 제목: `font-size:24px; font-weight:800; color:#1B2A4A; border-left:4px solid #D4A843; padding-left:14px`
- 카드 레이아웃: `<table>` 기반 (flex/grid 금지)
- 파일명: `상세_{브랜드}_{상품명}_{YYYYMMDD}_공용.html`
- 저장 위치: `~/.claude/output/`
- 참고 템플릿: `~/.claude/output/상세_녹스_로진백65g_20260331_공용.html` (최신 검증 완료)

###### 서머리 SEC 마무리 표준 코드
```html
<div style="text-align: center;">
  <a href="https://8k27y.channel.io" style="display: inline-block; background: #D4A843; color: #1B2A4A; font-size: 15px; font-weight: 600; padding: 12px 32px; text-decoration: none;" target="_blank">채널톡 문의하기</a>
</div>
```

##### 시행착오 일지

###### 상세페이지 제작 시 주의사항
1. **배송/교환 섹션 넣지 않는다** — 고도몰 자체 배송 안내가 별도 존재하므로 상세페이지에 중복 불필요. SEC:서머리를 마지막으로 마무리할 것.
2. **가격 하드코딩 금지** — 서머리 추천포인트에 구체적 금액/할인 정보 넣지 않는다. 가격은 수시 변동되므로 고도몰 상품 관리에서 별도 관리.
3. **킵 레더 늘어남 표현 금지** — "길들이면 딱 맞게 늘어납니다" 같은 표현 사용 불가. 킵 레더는 쉽게 늘어나지 않음. "포켓이 형성된다", "손에 적응한다"로 대체.
4. **채널톡 CTA 버튼 표준**: 골드 배경(#D4A843), 다크 텍스트(#1B2A4A), `<a href="https://8k27y.channel.io" target="_blank">채널톡 문의하기</a>` — 텍스트 안내가 아닌 클릭 가능한 버튼으로.

###### 기술적 주의사항
5. **고도몰 코어 파일 직접 수정 금지** — module/ 내 이벤트 리스너/서비스 오버라이드로 확장
6. **스마트스토어 HTML 제약** — `<style>`, `class`, `<details>`, flex/grid, `<ul>/<li>`, `<script>` 전면 금지. 인라인 스타일 + `<table>` 레이아웃만 사용.



## Last User Prompt

오늘 왜 재고체크 스케줄이 안돌았어?
