# 고도몰5 치환코드 실무 레퍼런스

> 스킨 개발 시 참조하는 치환코드 목록
> 출처: 고도몰 devcenter-help + 실무 정리
> 최종 업데이트: 2026-03-12

---

## 기본 문법

| 형식 | 설명 | 예시 |
|------|------|------|
| `{=변수명}` | 변수 출력 | `{=gMall.mallNm}` |
| `{=함수명(인자)}` | 함수 실행 결과 출력 | `{=gd_is_login()}` |
| `<!--{? 조건 }-->` | 조건문 시작 | `<!--{? gd_is_login() }-->` |
| `<!--{/}-->` | 조건/반복 블록 종료 | |
| `<!--{@ 배열 as 아이템 }-->` | 반복문(foreach) | `<!--{@ goodsList as goods }-->` |
| `{=...키명}` | 반복문 내 현재 아이템 키 접근 | `{=...goodsNm}` |
| `{ # header }` | 레이아웃 블록 삽입 | `{ # footer }` |
| `{=includeWidget(...)}` | 위젯 삽입 | 아래 예시 참조 |

> **주의**: `<script>` 태그 내부에서는 치환코드 동작 안 함. JS에서 데이터 필요 시 SDK 활용.

---

## 쇼핑몰 정보 — gMall

| 치환코드 | 설명 |
|---------|------|
| `{=gMall.mallNm}` | 쇼핑몰명 |
| `{=gMall.mallTitle}` | 쇼핑몰 타이틀 |
| `{=gMall.mallDomain}` | 쇼핑몰 도메인 |
| `{=gMall.companyNm}` | 상호(회사명) |
| `{=gMall.businessNo}` | 사업자등록번호 |
| `{=gMall.ceoNm}` | 대표자명 |
| `{=gMall.email}` | 대표 이메일 |
| `{=gMall.phone}` | 대표 전화번호 |
| `{=gMall.centerPhone}` | 고객센터 전화번호 |
| `{=gMall.centerEmail}` | 고객센터 이메일 |
| `{=gMall.mallFavicon}` | 파비콘 경로 |

---

## 로그인 회원 정보 — gSess

| 치환코드 | 설명 |
|---------|------|
| `{=gSess.memNo}` | 회원 일련번호 |
| `{=gSess.memId}` | 회원 아이디 |
| `{=gSess.memNm}` | 회원 이름 |
| `{=gSess.nickNm}` | 닉네임 |
| `{=gSess.groupSno}` | 회원 그룹 번호 |
| `{=gSess.groupNm}` | 회원 그룹명 |
| `{=gSess.cellPhone}` | 휴대폰 번호 |
| `{=gSess.adultFl}` | 성인인증 여부 |

로그인 여부 조건문:
```html
<!--{? gd_is_login() }-->
  <p>안녕하세요, {=gSess.memNm}님</p>
<!--{/}-->
```

---

## 상품 상세 페이지 — goodsView

| 치환코드 | 설명 |
|---------|------|
| `{=goodsView['goodsNo']}` | 상품 번호 |
| `{=goodsView['goodsNm']}` | 상품명 |
| `{=goodsView['goodsPrice']}` | 판매가 |
| `{=goodsView['fixedPrice']}` | 정가(소비자가) |
| `{=goodsView['cateCd']}` | 카테고리 코드 |
| `{=goodsView['shortDescription']}` | 간략 설명 |
| `{=goodsView['brandNm']}` | 브랜드명 |
| `{=goodsView['makerNm']}` | 제조사명 |
| `{=goodsView['originNm']}` | 원산지 |
| `{=goodsView['goodsCd']}` | 상품 코드 |
| `{=goodsView['orderPossible']}` | 주문 가능 여부 (y/n) |
| `{=goodsView['goodsDescription']}` | 상세 설명 (HTML 포함) |

null 안전 처리:
```html
{=gd_isset(goodsView['goodsPrice'],0)}
```

---

## 상품 목록 — goodsList 반복문

```html
<!--{@ goodsList as goods }-->
  <div class="goods-item">
    <a href="/goods/goods_view.php?goodsNo={=...goodsNo}">
      <img src="{=...listImage}" alt="{=...goodsNm}">
      <p class="goods-name">{=...goodsNm}</p>
      <p class="goods-price">{=gd_money_format(...price['goodsPrice'])}원</p>
    </a>
  </div>
<!--{/}-->
```

주요 반복문 내 변수:
| 변수 | 설명 |
|------|------|
| `{=...goodsNo}` | 상품 번호 |
| `{=...goodsNm}` | 상품명 |
| `{=...price['goodsPrice']}` | 판매가 |
| `{=...price['fixedPrice']}` | 정가 |
| `{=...listImage}` | 리스트 이미지 URL |
| `{=...goodsCnt}` | 재고 수량 |
| `{=...brandNm}` | 브랜드명 |

---

## 주문 정보 — orderInfo

| 치환코드 | 설명 |
|---------|------|
| `{=orderInfo.orderNo}` | 주문 번호 |
| `{=orderInfo.settlePrice}` | 결제 금액 |
| `{=orderInfo.totalDeliveryCharge}` | 총 배송비 |
| `{=orderInfo.firstSaleFl}` | 첫 구매 여부 |

주문 상품 반복:
```html
<!--{@ orderInfo.goods as item }-->
  {=...goodsNm} / {=...goodsCnt}개 / {=gd_money_format(...goodsPrice)}원
<!--{/}-->
```

---

## 장바구니 — cartInfo

| 치환코드 | 설명 |
|---------|------|
| `{=goodsTotalCnt}` | 장바구니 총 상품 수 |
| `{=cartInfo.value_.value_.goodsNo}` | 상품 번호 |
| `{=cartInfo.value_.value_.goodsNm}` | 상품명 |
| `{=cartInfo.value_.value_.price['goodsPrice']}` | 가격 |
| `{=cartInfo.value_.value_.goodsCnt}` | 수량 |

---

## 레이아웃 블록

| 치환코드 | 설명 |
|---------|------|
| `{ # header }` | 상단 레이아웃 |
| `{ # footer }` | 하단 레이아웃 |
| `{ # header_inc }` | 상단 디자인 인클루드 |
| `{ # footer_inc }` | 하단 디자인 인클루드 |

---

## 위젯 삽입

```html
<!-- 슬라이드 배너 -->
{=includeWidget('proc/_slider_banner.html','bannerCode','00000')}

<!-- 메인 상품 진열 -->
{=includeWidget('goods/_goods_display_main.html','sno','0')}
```

---

## 주요 내장 함수 (gd_ 접두어)

| 함수 | 설명 | 사용 예 |
|------|------|--------|
| `gd_is_login()` | 로그인 여부 | `<!--{? gd_is_login() }-->` |
| `gd_isset(변수, 기본값)` | null 안전 처리 | `{=gd_isset(goodsView['goodsPrice'],0)}` |
| `gd_money_format(금액)` | 금액 포맷팅 (쉼표) | `{=gd_money_format(goodsView['goodsPrice'])}` |
| `gd_html_cut(str, len)` | 문자열 자르기 | `{=gd_html_cut(goodsView['shortDescription'], 100)}` |
| `gd_htmlspecialchars(str)` | HTML 특수문자 이스케이프 | XSS 방지 시 사용 |
| `gd_date_format(date)` | 날짜 포맷 변환 | |
| `gd_currency_string()` | 통화 문자열 | |
| `gd_is_plus_shop()` | 플러스샵 여부 | |
| `gd_code()` | 코드 처리 | |
| `gd_select_box()` | 셀렉트 박스 생성 | |

---

## 템플릿 내 사용 가능한 PHP 함수

| 카테고리 | 함수 목록 |
|---------|---------|
| 문자열 | `substr`, `str_replace`, `nl2br`, `strlen`, `urlencode` |
| 배열 | `count`, `is_array`, `in_array`, `implode`, `explode`, `array_keys` |
| 타입 | `floatval`, `intval`, `empty`, `isset` |
| 날짜 | `date`, `time`, `strtotime` |
| 수학 | `ceil`, `floor`, `max`, `min`, `round` |
| JSON | `json_encode`, `json_decode` |
| 기타 | `number_format` |

---

## 조건문 패턴 예시

```html
<!-- 로그인/비로그인 분기 -->
<!--{? gd_is_login() }-->
  <span>회원 전용 가격: {=gd_money_format(goodsView['goodsPrice'])}원</span>
<!--{:}-->
  <a href="/member/login.php">로그인 후 확인</a>
<!--{/}-->

<!-- 재고 있음/없음 분기 -->
<!--{? goodsView['orderPossible'] == 'y' }-->
  <button>구매하기</button>
<!--{:}-->
  <button disabled>품절</button>
<!--{/}-->

<!-- null 체크 -->
<!--{? isset(displayBox) === true }-->
  <div>{=displayBox}</div>
<!--{/}-->
```

---

## 자주 쓰는 스킨 파일 경로

```
data/skin/front/[스킨명]/
  ├── layout/
  │   ├── header.html          ← 상단 레이아웃
  │   └── footer.html          ← 하단 레이아웃
  ├── goods/
  │   ├── goods_view.html      ← 상품 상세
  │   ├── goods_list.html      ← 상품 목록
  │   └── goods_search.html    ← 검색 결과
  ├── order/
  │   ├── cart.html            ← 장바구니
  │   └── order.html           ← 주문서
  ├── member/
  │   ├── login.html           ← 로그인
  │   └── join.html            ← 회원가입
  └── main/
      └── main.html            ← 메인 페이지
```

---

## 관리자 커스텀 컨트롤러 예시 (module/ 폴더)

```php
// 기존 컨트롤러 확장 예시
// module/Controller/Front/Goods/GoodsViewAllController.php

namespace Controller\Front\Goods;

class GoodsViewAllController extends \Bundle\Controller\Front\Goods\GoodsViewAllController
{
    public function index()
    {
        try {
            parent::index(); // 기존 기능 유지 필수
            // 추가 데이터 주입
            $this->setData('customData', '짱베이스볼 전용 데이터');
        } catch (\Exception $e) {
            throw $e;
        }
    }
}
```

스킨에서 사용:
```html
<!--{? isset(customData) === true }-->
  <div>{=customData}</div>
<!--{/}-->
```
