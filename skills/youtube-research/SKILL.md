---
name: youtube-research
description: YouTube 영상의 자막/내용을 추출하여 분석합니다. 영상 URL을 입력하면 자막 기반으로 핵심 내용을 정리합니다.
argument-hint: "<YouTube URL> [분석 관점]"
---

# YouTube 영상 리서치

YouTube 영상의 자막(transcript)을 추출하고 분석하여, 짱베이스볼 프로젝트에 적용 가능한 인사이트를 정리합니다.

## 현재 컨텍스트

- 입력: `$ARGUMENTS` (YouTube URL + 선택적 분석 관점)

## 워크플로우

### Step 1: URL 파싱 및 영상 정보 수집

1. YouTube URL에서 video ID를 추출합니다 (v= 파라미터)
2. noembed API로 기본 정보를 가져옵니다:

```bash
curl -s "https://noembed.com/embed?url=https://www.youtube.com/watch?v=VIDEO_ID"
```

3. 영상 제목, 채널명을 표시합니다.

### Step 2: 자막 추출 (3가지 방법 순차 시도)

**방법 A: yt-dlp (설치된 경우)**

```bash
yt-dlp --write-auto-sub --sub-lang ko,en --skip-download --sub-format json3 -o "/tmp/yt-%(id)s" "VIDEO_URL" 2>/dev/null
```

json3 자막 파일이 생성되면 파싱합니다.

자막 텍스트만 추출:
```bash
yt-dlp --write-auto-sub --sub-lang ko,en --skip-download --sub-format vtt -o "/tmp/yt-%(id)s" "VIDEO_URL" 2>/dev/null
cat /tmp/yt-VIDEO_ID.ko.vtt 2>/dev/null || cat /tmp/yt-VIDEO_ID.en.vtt 2>/dev/null
```

**방법 B: youtube-transcript-api (Python)**

```bash
pip install youtube-transcript-api 2>/dev/null
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
try:
    transcript = YouTubeTranscriptApi.get_transcript('VIDEO_ID', languages=['ko','en'])
    for entry in transcript:
        print(entry['text'])
except Exception as e:
    print(f'ERROR: {e}')
"
```

**방법 C: 웹 검색 폴백**

자막 추출이 모두 실패하면:
1. WebSearch로 "영상제목 + 요약/리뷰/정리" 검색
2. 블로그/커뮤니티 요약 게시물을 WebFetch로 수집
3. 수집된 정보를 기반으로 분석

### Step 3: 내용 분석

추출된 자막/내용을 다음 구조로 분석합니다:

```markdown
## 영상 분석 결과

### 기본 정보
- 제목:
- 채널:
- URL:

### 핵심 내용 요약
(3-5줄 요약)

### 주요 포인트
1. ...
2. ...
3. ...

### 짱베이스볼 적용 가능 사항
| 포인트 | 적용 방안 | 우선순위 |
|--------|----------|---------|
| ... | ... | 높음/중간/낮음 |

### 액션 아이템
- [ ] ...
- [ ] ...
```

### Step 4: 분석 관점별 특화

`$ARGUMENTS`에 분석 관점이 지정된 경우:

- **상품/소싱**: 언급된 브랜드, 상품, 가격대, 트렌드 추출
- **마케팅/프로모션**: 프로모션 전략, 이벤트 아이디어, 카피 참고
- **기술/개발**: 기술 스택, 구현 방법, 도구 활용법 추출
- **경쟁사**: 경쟁사 전략, 차별점, 벤치마킹 포인트 추출

## 주의사항

- 자막이 자동 생성된 경우 오역이 있을 수 있음을 명시합니다
- 영상 내용을 그대로 복사하지 않고, 분석/요약 형태로 제공합니다
- 저작권 관련 주의사항을 안내합니다
