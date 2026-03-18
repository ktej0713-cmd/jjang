---
name: verify-html
description: 상세페이지/기획전 HTML 결과물을 고도몰 호환성, 디자인 시스템, SEO 기준으로 검증합니다.
argument-hint: "[HTML 파일 경로]"
---

# HTML 결과물 검증

생성된 상세페이지/기획전 HTML이 짱베이스볼 표준을 준수하는지 자동 검증합니다.

## 실행 시점

- 상세페이지 HTML 생성 후
- 기획전 페이지 생성 후
- 품질체크 전 사전 검증으로
- HTML 수정 후 재검증

## 검증 대상 파일 탐색

`$ARGUMENTS`가 있으면 해당 파일을 검증합니다.
없으면 최근 변경된 HTML을 찾습니다:

```bash
find ~/.claude/output -name "*.html" -mmin -60 -type f 2>/dev/null | head -5
```

## 워크플로우

### Step 1: 고도몰 에디터 호환성 검증

| 검사 항목 | PASS 기준 | FAIL 기준 |
|-----------|----------|----------|
| 레이아웃 | table 기반 | flexbox/grid 사용 |
| 폰트 | 시스템 폰트 또는 Pretendard | 웹폰트 CDN 의존 |
| 이미지 경로 | 실제 경로 또는 플레이스홀더 명시 | 깨진 URL |
| 특수문자 | HTML 엔티티 사용 | 유니코드 직접 입력 |
| 인라인 SVG | 최소 사용 | 장식용 SVG 남발 |
| max-width | 860px (상세페이지) | 초과 |

검사 방법:
```bash
# flexbox/grid 사용 여부
grep -inE 'display:\s*(flex|grid)' FILE.html

# 외부 CDN 폰트 의존
grep -inE 'fonts\.googleapis|cdn.*font' FILE.html

# 이미지 경로 확인
grep -oP 'src="[^"]*"' FILE.html | grep -vE '(placeholder|via\.placeholder|dummyimage)'
```

### Step 2: 디자인 시스템 준수 검증

| 검사 항목 | PASS 기준 | FAIL 기준 |
|-----------|----------|----------|
| 컬러 | CSS 변수 또는 디자인 시스템 HEX | 하드코딩된 임의 색상 |
| 금지 요소 | 없음 | 이모지, 무의미한 아이콘 장식 |
| border-radius | 필요한 곳만 | 모든 요소에 일괄 적용 |
| 그림자 | 필요한 곳만 | 모든 요소에 일괄 적용 |
| 그라데이션 | 히어로 등 제한적 | 남발 |

검사 방법:
```bash
# 하드코딩 색상 (디자인 시스템 외)
grep -oP '#[0-9a-fA-F]{3,8}' FILE.html | sort -u | grep -ivE '(1B2A4A|2C3E6B|0F1A30|D4A843|E8C876|B8922E|2E7D32|E65100|C62828|1565C0|E53935|222222|555555|888888|CCCCCC|F5F5F5|FAFAFA|FFFFFF|F9F9F9|FDF8EC|000000|fff)'

# 이모지 사용 여부
grep -P '[\x{1F300}-\x{1F9FF}]' FILE.html
```

### Step 3: SEO 기본 검증

| 검사 항목 | PASS 기준 | FAIL 기준 |
|-----------|----------|----------|
| 이미지 alt | 모든 img에 alt 속성 | alt 누락 |
| 제목 계층 | H1 1개, H2~H4 순서대로 | H1 복수 또는 계층 건너뜀 |
| 링크 텍스트 | 의미 있는 텍스트 | "여기 클릭" |

검사 방법:
```bash
# alt 없는 이미지
grep -inE '<img[^>]*(?!alt)' FILE.html

# H1 개수
grep -ciE '<h1' FILE.html
```

### Step 4: 콘텐츠 품질 검증

| 검사 항목 | PASS 기준 | FAIL 기준 |
|-----------|----------|----------|
| 금지 표현 | 없음 | "최저가 보장", "파격 할인", "보통 쇼핑몰에서는" |
| 야구 용어 | 커뮤니티 실제 용어 | 부자연스러운 표현 |
| 플레이스홀더 | 없음 | "Lorem ipsum", "TODO", "여기에 입력" 잔존 |

검사 방법:
```bash
# 금지 표현
grep -inE '최저가 보장|파격 할인|보통 쇼핑몰|업계 최초|혁신적인' FILE.html

# 플레이스홀더 잔존
grep -inE 'lorem ipsum|TODO|FIXME|여기에 입력|텍스트를 입력|placeholder text' FILE.html
```

### Step 5: 기술 검증

| 검사 항목 | PASS 기준 | FAIL 기준 |
|-----------|----------|----------|
| HTML 유효성 | 태그 닫힘 정상 | 닫히지 않은 태그 |
| CSS 충돌 | 스코프된 선택자 | 전역 * 선택자 |
| JS 에러 | 없음 | 문법 에러 |
| 파일 크기 | 500KB 이하 | 초과 |

검사 방법:
```bash
# 파일 크기
wc -c FILE.html

# 전역 와일드카드 선택자
grep -nE '^\s*\*\s*\{' FILE.html

# 닫히지 않은 태그 (간이 검사)
python3 -c "
from html.parser import HTMLParser
import sys

class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void = {'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}
    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.void:
            self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

with open('FILE.html') as f:
    checker = TagChecker()
    checker.feed(f.read())
    for tag, pos in checker.stack:
        print(f'UNCLOSED: <{tag}> at line {pos[0]}')
" 2>/dev/null
```

## 출력 형식

```markdown
## HTML 검증 결과

**파일:** `파일명.html`
**검증 시간:** YYYY-MM-DD HH:MM

### 요약
| 카테고리 | 결과 | 이슈 수 |
|---------|------|---------|
| 고도몰 호환성 | PASS/FAIL | N |
| 디자인 시스템 | PASS/FAIL | N |
| SEO | PASS/FAIL | N |
| 콘텐츠 품질 | PASS/FAIL | N |
| 기술 검증 | PASS/FAIL | N |

**총점:** X/5 PASS

### 발견된 이슈
| # | 카테고리 | 라인 | 문제 | 수정 방법 |
|---|---------|------|------|----------|
| 1 | ... | ... | ... | ... |
```

## 예외사항

1. **플레이스홀더 이미지 경로** - `via.placeholder.com`, `dummyimage.com`은 개발 단계에서 허용
2. **인라인 스타일** - 고도몰 에디터 붙여넣기용 HTML은 인라인 스타일 허용
3. **외부 JS** - analytics, GTM 등 트래킹 스크립트는 CDN 허용
