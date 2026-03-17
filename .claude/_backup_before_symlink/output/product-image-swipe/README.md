# 상품 이미지 스와이프 슬라이더

## 적용 방법

### 방법 1: 고도몰 관리자 > 외부 스크립트 등록
1. `goods-image-swipe.js` 파일을 서버에 업로드 (예: `/data/skin/js/`)
2. 고도몰 관리자 > 기본설정 > 외부스크립트 등록
3. 상품 상세페이지에 아래 스크립트 태그 추가:
```html
<script src="/data/skin/js/goods-image-swipe.js"></script>
```

### 방법 2: 스킨 파일 직접 편집
1. 고도몰 관리자 > 디자인 > 스킨 편집
2. `goods/goods_view.html` 파일 열기
3. 파일 최하단 `</body>` 또는 `{/literal}` 직전에 삽입:
```html
<script src="/data/skin/js/goods-image-swipe.js"></script>
```

## 기능
- 마우스 드래그 / 터치 스와이프로 이미지 전환
- 좌우 화살표 버튼
- 하단 도트 인디케이터 (빨간색 활성)
- 썸네일 슬라이더 자동 동기화
- 커서: grab ↔ grabbing 전환

## 의존성
- jQuery 1.x+ (고도몰 기본 포함)
- Slick Slider (고도몰 기본 포함)

## 참고
- 이미지 1개 이하인 상품에서는 자동으로 비활성화됩니다
- 기존 확대(zoom) 기능은 비활성화됩니다
