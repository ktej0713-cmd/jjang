#!/usr/bin/env bash
# Hook: Stop (async)
# 세션 활동을 추적하여 자동 강화 시스템에 데이터를 제공합니다.
# 기록: 날짜, 사용된 스킬, 생성된 파일, 반복 패턴

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
LOG_DIR="$CLAUDE_DIR/logs"
mkdir -p "$LOG_DIR"

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
SESSION_LOG="$LOG_DIR/sessions.jsonl"
PATTERN_LOG="$LOG_DIR/patterns.jsonl"

# --- 1. 이번 세션에서 변경/생성된 파일 수집 ---
OUTPUT_DIR="$CLAUDE_DIR/output"
NEW_FILES=""
if [ -d "$OUTPUT_DIR" ]; then
  # 최근 2시간 이내 수정된 파일
  NEW_FILES=$(find "$OUTPUT_DIR" -type f -mmin -120 -name "*.html" 2>/dev/null | while read -r f; do basename "$f"; done | tr '\n' ',' | sed 's/,$//')
fi

# --- 2. 스킬 사용 흔적 감지 ---
# .claude 디렉토리에서 최근 변경된 스킬 파일
USED_SKILLS=""
if [ -d "$CLAUDE_DIR/skills" ]; then
  USED_SKILLS=$(find "$CLAUDE_DIR/skills" -name "SKILL.md" -mmin -120 2>/dev/null | while read -r f; do
    dirname "$f" | xargs basename
  done | tr '\n' ',' | sed 's/,$//')
fi

# --- 3. 세션 로그 기록 (JSONL 형식) ---
# python3으로 안전한 JSON 생성
python3 -c "
import json, sys
entry = {
    'date': '$DATE',
    'time': '$TIME',
    'output_files': '${NEW_FILES}'.split(',') if '${NEW_FILES}' else [],
    'modified_skills': '${USED_SKILLS}'.split(',') if '${USED_SKILLS}' else [],
}
print(json.dumps(entry, ensure_ascii=False))
" >> "$SESSION_LOG" 2>/dev/null || true

# --- 4. 반복 패턴 감지 ---
# 최근 7일 세션 로그에서 반복되는 output 파일 접두사 추출
if [ -f "$SESSION_LOG" ]; then
  python3 -c "
import json, sys, re
from collections import Counter
from datetime import datetime, timedelta

cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
prefixes = Counter()
skill_freq = Counter()

with open('$SESSION_LOG') as f:
    for line in f:
        try:
            entry = json.loads(line.strip())
            if entry.get('date','') >= cutoff:
                for fname in entry.get('output_files', []):
                    if fname:
                        # 파일명에서 패턴 추출 (예: 'mizuno-pro-detail.html' -> 'detail')
                        parts = fname.replace('.html','').split('-')
                        for p in parts:
                            if p in ('detail','event','banner','plan','compare'):
                                prefixes[p] += 1
                for skill in entry.get('modified_skills', []):
                    if skill:
                        skill_freq[skill] += 1
        except:
            continue

# 3회 이상 반복된 패턴 기록
patterns = {k:v for k,v in prefixes.items() if v >= 3}
skills = {k:v for k,v in skill_freq.items() if v >= 2}

if patterns or skills:
    result = {
        'date': '$DATE',
        'repeated_output_types': patterns,
        'frequent_skills': skills,
        'suggestion': '반복 패턴 감지됨 - /auto-enhance 실행 권장'
    }
    print(json.dumps(result, ensure_ascii=False))
" >> "$PATTERN_LOG" 2>/dev/null || true
fi
