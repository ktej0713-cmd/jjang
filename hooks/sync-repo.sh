#!/usr/bin/env bash
# SessionStart 훅: .claude 레포 자동 동기화
# - master → main 브랜치 자동 마이그레이션
# - 원격 변경사항 pull
# 어느 PC에서 실행해도 자동으로 main 브랜치로 통일됨

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
cd "$CLAUDE_DIR" || exit 0

# git 레포가 아니면 종료
if [ ! -d ".git" ]; then
  exit 0
fi

CURRENT=$(git branch --show-current 2>/dev/null || true)

# 로컬이 master인 경우 → main으로 자동 전환
if [ "$CURRENT" = "master" ]; then
  # 커밋되지 않은 변경사항 임시 저장
  STASHED=false
  if ! git diff-index --quiet HEAD 2>/dev/null; then
    git stash push -m "auto-migration-to-main" 2>/dev/null || true
    STASHED=true
  fi

  # master → main 이름 변경
  git branch -m master main 2>/dev/null || true

  # 원격 main 추적 설정
  git fetch origin 2>/dev/null || true
  git branch -u origin/main main 2>/dev/null || true

  # 원격 master 브랜치 삭제 (있으면)
  git push origin --delete master 2>/dev/null || true

  # stash 복원
  if [ "$STASHED" = true ]; then
    git stash pop 2>/dev/null || true
  fi

  CURRENT="main"
fi

# main 브랜치에서 pull
if [ "$CURRENT" = "main" ]; then
  git pull origin main 2>/dev/null | grep -v 'Already up to date' || true
fi
