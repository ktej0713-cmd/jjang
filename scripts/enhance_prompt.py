#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
짱베이스볼 프롬프트 자동 강화 훅
UserPromptSubmit 훅에서 호출됨
"""
import sys
import json
import io

# Windows UTF-8 인코딩 강제 적용
if sys.platform == "win32":
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def enhance(prompt: str) -> str:
    p = prompt.strip().lower()

    # 짱베이스볼 관련 키워드
    keywords = [
        "상세페이지", "기획전", "배너", "카테고리", "상품", "글러브", "배트",
        "야구", "프로모션", "seo", "카피", "콘텐츠", "html", "소싱", "브랜드",
        "md", "재고", "발주", "메일", "자동화", "스마트스토어", "고도몰"
    ]

    if not any(kw in p for kw in keywords):
        return ""  # 무관한 대화는 강화 안 함

    context_parts = []

    # 상세페이지 요청
    if any(kw in p for kw in ["상세페이지", "상품설명", "product"]):
        context_parts.append(
            "상세페이지 10단계 표준 구조 적용: 히어로+1줄정의 → 필요상황 → 스펙표 → 체감설명 → 포지션별추천 → 사이즈가이드 → 비교표 → FAQ → 추천포인트 → 배송안내. "
            "결과물은 ~/.claude/output/상세페이지/ 에 HTML로 저장."
        )

    # 기획전/배너 요청
    if any(kw in p for kw in ["기획전", "배너", "이벤트", "프로모션"]):
        context_parts.append(
            "고도몰5 에디터 호환 HTML 출력. 디자인 시스템 컬러(primary:#1B2A4A, accent:#D4A843) 적용. "
            "결과물은 ~/.claude/output/ 에 저장."
        )

    # SEO 관련
    if any(kw in p for kw in ["seo", "검색", "키워드", "메타"]):
        context_parts.append(
            "네이버 쇼핑 1순위 최적화. JSON-LD 구조화 데이터(Product+Offer+AggregateRating) 포함. "
            "GEO 최적화: 두괄식 + 불릿 + 표 + FAQ 구조."
        )

    # 자동화/개발
    if any(kw in p for kw in ["자동화", "스마트스토어", "고도몰", "php", "python", "스크립트"]):
        context_parts.append(
            "고도몰5 플랫폼(PHP+Symfony). 코어 파일 직접 수정 금지, 모듈 방식으로 확장. "
            "SQL Injection/XSS 방지 필수."
        )

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
