#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
스킬 레지스트리 자동 동기화
SessionStart 훅에서 호출됨
스킬 디렉토리를 스캔하여 skill-registry.json을 생성/갱신
"""
import os
import json
import re
import glob
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CLAUDE_DIR = os.path.expanduser("~/.claude")
SKILLS_DIR = os.path.join(CLAUDE_DIR, "skills")
REGISTRY_PATH = os.path.join(CLAUDE_DIR, "skill-registry.json")


def main():
    if not os.path.isdir(SKILLS_DIR):
        return

    registry = {}

    for skill_file in sorted(glob.glob(os.path.join(SKILLS_DIR, "*/SKILL.md"))):
        dir_name = os.path.basename(os.path.dirname(skill_file))

        try:
            with open(skill_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue

        name = dir_name
        description = ""
        argument_hint = ""

        # frontmatter 파싱
        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)

            nm = re.search(r"name:\s*(.+)", fm)
            if nm:
                name = nm.group(1).strip()

            dm = re.search(r"description:\s*(.+)", fm)
            if dm:
                description = dm.group(1).strip()

            ah = re.search(r"argument-hint:\s*(.+)", fm)
            if ah:
                argument_hint = ah.group(1).strip().strip('"')

        # 키워드 추출
        ko_kw = re.findall(r"[\uac00-\ud7a3]{2,}", description)
        en_kw = re.findall(r"[a-zA-Z]{3,}", description.lower())
        keywords = list(set(ko_kw + en_kw))[:10]

        registry[dir_name] = {
            "name": name,
            "description": description,
            "keywords": keywords,
            "argument_hint": argument_hint,
            "path": skill_file,
        }

    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "additionalContext": f"스킬 레지스트리 동기화 완료: {len(registry)}개 스킬"
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
