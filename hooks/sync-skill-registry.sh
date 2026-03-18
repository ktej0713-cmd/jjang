#!/usr/bin/env bash
# Hook: SessionStart
# 스킬 디렉토리를 스캔하여 레지스트리 파일을 자동 생성/갱신합니다.
# 새 스킬이 추가되면 자동으로 감지되어 enhance_prompt.py에서 활용됩니다.

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_DIR/skills"
REGISTRY="$CLAUDE_DIR/skill-registry.json"

if [ ! -d "$SKILLS_DIR" ]; then
  exit 0
fi

python3 -c "
import os, json, re, glob

skills_dir = '$SKILLS_DIR'
registry = {}

for skill_dir in sorted(glob.glob(os.path.join(skills_dir, '*/SKILL.md'))):
    dir_name = os.path.basename(os.path.dirname(skill_dir))

    with open(skill_dir, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # frontmatter 파싱
    name = dir_name
    description = ''
    keywords = []
    argument_hint = ''

    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)

        nm = re.search(r'name:\s*(.+)', fm)
        if nm: name = nm.group(1).strip()

        dm = re.search(r'description:\s*(.+)', fm)
        if dm: description = dm.group(1).strip()

        ah = re.search(r'argument-hint:\s*(.+)', fm)
        if ah: argument_hint = ah.group(1).strip().strip('\"')

    # 설명에서 키워드 추출 (한국어 + 영어)
    desc_lower = description.lower()
    # 한국어 키워드
    ko_kw = re.findall(r'[가-힣]{2,}', description)
    # 영어 키워드
    en_kw = re.findall(r'[a-zA-Z]{3,}', desc_lower)
    keywords = list(set(ko_kw + en_kw))[:10]

    registry[dir_name] = {
        'name': name,
        'description': description,
        'keywords': keywords,
        'argument_hint': argument_hint,
        'path': skill_dir
    }

with open('$REGISTRY', 'w', encoding='utf-8') as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)

print(f'스킬 레지스트리 동기화: {len(registry)}개 스킬 등록')
" 2>/dev/null || echo "스킬 레지스트리 동기화 실패"
