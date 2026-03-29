#!/bin/bash
# .claude 폴더 Git 자동 동기화 스크립트
# 사용: git-sync.sh pull | push

CLAUDE_DIR="C:/Users/NO/.claude"
ACTION="${1:-pull}"

cd "$CLAUDE_DIR" || exit 1

# git 리포인지 확인
if [ ! -d ".git" ]; then
  echo "git-sync: .claude는 git 리포가 아닙니다"
  exit 0
fi

if [ "$ACTION" = "pull" ]; then
  # 세션 시작 시: 원격에서 최신 버전 가져오기
  git stash --quiet 2>/dev/null
  git pull --rebase origin main --quiet 2>/dev/null
  git stash pop --quiet 2>/dev/null
  echo "git-sync: pull 완료"

elif [ "$ACTION" = "push" ]; then
  # 세션 종료 시: 변경사항 자동 커밋 + push
  CHANGES=$(git status --porcelain 2>/dev/null | wc -l)
  if [ "$CHANGES" -gt 0 ]; then
    git add -A
    TIMESTAMP=$(date +"%Y-%m-%d_%H:%M")
    git commit -m "auto: ${TIMESTAMP}" --quiet 2>/dev/null
    git push origin main --quiet 2>/dev/null
    echo "git-sync: push 완료 (${CHANGES}개 파일)"
  else
    echo "git-sync: 변경사항 없음"
  fi
fi
