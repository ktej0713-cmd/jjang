#!/usr/bin/env bash
# Hook: SessionStart
# 최근 작업 맥락(output 폴더 변경, git 로그, 태스크 상태)을 세션 시작 시 로드합니다.

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
OUTPUT_DIR="$CLAUDE_DIR/output"
TASKS_DIR="$CLAUDE_DIR/tasks/jjang-md-team"

CONTEXT=""

# 1. 최근 output 파일 변경 (최근 7일 이내 생성/수정된 HTML)
if [ -d "$OUTPUT_DIR" ]; then
  RECENT_FILES=$(find "$OUTPUT_DIR" -name "*.html" -mtime -7 -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -5 | awk '{print $2}' || true)
  if [ -n "$RECENT_FILES" ]; then
    CONTEXT="최근 생성된 결과물:\n"
    while IFS= read -r f; do
      BASENAME=$(basename "$f")
      MTIME=$(date -r "$f" '+%m/%d %H:%M' 2>/dev/null || stat -c '%y' "$f" 2>/dev/null | cut -d' ' -f1)
      CONTEXT="${CONTEXT}- ${BASENAME} (${MTIME})\n"
    done <<< "$RECENT_FILES"
    CONTEXT="${CONTEXT}\n"
  fi
fi

# 2. 진행 중인 태스크
if [ -d "$TASKS_DIR" ]; then
  IN_PROGRESS=$(grep -rl 'status: in_progress\|status: review' "$TASKS_DIR" 2>/dev/null | head -5 || true)
  if [ -n "$IN_PROGRESS" ]; then
    CONTEXT="${CONTEXT}진행 중인 태스크:\n"
    while IFS= read -r f; do
      TASK_NAME=$(head -5 "$f" 2>/dev/null | grep -oP 'title:\s*\K.*' || basename "$f" .md)
      CONTEXT="${CONTEXT}- ${TASK_NAME}\n"
    done <<< "$IN_PROGRESS"
    CONTEXT="${CONTEXT}\n"
  fi
fi

# 3. .claude 저장소 최근 커밋
if [ -d "$CLAUDE_DIR/.git" ] || [ -f "$CLAUDE_DIR/.git" ]; then
  RECENT_COMMITS=$(cd "$CLAUDE_DIR" && git log --oneline -5 --format='%h %s' 2>/dev/null || true)
  if [ -n "$RECENT_COMMITS" ]; then
    CONTEXT="${CONTEXT}최근 설정 변경:\n${RECENT_COMMITS}\n"
  fi
fi

# JSON 출력
if [ -n "$CONTEXT" ]; then
  ESCAPED=$(echo -e "$CONTEXT" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' 2>/dev/null || echo "\"context loading failed\"")
  echo "{\"additionalContext\": $ESCAPED}"
fi
