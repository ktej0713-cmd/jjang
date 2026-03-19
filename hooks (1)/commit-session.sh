#!/usr/bin/env bash
# Hook: Stop
# 세션 종료 시 .claude 변경사항을 자동 커밋합니다.
# claude -p로 커밋 메시지를 생성하고, 실패 시 WIP 메시지를 사용합니다.

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
cd "$CLAUDE_DIR" || exit 0

# .git이 없으면 종료 (심볼릭 링크 환경 대응)
if [ ! -d ".git" ] && [ ! -f ".git" ]; then
  # symlink 대상에서 .git 확인
  REAL_DIR=$(readlink -f "$CLAUDE_DIR" 2>/dev/null || echo "$CLAUDE_DIR")
  cd "$REAL_DIR" || exit 0
  if [ ! -d ".git" ]; then
    exit 0
  fi
fi

# 세션 로그 기록
echo "[$(date +%Y-%m-%d_%H:%M)] session end" >> "$CLAUDE_DIR/session-log.txt" 2>/dev/null || true

# 모든 변경사항 스테이징
git add -A 2>/dev/null || true

# 커밋할 것이 없으면 종료
if git diff-index --quiet HEAD 2>/dev/null; then
  exit 0
fi

# diff 추출 (커밋 메시지 생성용, 2000줄 제한)
DIFF=$(git diff --cached 2>/dev/null | head -2000)

# claude -p로 커밋 메시지 생성
COMMIT_MSG=""
if command -v claude &>/dev/null; then
  COMMIT_MSG=$(echo "$DIFF" | claude -p \
    "git diff를 보고 커밋 메시지를 작성하세요.
규칙:
- 첫 줄: 'WIP(scope): 요약' (72자 이내, 한국어)
- scope는 변경 영역 (예: skills, hooks, output, agents, knowledge)
- 필요시 빈 줄 후 불릿으로 상세 내용
- 커밋 메시지만 출력, 다른 텍스트 금지" 2>/dev/null) || true
fi

# claude -p 실패 시 폴백
if [ -z "$COMMIT_MSG" ]; then
  FILE_COUNT=$(git diff --cached --name-only | wc -l | tr -d ' ')
  CHANGED_DIRS=$(git diff --cached --name-only | head -5 | xargs -I{} dirname {} | sort -u | head -3 | tr '\n' ',' | sed 's/,$//')
  COMMIT_MSG="WIP(auto): ${FILE_COUNT}개 파일 변경 [${CHANGED_DIRS}]"
fi

# 커밋
echo "$COMMIT_MSG" | git commit -F - --no-verify 2>/dev/null || true

# push (백그라운드)
git push origin main 2>/dev/null || true
