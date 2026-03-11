# 스마트스토어 태그 자동화 CLI 도구

## Context
짱베이스볼 스마트스토어 상품의 SEO 태그를 자동으로 적용하는 도구.
현재 `_debug/` 폴더에 흩어진 스크립트들을 하나의 CLI 도구로 통합하여,
회사 컴퓨터와 집 컴퓨터 모두에서 **상품번호만 입력하면 자동으로 태그 검색 → 적용 → 검증**이 완료되도록 한다.

### 해결하는 문제
1. 매번 스크립트를 수동으로 수정해야 함 (상품번호, 태그 하드코딩)
2. 태그 점수 알고리즘이 "블루투스" 같은 무관한 태그를 선택함
3. 차단 단어 처리가 일회성 (학습 안 됨)
4. 상품번호 유형(channel/origin/그룹) 매핑이 불안정

## 사용법
```bash
# Chrome을 --remote-debugging-port=9222로 실행 후:
python smartstore_tags.py 13189721466
python smartstore_tags.py 13189721466 --dry-run    # 태그만 검색, 적용 안 함
python smartstore_tags.py 13189721466 --tags "배팅장갑,타격장갑,야구장갑"  # 수동 태그 지정
```

## 파일 구조

### 신규 생성 (6개)
```
automation/smartstore-updater/
├── smartstore_tags.py              # CLI 진입점 (argparse)
├── selenium_handler/
│   ├── js_utils.py                 # JS 실행 유틸 (safe_execute, close_modals 등)
│   ├── tag_search.py               # 태그사전 검색 (selectize autocomplete)
│   ├── tag_applier.py              # 태그 적용 + 저장 + 차단단어 재시도
│   └── tag_verifier.py             # 저장 후 검증 (재로딩 → 태그 확인)
└── tags/
    └── scorer.py                   # 태그 점수 산정 (야구 도메인 가중치)
```

### 기존 재사용
- `selenium_handler/browser.py` — Chrome debug 연결
- `selenium_handler/navigator.py` — 상품 페이지 이동 (수정 필요: origin/channel/그룹 매핑)
- `config.py` — 설정값
- `data/models.py` — 데이터 클래스

### 신규 데이터 파일
- `data/blocked_words.json` — 차단 단어 누적 캐시

## 구현 상세

### 1. `smartstore_tags.py` — CLI 진입점
```python
# argparse: product_id (필수), --dry-run, --tags, --max-tags (기본 10)
# 흐름: 브라우저 연결 → 상품 이동 → 태그 검색 → 점수 산정 → 적용 → 검증
```

### 2. `selenium_handler/js_utils.py` — JS 유틸
기존 `_debug/` 스크립트에서 반복되는 패턴 통합:
- `safe_execute(driver, script, *args, retries=3)` — alert 자동 처리
- `safe_dismiss_alert(driver)` — 반복 alert dismiss
- `close_all_modals(driver)` — 모달 닫기
- `safe_url(driver)` — alert-safe URL 조회

### 3. `selenium_handler/tag_search.py` — 태그사전 검색
검증된 방식 (`_debug/find_dictionary_tags.py`):
```
selectize ctrl.setTextboxValue(keyword) → onSearchChange → 1초 대기 → $dropdown_content 파싱
```
- `search_dictionary_tags(driver, keywords: list[str]) -> list[str]`
- 상품명에서 키워드 자동 추출 (2~4글자 조합)
- 야구 도메인 키워드 우선 검색

### 4. `tags/scorer.py` — 태그 점수 (핵심 개선)
```python
BASEBALL_DOMAIN = {"배팅장갑", "타격장갑", "글러브", "야구글러브", ...}  # +10
NON_BASEBALL = {"블루투스", "블루레이", "블루베리", "블루종", ...}       # -50 (즉시 제외)

def score_tag(tag, product_name, category_keywords):
    if tag in NON_BASEBALL: return -50
    score = 0
    if tag in product_name: score += 10      # 상품명에 포함
    if tag in BASEBALL_DOMAIN: score += 10   # 야구 도메인
    if tag in category_keywords: score += 5  # 카테고리 관련
    # 부분 일치는 2글자 이상만, +2점
    return score
```

### 5. `selenium_handler/tag_applier.py` — 태그 적용
검증된 방식 (`_debug/apply_dictionary_tags_v3.py`):
```
ngModel.$setViewValue(arr) + $setDirty() + $parentForm.$setDirty()
+ scope.vm.product...sellerTags = arr + scope.$apply()
→ 저장하기 클릭 → 팝업 확인
→ 차단 단어 시 자동 제거 후 재시도 (최대 3회)
→ 차단 단어를 data/blocked_words.json에 누적 저장
```

### 6. `selenium_handler/tag_verifier.py` — 검증
- 목록 → 수정 페이지 재이동 → sellerTags ngModel 읽기
- 적용한 태그와 비교 → PASS/FAIL 출력

### 7. `navigator.py` 수정 — 상품번호 매핑
현재 문제: channelProductNo로만 이동 시도함
수정: ag-Grid API로 origin/channel/그룹 매핑 후 originProductNo로 이동
```python
def find_origin_product_no(self, product_id: str) -> str:
    # 1. ag-Grid에서 검색 (channel/origin/그룹 모두 매칭)
    # 2. 없으면 페이지 넘기며 검색
    # 3. originProductNo 반환
```

## 구현 순서
1. `js_utils.py` — 기반 유틸 (의존성 없음)
2. `scorer.py` — 점수 산정 (의존성 없음)
3. `data/blocked_words.json` — 빈 캐시 파일
4. `tag_search.py` — 태그사전 검색 (js_utils 의존)
5. `tag_applier.py` — 태그 적용 (js_utils, scorer 의존)
6. `tag_verifier.py` — 검증 (js_utils 의존)
7. `navigator.py` 수정 — 상품번호 매핑 추가
8. `smartstore_tags.py` — CLI 통합
9. 테스트: 기존 성공 상품 (13042924986, 13131430426)으로 검증

## 검증 방법
```bash
# 1. Chrome을 디버그 모드로 실행 (스마트스토어 로그인 상태)
# 2. dry-run으로 태그 검색만 확인
python smartstore_tags.py 13042924986 --dry-run

# 3. 실제 적용 (이미 성공한 상품으로 안전 테스트)
python smartstore_tags.py 13042924986

# 4. 새 상품 테스트
python smartstore_tags.py [새상품번호]
```

## 다른 컴퓨터 설치
```bash
# 1. 저장소 클론 또는 폴더 복사
# 2. pip install -r requirements.txt
# 3. Chrome 디버그 모드 실행
chrome.exe --remote-debugging-port=9222
# 4. 스마트스토어 로그인 후 사용
python smartstore_tags.py [상품번호]
```
