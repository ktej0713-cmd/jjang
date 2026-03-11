# 네이버 스마트스토어 상품 일괄 수정 자동화 프로그램

## Context
짱베이스볼 스마트스토어의 **상품 주요정보, 상품정보제공고시, 검색설정(태그)**을 일괄 수정하는 자동화 프로그램이 필요합니다. 수십~수백 개 상품을 하나씩 수동으로 수정하는 비효율을 해결하기 위한 도구입니다.

## 핵심 설계 결정: 하이브리드 방식 (API + Selenium)

| 작업 | 수단 | 이유 |
|---|---|---|
| 상품 주요정보 수정 | **커머스 API** | 안정적, 빠름, 에러 핸들링 용이 |
| 검색태그 수정 | **커머스 API** | `seoInfo.tags` 필드로 직접 수정 가능 |
| 상품정보제공고시 수정 | **Selenium** | 카테고리별 동적 폼 구조가 복잡, 브라우저 조작이 직관적 |

> API 키를 이미 보유 중이므로, 안정적인 항목은 API로 처리하고 복잡한 UI 폼만 Selenium으로 처리합니다.

---

## 파일 구조

```
~/.claude/automation/smartstore-updater/
├── main.py                    # CLI 진입점 (--mode all|api|selenium --dry-run)
├── config.py                  # 환경변수/설정 관리
├── requirements.txt           # 의존성 패키지
│
├── api/
│   ├── auth.py                # OAuth2 토큰 발급 (bcrypt 서명)
│   ├── client.py              # API 기본 클라이언트 (requests)
│   └── products.py            # 상품 조회/수정 함수 (read-modify-write 패턴)
│
├── selenium_handler/
│   ├── browser.py             # Chrome 드라이버 초기화 (프로필/디버깅 모드)
│   └── disclosure_form.py     # 상품정보제공고시 폼 자동 입력
│
├── data/
│   ├── models.py              # 데이터 모델 (dataclass)
│   └── excel_reader.py        # 엑셀 파싱 + 유효성 검사
│
└── logger/
    ├── run_logger.py           # JSON 히스토리 + 콘솔 출력
    └── report.py               # HTML 리포트 생성

~/.claude/automation/input/
└── products-update.xlsx        # 수정할 상품 데이터 (3개 시트)

~/output/smartstore-updates/    # 실행 결과 HTML 리포트
```

---

## 엑셀 입력 파일 구조 (3개 시트)

**Sheet 1: `main_info`** — 상품 주요정보

| channel_product_no | product_name | sale_price | category_id |
|---|---|---|---|
| 8234567890 | 미즈노 글러브 GXF72B | 185000 | (빈칸=유지) |

**Sheet 2: `tags`** — 검색태그

| channel_product_no | tag1 | tag2 | ... | tag10 |
|---|---|---|---|---|
| 8234567890 | 야구글러브 | 미즈노 | ... | 사회인야구 |

**Sheet 3: `disclosure`** — 상품정보제공고시

| channel_product_no | notice_type | material | color | size | manufacturer | origin | as_phone | wash_care |
|---|---|---|---|---|---|---|---|---|
| 8234567890 | WEAR | 소가죽 | 갈색 | 11.5인치 | Mizuno | 일본 | 02-1234-5678 | 부드러운 천으로 닦기 |

---

## 실행 흐름

```
1. 엑셀 로드 → 유효성 검사
2. API 작업 (주요정보 + 태그)
   └─ 각 상품: GET 조회 → merge 변경값 → PUT 수정
3. Selenium 작업 (상품정보제공고시)
   └─ Chrome 시작 → 상품 수정 페이지 이동 → 고시 폼 입력 → 저장
4. 결과 집계 → HTML 리포트 생성
```

---

## CLI 사용법

```bash
# 전체 실행 (API + Selenium)
python main.py --mode all

# API만 (주요정보 + 태그)
python main.py --mode api

# Selenium만 (상품정보제공고시)
python main.py --mode selenium

# 시뮬레이션 (실제 수정 없이 테스트)
python main.py --mode all --dry-run

# jjang CLI 통합
bash ~/.claude/scripts/jjang.sh smartstore all
bash ~/.claude/scripts/jjang.sh smartstore all --dry-run
```

---

## 핵심 기술 사항

### API 인증 (bcrypt 서명)
- `client_id + "_" + timestamp` → bcrypt 해시 → base64 인코딩 → OAuth2 토큰 발급
- 토큰 만료 60초 전 자동 재발급

### API 상품 수정 주의점
- **read-modify-write 필수**: PUT 시 누락 필드는 삭제됨
- **seoInfo null 금지**: 기존 태그 사라짐 → 기존값 보존 후 tags만 교체

### Selenium 캡챠 회피
- **방법 1**: Chrome 프로필(`--user-data-dir`)로 기존 로그인 세션 재사용
- **방법 2**: 크롬 디버깅 모드(`--remote-debugging-port=9222`)로 수동 로그인 후 연결
- 봇 감지 회피 옵션: `excludeSwitches`, `disable-blink-features=AutomationControlled`

### Selenium 셀렉터 (사전 DOM 분석 필요)
- 상품정보제공고시 폼의 CSS 셀렉터는 **스마트스토어 실제 접속 후 확정**
- 초기 구현 시 placeholder 셀렉터 → 1차 테스트 후 교정

---

## 에러 처리

| 에러 | 대응 |
|---|---|
| API 인증 실패 (401) | 토큰 재발급 1회 재시도, 실패 시 중단 |
| Rate Limit (429) | 60초 대기 후 최대 3회 재시도 |
| 상품 없음 (404) | SKIP + 로그, 다음 상품 계속 |
| Selenium CAPTCHA | 중단 + 수동 처리 안내 메시지 |
| 요소 미발견 | 스크린샷 저장 + SKIP + 로그 |

---

## 의존성

```
requests>=2.31.0
bcrypt>=4.0.0
pybase64>=1.3.0
openpyxl>=3.1.0
selenium>=4.15.0
webdriver-manager>=4.0.0
python-dotenv>=1.0.0
```

---

## 환경변수 설정

```
NAVER_COMMERCE_CLIENT_ID=발급받은_CLIENT_ID
NAVER_COMMERCE_CLIENT_SECRET=발급받은_CLIENT_SECRET
CHROME_PROFILE_DIR=C:\Users\NO\AppData\Local\Google\Chrome\User Data  (선택)
```

---

## 구현 순서 (8단계)

1. `config.py` + `api/auth.py` — API 키 연결 + 토큰 발급 테스트
2. `api/client.py` + `api/products.py` — 상품 조회 GET 테스트
3. `data/models.py` + `data/excel_reader.py` — 엑셀 파싱
4. `main.py` API 파트 — 주요정보 + 태그 수정 완성
5. Selenium DOM 분석 — 스마트스토어 실제 접속, 셀렉터 확정
6. `selenium_handler/` — 고시 입력 자동화
7. `logger/` — HTML 리포트 생성
8. `jjang.sh` 통합 — CLI 명령 등록

---

## 검증 방법

1. `--dry-run` 모드로 전체 흐름 시뮬레이션 (실제 수정 없음)
2. 테스트용 상품 1개로 API 수정 → 스마트스토어에서 결과 확인
3. 테스트용 상품 1개로 Selenium 고시 입력 → 저장 확인
4. 엑셀 5~10건으로 일괄 실행 → 리포트 확인
5. 실패 건 재시도 동작 확인

---

## 참조 파일 (기존)
- `~/.claude/automation/season-alert.py` — HTML 리포트, JSON 히스토리 패턴 재사용
- `~/.claude/scripts/jjang.sh` — `smartstore` 명령 추가 대상
