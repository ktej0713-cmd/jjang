# 고도몰 재고 현황 자동 이메일 발송

고도몰(Godo Mall) 오픈 API를 통해 특정 상품의 재고를 매일 아침 자동으로 확인하고, Gmail로 재고 현황 리포트를 발송합니다.

## 기능

- 지정한 상품번호 목록의 재고 수량 자동 조회
- 옵션별 재고 상세 표시
- 재고 부족/품절 상품 하이라이트 경고
- HTML 형식의 깔끔한 리포트 이메일
- GitHub Actions로 매일 아침 7시(KST) 자동 실행

## 사전 준비

### 1. 고도몰 API 키 발급

1. [NHN커머스 개발자센터](https://devcenter.nhn-commerce.com/) 회원가입
2. 개발자 등록 후 승인 대기
3. 승인 후 **오픈 API 키 발급 신청** → **제휴사키(partner_key)** 획득
4. 고도몰 SCM 관리자 페이지 → 관리 정책 → 운영자 관리 → **사용자키** 발급

> API 스펙 정의서: https://devcenter.nhn-commerce.com/godomall5/openapi/specDownload

### 2. Gmail 앱 비밀번호 설정

1. Google 계정 → [보안](https://myaccount.google.com/security) → **2단계 인증** 활성화
2. [앱 비밀번호](https://myaccount.google.com/apppasswords) 페이지에서 새 앱 비밀번호 생성
3. 생성된 16자리 비밀번호를 `GMAIL_APP_PASSWORD`로 사용

### 3. GitHub Secrets 등록

리포지토리 → Settings → Secrets and variables → Actions에서 아래 시크릿을 등록:

| 시크릿 이름 | 설명 |
|-------------|------|
| `GODO_PARTNER_KEY` | 고도몰 제휴사키 |
| `GODO_USER_KEY` | 고도몰 사용자키 |
| `GODO_SHOP_URL` | 쇼핑몰 URL (예: `https://yourshop.godomall.com`) |
| `GMAIL_ADDRESS` | 발신 Gmail 주소 |
| `GMAIL_APP_PASSWORD` | Gmail 앱 비밀번호 |
| `RECIPIENT_EMAIL` | 수신자 이메일 (쉼표로 복수 가능) |
| `TARGET_GOODS_NOS` | 모니터링할 상품번호 (쉼표 구분, 예: `1000,1001,1002`) |
| `LOW_STOCK_THRESHOLD` | 재고 부족 기준 수량 (기본값: `10`) |

## 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일 편집하여 실제 값 입력

# 실행
cd src
python main.py
```

> 로컬 실행 시 `.env` 파일의 환경변수를 로드하려면 `export $(cat ../.env | xargs)` 후 실행하세요.

## 수동 실행 (GitHub Actions)

GitHub 리포지토리 → Actions → "Daily Inventory Check" → "Run workflow" 버튼으로 수동 실행 가능합니다.

## API 엔드포인트 수정

고도몰 API의 정확한 엔드포인트 URL은 발급받은 API 스펙 정의서에 따라 다를 수 있습니다.
`src/godo_api.py`의 `get_goods_info()` 메서드에서 엔드포인트 경로를 수정하세요:

```python
data = self._make_request(
    "api/goods/Goods_Search.php",  # ← 실제 엔드포인트로 수정
    params={"goodsNo": goods_no},
)
```

## 프로젝트 구조

```
├── .github/workflows/
│   └── inventory-check.yml    # GitHub Actions (매일 KST 07:00)
├── src/
│   ├── config.py              # 환경변수 설정 관리
│   ├── godo_api.py            # 고도몰 API 클라이언트
│   ├── email_sender.py        # Gmail SMTP 이메일 발송
│   └── main.py                # 메인 실행 스크립트
├── .env.example               # 환경변수 예시
├── requirements.txt           # Python 의존성
└── README.md
```
