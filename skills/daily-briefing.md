---
name: daily-briefing
description: 유튜브, 깃허브, 클로드코드의 유용한 기능/업데이트를 조사하여 일일 브리핑 리포트를 생성한다. 매일 아침 자동 실행되거나 수동으로 `/daily-briefing` 으로 호출할 수 있다.
triggers:
  - "일일 브리핑"
  - "오늘 브리핑"
  - "daily briefing"
  - "유튜브 깃허브 클로드 조사"
  - "아침 브리핑"
---

# 일일 기술 브리핑 스킬

당신은 DailyBriefingLead 에이전트를 실행하여 오늘의 기술 브리핑을 생성합니다.

## 실행 순서

1. 오늘 날짜 확인 (YYYY-MM-DD 형식)
2. 출력 디렉토리 확인: `C:/Users/NO/.claude/output/daily-briefing/`
3. 이미 오늘 리포트가 있으면 바로 출력 (`YYYY-MM-DD.md` 파일 확인)
4. 없으면 3개 리서처 에이전트를 **병렬로** 실행:
   - YouTubeResearcher
   - GitHubResearcher
   - ClaudeCodeResearcher
5. 결과를 통합하여 마크다운 리포트 생성
6. `C:/Users/NO/.claude/output/daily-briefing/YYYY-MM-DD.md` 에 저장
7. `latest.md` 도 같은 내용으로 업데이트

## 리포트 구조

```markdown
# 일일 기술 브리핑 — YYYY-MM-DD

## YouTube
...

## GitHub
...

## Claude Code
...

---
생성: YYYY-MM-DD HH:MM | 다음 브리핑: 내일 오전 9시
```

## 병렬 실행 방법

세 에이전트를 단일 메시지에서 동시에 실행하여 처리 시간을 최소화한다.
각 에이전트 결과를 받으면 즉시 통합 작업을 시작한다.

## 출력

- 파일 저장 완료 메시지
- 리포트 핵심 요약 (각 플랫폼당 Top 3 항목)
- 저장 경로 안내
