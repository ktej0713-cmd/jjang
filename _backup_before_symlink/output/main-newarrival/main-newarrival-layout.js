/**
 * 짱베이스볼 메인 신상품 섹션 레이아웃 변경 v3
 * Slick 슬라이더 재초기화 + 커스텀 타이틀/서브타이틀 삽입
 * (CSS는 별도 파일로 분리)
 *
 * v3: 스와이프 스냅백 버그 수정 (useTransform/useCSS off, dragstart 차단)
 * 설정값은 config 객체에서 관리 (하드코딩 지양)
 */
(function () {
  'use strict';

  // ─── 설정값 (수정 시 이 부분만 변경) ───
  var config = {
    // 슬라이더 노출 상품 수
    slidesToShow: 6,
    slidesToScroll: 1,

    // 자동 슬라이드
    autoplay: true,
    autoplaySpeed: 3000,   // 3초마다 이동
    pauseOnHover: true,    // 마우스 올리면 일시정지
    pauseOnFocus: true,    // 포커스 시 일시정지

    // 반응형 브레이크포인트
    responsive: [
      { breakpoint: 1400, settings: { slidesToShow: 5, slidesToScroll: 1 } },
      { breakpoint: 1024, settings: { slidesToShow: 3, slidesToScroll: 1 } },
      { breakpoint: 768,  settings: { slidesToShow: 2, slidesToScroll: 1 } },
      { breakpoint: 480,  settings: { slidesToShow: 1, slidesToScroll: 1 } }
    ],

    // 대상 선택자
    sectionSelector: '#sec02',
    sliderSelector: '.slide_horizontal_12',

    // 커스텀 타이틀
    titleText: '\uBC29\uAE08 \uC785\uACE0\uB41C \uC2E0\uC0C1\uD488',
    titleLink: '/goods/goods_list.php?cateCd=036',
    subtitleText: '\uB9E4\uC77C \uC0C8\uB85C\uC6B4 \uC57C\uAD6C\uC6A9\uD488\uC774 \uC5C5\uB370\uC774\uD2B8\uB429\uB2C8\uB2E4'
  };

  // ─── 커스텀 타이틀 + 서브타이틀 삽입 ───
  function insertTitle() {
    var section = document.querySelector(config.sectionSelector);
    if (!section || section.querySelector('.jjang-newarrival-title')) return;

    // 타이틀 (링크 포함)
    var title = document.createElement('div');
    title.className = 'jjang-newarrival-title';

    if (config.titleLink) {
      var link = document.createElement('a');
      link.href = config.titleLink;
      link.textContent = config.titleText;
      title.appendChild(link);
    } else {
      title.textContent = config.titleText;
    }

    section.insertBefore(title, section.firstChild);

    // 서브타이틀
    var subtitle = document.createElement('div');
    subtitle.className = 'jjang-newarrival-subtitle';
    subtitle.textContent = config.subtitleText;
    title.insertAdjacentElement('afterend', subtitle);
  }

  // ─── Slick 재초기화 ───
  function reinitSlider() {
    var $slider = $(config.sliderSelector);
    if (!$slider.length) return;

    // 기존 Slick 해제
    if ($slider.hasClass('slick-initialized')) {
      $slider.slick('unslick');
    }

    // 이미지/링크 네이티브 드래그 차단 (스와이프 스냅백 방지)
    $slider[0].addEventListener('dragstart', function (e) {
      e.preventDefault();
    });

    // 새 설정으로 초기화
    $slider.slick({
      slidesToShow: config.slidesToShow,
      slidesToScroll: config.slidesToScroll,
      infinite: true,
      arrows: true,
      dots: false,
      autoplay: config.autoplay,
      autoplaySpeed: config.autoplaySpeed,
      pauseOnHover: config.pauseOnHover,
      pauseOnFocus: config.pauseOnFocus,
      swipe: true,
      swipeToSlide: true,
      draggable: true,
      touchMove: true,
      touchThreshold: 3,
      waitForAnimate: false,
      useTransform: false,
      useCSS: false,
      speed: 300,
      responsive: config.responsive
    });
  }

  // DOM 준비 후 실행
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      insertTitle();
      setTimeout(reinitSlider, 100);
    });
  } else {
    insertTitle();
    setTimeout(reinitSlider, 100);
  }
})();
