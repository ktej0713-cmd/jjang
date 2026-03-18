#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
일일 시스템 운영 보고서 생성
크론 트리거 → 에이전트가 이 스크립트 결과를 메일로 발송
"""
import os
import json
import io
import sys
from datetime import datetime, timedelta

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CLAUDE_DIR = os.path.expanduser("~/.claude")
LOGS_DIR = os.path.join(CLAUDE_DIR, "logs")
REGISTRY_PATH = os.path.join(CLAUDE_DIR, "skill-registry.json")
SESSION_LOG = os.path.join(LOGS_DIR, "sessions.jsonl")
OPS_REPORT = os.path.join(LOGS_DIR, "ops-report.md")
OUTPUT_DIR = os.path.join(CLAUDE_DIR, "output")

today = datetime.now().strftime("%Y-%m-%d")
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")


def count_skills():
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return len(json.load(f))
    return 0


def analyze_sessions():
    """최근 세션 분석"""
    if not os.path.exists(SESSION_LOG):
        return {"total_7d": 0, "yesterday": 0, "output_files": []}

    total_7d = 0
    yesterday_count = 0
    recent_outputs = []

    with open(SESSION_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                date = entry.get("date", "")
                if date >= week_ago:
                    total_7d += 1
                if date == yesterday:
                    yesterday_count += 1
                    for f_name in entry.get("output_files", []):
                        if f_name:
                            recent_outputs.append(f_name)
            except Exception:
                continue

    return {
        "total_7d": total_7d,
        "yesterday": yesterday_count,
        "output_files": recent_outputs[-5:],
    }


def count_recent_outputs():
    """최근 7일 output 파일"""
    if not os.path.isdir(OUTPUT_DIR):
        return []

    results = []
    cutoff = datetime.now().timestamp() - 7 * 86400
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                if os.path.getmtime(fpath) >= cutoff:
                    results.append(fname)
            except Exception:
                continue
    return results[-10:]


def get_ops_report():
    """최근 ops 보고서"""
    if os.path.exists(OPS_REPORT):
        with open(OPS_REPORT, "r", encoding="utf-8") as f:
            return f.read()
    return "아직 운영 보고서가 없습니다."


def generate_report():
    skill_count = count_skills()
    sessions = analyze_sessions()
    recent_outputs = count_recent_outputs()
    ops = get_ops_report()

    report = f"""짱베이스볼 MD팀 일일 보고서
날짜: {today}

[시스템 현황]
- 등록 스킬: {skill_count}개
- 최근 7일 세션: {sessions['total_7d']}회
- 어제 세션: {sessions['yesterday']}회

[최근 결과물]
"""
    if recent_outputs:
        for f in recent_outputs:
            report += f"- {f}\n"
    else:
        report += "- 최근 7일간 생성된 결과물 없음\n"

    if sessions["output_files"]:
        report += f"\n[어제 생성 파일]\n"
        for f in sessions["output_files"]:
            report += f"- {f}\n"

    report += f"""
[운영 보고서 요약]
{ops[:500]}
"""

    return report


if __name__ == "__main__":
    print(generate_report())
