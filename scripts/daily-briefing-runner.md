# 일일 브리핑 수동 실행 가이드

## 수동 실행 방법

Claude Code 채팅창에서 아래 중 하나를 입력:

```
/daily-briefing
일일 브리핑 실행해줘
오늘 브리핑 보여줘
```

## 자동 실행

- 매일 오전 9:03에 자동 실행 (Claude Code가 열려 있는 경우)
- **주의**: 크론잡은 세션 전용 (Claude Code 종료 시 재등록 필요)

## 재등록 방법 (세션 시작 후)

Claude Code에서:
```
매일 아침 일일 브리핑 크론 다시 등록해줘
```

## 리포트 저장 위치

```
C:/Users/NO/.claude/output/daily-briefing/
├── 2026-03-20.md   ← 날짜별 리포트
├── 2026-03-21.md
└── latest.md       ← 최신 리포트 (항상 최신)
```

## 참여 에이전트

| 에이전트 | 역할 | 모델 |
|---------|------|------|
| DailyBriefingLead | 조율 및 통합 | sonnet |
| YouTubeResearcher | YouTube 신기능/팁 | sonnet |
| GitHubResearcher | GitHub 트렌딩/릴리즈 | sonnet |
| ClaudeCodeResearcher | Claude Code/API 업데이트 | sonnet |
