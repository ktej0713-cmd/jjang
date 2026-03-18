#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
짱베이스볼 프롬프트 자동 강화 훅 v2
- 스킬 레지스트리 기반 동적 컨텍스트 주입
- 세션 패턴 로그 기반 추천
- UserPromptSubmit 훅에서 호출됨
"""
import sys
import json
import io
import os
import re

# Windows UTF-8 인코딩 강제 적용
if sys.platform == "win32":
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CLAUDE_DIR = os.path.expanduser("~/.claude")
REGISTRY_PATH = os.path.join(CLAUDE_DIR, "skill-registry.json")
PATTERN_LOG = os.path.join(CLAUDE_DIR, "logs", "patterns.jsonl")


def load_registry():
    """스킬 레지스트리를 로드합니다."""
    if not os.path.exists(REGISTRY_PATH):
        return {}
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_recent_patterns():
    """최근 반복 패턴을 로드합니다."""
    if not os.path.exists(PATTERN_LOG):
        return {}
    try:
        last_line = ""
        with open(PATTERN_LOG, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last_line = line.strip()
        if last_line:
            return json.loads(last_line)
    except Exception:
        pass
    return {}


def find_matching_skills(prompt, registry):
    """프롬프트와 매칭되는 스킬을 찾습니다."""
    p = prompt.strip().lower()
    matches = []

    for skill_id, info in registry.items():
        score = 0
        # 스킬 이름이 프롬프트에 포함
        if skill_id.replace("-", " ") in p or skill_id.replace("-", "") in p:
            score += 10

        # 키워드 매칭
        for kw in info.get("keywords", []):
            if kw.lower() in p:
                score += 2

        # 설명 키워드 매칭
        desc = info.get("description", "").lower()
        desc_words = set(re.findall(r"[가-힣]{2,}|[a-z]{3,}", desc))
        prompt_words = set(re.findall(r"[가-힣]{2,}|[a-z]{3,}", p))
        overlap = desc_words & prompt_words
        score += len(overlap)

        if score >= 3:
            matches.append((skill_id, score, info.get("description", "")))

    # 점수 내림차순 정렬, 상위 3개
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:3]


def enhance(prompt):
    """프롬프트를 분석하여 컨텍스트를 생성합니다."""
    p = prompt.strip().lower()

    # --- 기본 키워드 매칭 (고정 규칙) ---
    context_parts = []

    # 짱베이스볼 관련 키워드
    base_keywords = [
        "상세페이지", "기획전", "배너", "카테고리", "상품", "글러브", "배트",
        "야구", "프로모션", "seo", "카피", "콘텐츠", "html", "소싱", "브랜드",
        "md", "재고", "발주", "메일", "자동화", "스마트스토어", "고도몰",
        "가격", "경쟁", "시즌", "품질", "검증"
    ]

    if not any(kw in p for kw in base_keywords):
        return ""

    # 상세페이지
    if any(kw in p for kw in ["상세페이지", "상품설명", "product"]):
        context_parts.append(
            "상세페이지 10단계 표준 구조 적용: 히어로+1줄정의 > 필요상황 > 스펙표 > 체감설명 > "
            "포지션별추천 > 사이즈가이드 > 비교표 > FAQ > 추천포인트 > 배송안내. "
            "결과물은 ~/.claude/output/ 에 HTML로 저장."
        )

    # 기획전/배너
    if any(kw in p for kw in ["기획전", "배너", "이벤트", "프로모션"]):
        context_parts.append(
            "고도몰5 에디터 호환 HTML 출력. 디자인 시스템 컬러(primary:#1B2A4A, accent:#D4A843) 적용. "
            "결과물은 ~/.claude/output/ 에 저장."
        )

    # SEO
    if any(kw in p for kw in ["seo", "검색", "키워드", "메타"]):
        context_parts.append(
            "네이버 쇼핑 1순위 최적화. JSON-LD 구조화 데이터(Product+Offer+AggregateRating) 포함."
        )

    # 자동화/개발
    if any(kw in p for kw in ["자동화", "스마트스토어", "고도몰", "php", "python", "스크립트"]):
        context_parts.append(
            "고도몰5 플랫폼(PHP+Symfony). 코어 파일 직접 수정 금지, 모듈 방식으로 확장. "
            "SQL Injection/XSS 방지 필수."
        )

    # 가격/경쟁
    if any(kw in p for kw in ["가격", "경쟁", "비교", "마진"]):
        context_parts.append(
            "오픈마켓(네이버/쿠팡/11번가/지마켓) 중심 가격 비교. "
            "야구야닷컴/베이스볼파크는 경쟁 대상 아님."
        )

    # --- 동적 스킬 매칭 ---
    registry = load_registry()
    if registry:
        matches = find_matching_skills(prompt, registry)
        if matches:
            skill_hints = []
            for skill_id, score, desc in matches:
                skill_hints.append(f"/{skill_id}")
            if skill_hints:
                context_parts.append(f"관련 스킬: {', '.join(skill_hints)}")

    # --- 반복 패턴 알림 ---
    patterns = load_recent_patterns()
    if patterns.get("suggestion"):
        freq_skills = patterns.get("frequent_skills", {})
        if freq_skills:
            top_skill = max(freq_skills, key=freq_skills.get)
            context_parts.append(f"최근 자주 사용: /{top_skill}")

    # 폴백
    if not context_parts:
        context_parts.append(
            "짱베이스볼(jjangbaseball.com) 야구용품 전문몰 관점으로 답변. "
            "결과물은 바로 쇼핑몰에 적용 가능해야 함."
        )

    return "[짱베이스볼 컨텍스트] " + " | ".join(context_parts)


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
        prompt = data.get("prompt", "")
    except Exception:
        print(json.dumps({"decision": "approve"}, ensure_ascii=False))
        return

    extra = enhance(prompt)

    if extra:
        result = {
            "decision": "approve",
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": extra
            }
        }
    else:
        result = {"decision": "approve"}

    print(json.dumps(result, ensure_ascii=False))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
