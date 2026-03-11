# 짱베이스볼 (jjangbaseball.com) 프로젝트

## 기본 환경
- 플랫폼: 고도몰5 (PHP + Symfony 기반)
- OS: Windows 11
- 언어: 모든 대화/코드 주석은 **한국어**로 진행

## 프로젝트 구조
- `.claude/jjang.md` — MD팀 운영 가이드라인 (통신 프로토콜, 에러 복구 포함)
- `.claude/agents/` — 커스텀 에이전트 (MD팀 6명 + 개발팀 4명)
- `.claude/rules/` — 모듈형 규칙 (brand-voice, copywriting, security, seo-standards)
- `.claude/tasks/jjang-md-team/` — 태스크 추적 (backlog, 개별 태스크 파일)
- `.claude/knowledge/` — 지식 베이스 (시즌캘린더, 브랜드, 경쟁사, 캠페인이력)
- `.claude/output/` — 생성 결과물 (기획전 HTML 등)

## 작업 규칙
1. 결과물은 `~/.claude/output/{프로젝트명}/` 폴더에 HTML로 생성
2. 코드 수정 시 한국어 주석 필수
3. 고도몰 코어 파일은 직접 수정하지 않고, 모듈 방식으로 기능 추가
4. 보안 최우선 (SQL 인젝션, XSS 방지)
5. 에이전트 팀 작업 시 `jjang.md`의 MD팀 가이드라인을 따름

## 에이전트 팀: jjang-md-team
- 팀명: `jjang-md-team`
- 역할: 짱베이스볼 MD + 개발 운영 전담팀

### 조직 구조 (계층형)
```
┌─────────────────────────────────────────┐
│              Lead MD (팀장)              │
│    방향성 결정 · 우선순위 · 오케스트레이션    │
├─────────┬──────────┬──────────┬─────────┤
│ 소싱 MD │콘텐츠 MD │ 구조 MD  │프로모션MD│
│상품/브랜드│상세페이지 │카테고리  │기획전   │
│가격전략  │카피/설명 │SEO/노출  │배너/푸시 │
├─────────┴──────────┴──────────┴─────────┤
│           고객검증 MD (최종 게이트)         │
│     야구인 관점 검증 · PASS/FAIL 판정      │
├─────────────────────────────────────────┤
│              개발팀 (실행)                │
│  PHP개발자 · 스킨디자이너 · 테스터 · SEO전문가│
└─────────────────────────────────────────┘
```

### 모델 라우팅
- **opus**: Lead MD (전략 판단), 고객검증 MD (최종 게이트)
- **sonnet**: 소싱/콘텐츠/구조/프로모션 MD, PHP개발자, 스킨디자이너, SEO전문가
- **haiku**: 테스터 (체크리스트 검증, 빠른 처리)

### 협업 흐름
1. **기획**: Lead MD (방향 결정) → 소싱/콘텐츠/구조/프로모션 MD (병렬 작업) → 고객검증 MD (최종 검증)
2. **실행**: PHP개발자/스킨디자이너 (구현) → 테스터 (검증) → SEO전문가 (최적화)
3. **보고**: 각 MD → Lead MD에게 결과 보고, Lead MD가 통합 출력

### 강화 기능
- **Persistent Memory**: 전 에이전트 `memory: project` — 세션 간 학습
- **Hooks**: 코어 파일 보호(PreToolUse), PHP 문법 검사(PostToolUse), 컨텍스트 재주입(SessionStart/compact)
- **Rules**: `.claude/rules/` — brand-voice, copywriting, security, seo-standards
- **통신 프로토콜**: `jjang.md`에 정의 — 요청 형식, 의존성, 충돌 해결
- **태스크 추적**: `.claude/tasks/jjang-md-team/` — pending→assigned→in_progress→review→completed
- **지식 베이스**: `.claude/knowledge/` — seasonal-calendar, brand-catalog, competitor-tracking, campaign-history
- **에러 복구**: Level 1(자체)→Level 2(Lead MD)→Level 3(사용자)→Fallback(이월)

## 금지 사항
- 막연한 트렌드, 해외 사례만 나열, 실행 불가능한 아이디어
- "보통 쇼핑몰에서는" 같은 일반론
- 과장 광고 표현
