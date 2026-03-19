// 배너 캡처 스크립트 - Playwright 사용
// 2026 시즌 개막전 배너 HTML을 정확한 픽셀 크기로 PNG 저장

const { chromium } = require('playwright');
const path = require('path');

async function captureBanners() {
  const browser = await chromium.launch();

  const outputDir = path.resolve(__dirname);

  // 배너 1: 모바일 (1176 x 790)
  {
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1176, height: 790 });

    const htmlPath = path.join(outputDir, 'banner_mobile_opening.html');
    await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`);

    // 폰트 렌더링 대기
    await page.waitForTimeout(500);

    await page.screenshot({
      path: path.join(outputDir, 'banner_mobile_opening.png'),
      clip: { x: 0, y: 0, width: 1176, height: 790 },
      type: 'png'
    });

    console.log('모바일 배너 저장 완료: banner_mobile_opening.png');
    await page.close();
  }

  // 배너 2: PC (1254 x 484)
  {
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1254, height: 484 });

    const htmlPath = path.join(outputDir, 'banner_pc_opening.html');
    await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`);

    // 폰트 렌더링 대기
    await page.waitForTimeout(500);

    await page.screenshot({
      path: path.join(outputDir, 'banner_pc_opening.png'),
      clip: { x: 0, y: 0, width: 1254, height: 484 },
      type: 'png'
    });

    console.log('PC 배너 저장 완료: banner_pc_opening.png');
    await page.close();
  }

  await browser.close();
  console.log('모든 배너 캡처 완료.');
}

captureBanners().catch(err => {
  console.error('오류 발생:', err);
  process.exit(1);
});
