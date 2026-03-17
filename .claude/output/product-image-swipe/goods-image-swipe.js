/**
 * 짱베이스볼 - 상품 이미지 스와이프 슬라이더
 * 고도몰5 상품 상세페이지(goods_view)용
 *
 * 기능:
 * - 메인 상품 이미지를 마우스 드래그/터치 스와이프로 전환
 * - 좌우 화살표 버튼
 * - 하단 도트 인디케이터
 * - 썸네일 슬라이더와 자동 동기화
 *
 * 의존성: jQuery 1.x+, Slick Slider (고도몰 기본 포함)
 * 적용 위치: 고도몰 관리자 > 디자인 > 스킨 편집 > goods/goods_view.html 하단
 *            또는 관리자 > 기본설정 > 외부스크립트 등록
 */
(function($) {
  'use strict';

  // DOM 로드 후 실행
  $(document).ready(function() {
    initGoodsImageSwipe();
  });

  function initGoodsImageSwipe() {
    // 1. 썸네일에서 큰 이미지 URL 목록 추출
    var thumbImgs = document.querySelectorAll('.slider_goods_nav img');
    var bigUrls = [];
    thumbImgs.forEach(function(img) {
      bigUrls.push(img.src.replace('/t50_', '/'));
    });

    // 이미지가 1개 이하면 스와이프 불필요
    if (bigUrls.length <= 1) return;

    // 2. 메인 이미지 영역 찾기
    var imgSpan = document.querySelector('.img_photo_big');
    if (!imgSpan) return;

    // 기존 이미지 크기 참조
    var mainImg = document.querySelector('#mainImage img');
    var imgWidth = mainImg ? mainImg.offsetWidth : 708;
    var imgHeight = mainImg ? mainImg.offsetHeight : 708;

    // 3. 기존 내용 교체 — 슬라이더 생성
    imgSpan.innerHTML = '';
    var slider = document.createElement('div');
    slider.id = 'mainImageSlider';
    bigUrls.forEach(function(url, i) {
      var div = document.createElement('div');
      var img = document.createElement('img');
      img.src = url;
      img.alt = '상품 이미지 ' + (i + 1);
      img.style.cssText = 'width:' + imgWidth + 'px;height:' + imgHeight + 'px;display:block;object-fit:contain;';
      div.appendChild(img);
      slider.appendChild(div);
    });
    imgSpan.appendChild(slider);

    // 4. 스타일 삽입
    if (!document.getElementById('swipeSliderCSS')) {
      var css = document.createElement('style');
      css.id = 'swipeSliderCSS';
      css.textContent = [
        /* 컨테이너 */
        '.img_photo_big { display:block !important; width:' + imgWidth + 'px !important; height:' + imgHeight + 'px !important; overflow:hidden !important; position:relative !important; }',
        '#mainImageSlider { width:' + imgWidth + 'px !important; }',
        '#mainImageSlider .slick-list { overflow:hidden !important; }',
        '#mainImageSlider .slick-slide { outline:none; }',
        /* 도트 인디케이터 */
        '#mainImageSlider .slick-dots { position:absolute; bottom:12px; width:100%; text-align:center; padding:0; margin:0; list-style:none; z-index:5; }',
        '#mainImageSlider .slick-dots li { display:inline-block; margin:0 3px; }',
        '#mainImageSlider .slick-dots li button { font-size:0; line-height:0; width:10px; height:10px; padding:0; border:2px solid #fff; border-radius:50%; background:rgba(0,0,0,0.3); cursor:pointer; box-shadow:0 1px 3px rgba(0,0,0,0.3); }',
        '#mainImageSlider .slick-dots li.slick-active button { background:#e53935; border-color:#fff; }',
        /* 화살표 */
        '#mainImageSlider .slick-arrow { position:absolute; top:50%; z-index:10; width:36px; height:36px; border:none; border-radius:50%; background:rgba(0,0,0,0.25); color:#fff; font-size:16px; cursor:pointer; transform:translateY(-50%); transition:background 0.2s; }',
        '#mainImageSlider .slick-arrow:hover { background:rgba(0,0,0,0.5); }',
        '#mainImageSlider .slick-prev { left:10px; }',
        '#mainImageSlider .slick-next { right:10px; }',
        /* 드래그 커서 */
        '#mainImageSlider .slick-slide { cursor:grab; }',
        '#mainImageSlider .slick-slide:active { cursor:grabbing; }'
      ].join('\n');
      document.head.appendChild(css);
    }

    // 5. Slick 슬라이더 초기화
    $('#mainImageSlider').slick({
      dots: true,
      arrows: true,
      infinite: true,
      speed: 300,
      slidesToShow: 1,
      slidesToScroll: 1,
      swipe: true,
      draggable: true,
      touchMove: true,
      touchThreshold: 10,
      prevArrow: '<button type="button" class="slick-prev slick-arrow">\u2039</button>',
      nextArrow: '<button type="button" class="slick-next slick-arrow">\u203A</button>',
      adaptiveHeight: false
    });

    // 6. 메인 슬라이더 ↔ 썸네일 동기화
    var thumbSlides = document.querySelectorAll('.slider_goods_nav .slick-slide');

    // 초기 썸네일 상태 설정
    thumbSlides.forEach(function(s, i) {
      s.style.opacity = (i === 0) ? '1' : '0.5';
      s.style.transition = 'opacity 0.2s';
    });

    // 메인 슬라이더 변경 → 썸네일 이동 + 활성 표시
    $('#mainImageSlider').on('afterChange', function(e, slick, idx) {
      $('.slider_goods_nav').slick('slickGoTo', idx);
      thumbSlides.forEach(function(s, i) {
        s.style.opacity = (i === idx) ? '1' : '0.5';
      });
    });

    // 7. 썸네일 클릭 → 메인 슬라이더 이동 (기존 gd_change_image 대체)
    document.querySelectorAll('.slider_goods_nav .slick-slide a').forEach(function(a, i) {
      a.setAttribute('href', 'javascript:void(0)');
      a.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $('#mainImageSlider').slick('slickGoTo', i);
        return false;
      }, true);
    });
  }

})(jQuery);
