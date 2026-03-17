#!/bin/bash
# 짱베이스볼 Google Drive 동기화 상태 체크
# SessionStart hook에서 자동 실행

GDRIVE="$HOME/내 드라이브/claude/짱베이스볼"
CLAUDE_DIR="$HOME/.claude"
ERRORS=0

# Google Drive 접근 가능 확인
if [ ! -d "$GDRIVE" ]; then
  echo "⚠️  Google Drive 연결 안 됨! 오프라인 모드로 작동합니다."
  exit 0
fi

# 주요 폴더 심링크 체크
for dir in agents rules knowledge output tasks scripts plans; do
  if [ ! -d "$CLAUDE_DIR/$dir" ]; then
    echo "⚠️  $dir 폴더 누락"
    ERRORS=$((ERRORS + 1))
  fi
done

# 주요 파일 체크
for file in jjang.md settings.json session-log.txt; do
  if [ ! -f "$CLAUDE_DIR/$file" ]; then
    echo "⚠️  $file 파일 누락"
    ERRORS=$((ERRORS + 1))
  fi
done

if [ ! -f "$HOME/CLAUDE.md" ]; then
  echo "⚠️  CLAUDE.md 파일 누락"
  ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -eq 0 ]; then
  echo "✅ Google Drive 동기화 정상 ($(ls $GDRIVE/agents/ | wc -l) agents, $(ls $GDRIVE/rules/ | wc -l) rules, $(ls $GDRIVE/knowledge/ | wc -l) knowledge)"
else
  echo "⚠️  ${ERRORS}개 항목 동기화 이상 — setup-work-pc.ps1 재실행 필요"
fi
