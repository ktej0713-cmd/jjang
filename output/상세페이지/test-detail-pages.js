/**
 * 짱베이스볼 상세페이지 Playwright 테스트
 * 10단계 표준 구조 검증 + 스크린샷 캡처
 *
 * 실행: node test-detail-pages.js
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// 테스트할 HTML 파일 목록 (ref_ 제외)
const HTML_DIR = __dirname;
const SCREENSHOT_DIR = path.join(__dirname, 'screenshots');

// 10단계 표준 구조 검증 키워드
// 각 섹션에서 하나 이상 매칭되면 PASS
const SECTIONS = [
  { step: 1, name: '히어로 + 핵심 카피',   keywords: ['hero', 'section-hero', 'sec01', 'sec-hero', 'headline', 'product-title', 'main-title'] },
  { step: 2, name: '필요 상황 (공감)',       keywords: ['필요', '상황', '고민', '이런', '공감', 'situation', 'need', 'sec02'] },
  { step: 3, name: '핵심 스펙 표',          keywords: ['스펙', 'spec', 'table', '규격', '소재', '중량', 'sec03'] },
  { step: 4, name: '체감 설명',             keywords: ['체감', '착용', '사용감', '실사용', '느낌', 'sec04', 'feel'] },
  { step: 5, name: '포지션별 추천',         keywords: ['포지션', '추천', 'position', '사회인', '유소년', '엘리트', 'sec05'] },
  { step: 6, name: '사이즈 가이드',         keywords: ['사이즈', 'size', '치수', '가이드', 'guide', 'sec06'] },
  { step: 7, name: '비교표',               keywords: ['비교', 'compare', '차이', 'vs', 'sec07'] },
  { step: 8, name: 'FAQ',                  keywords: ['faq', 'FAQ', '자주', '질문', 'question', 'sec08'] },
  { step: 9, name: '추천 포인트',           keywords: ['추천', '포인트', 'point', '이유', '장점', 'sec09'] },
  { step: 10, name: '배송/교환/반품 안내',  keywords: ['배송', '교환', '반품', '안내', 'delivery', 'sec10', 'shipping'] },
];

// 스크린샷 폴더 생성
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

// HTML 파일 목록 (ref_ 제외)
const htmlFiles = fs.readdirSync(HTML_DIR)
  .filter(f => f.endsWith('.html') && !f.startsWith('ref_'));

async function testPage(browser, filePath, fileName) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`파일: ${fileName}`);
  console.log('='.repeat(60));

  const page = await browser.newPage();
  // 뷰포트: 860px (네이버 스마트스토어 상세페이지 표준)
  await page.setViewportSize({ width: 860, height: 900 });

  const fileUrl = `file:///${filePath.replace(/\\/g, '/')}`;
  await page.goto(fileUrl, { waitUntil: 'domcontentloaded' });

  // HTML 전체 텍스트 + class/id 속성 추출
  const pageContent = await page.evaluate(() => {
    return document.documentElement.innerHTML.toLowerCase();
  });

  // 10단계 섹션 검증
  const results = [];
  let passCount = 0;

  for (const section of SECTIONS) {
    const found = section.keywords.some(kw => pageContent.includes(kw.toLowerCase()));
    results.push({ ...section, found });
    if (found) passCount++;

    const icon = found ? '✓' : '✗';
    const status = found ? 'PASS' : 'FAIL';
    console.log(`  [${icon}] Step ${section.step}: ${section.name.padEnd(20)} ${status}`);
  }

  const score = `${passCount}/${SECTIONS.length}`;
  const overallPass = passCount >= 7; // 70% 이상 PASS
  console.log(`\n  결과: ${score} 섹션 감지 → ${overallPass ? '✓ PASS' : '✗ FAIL'}`);

  // 전체 페이지 스크린샷
  const baseName = fileName.replace('.html', '');
  const screenshotPath = path.join(SCREENSHOT_DIR, `${baseName}.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`  스크린샷: screenshots/${baseName}.png`);

  // 추가 체크: 제목 태그
  const title = await page.title();
  console.log(`  페이지 제목: ${title || '(없음)'}`);

  // 추가 체크: 이미지 깨진 것 확인
  const brokenImages = await page.evaluate(() => {
    return Array.from(document.images)
      .filter(img => !img.complete || img.naturalWidth === 0)
      .map(img => img.src);
  });
  if (brokenImages.length > 0) {
    console.log(`  깨진 이미지 ${brokenImages.length}개:`);
    brokenImages.slice(0, 3).forEach(src => console.log(`    - ${src.substring(0, 80)}`));
  }

  await page.close();

  return { fileName, score, passCount, overallPass };
}

async function main() {
  if (htmlFiles.length === 0) {
    console.log('테스트할 HTML 파일이 없습니다.');
    return;
  }

  console.log('짱베이스볼 상세페이지 테스트 시작');
  console.log(`대상 파일: ${htmlFiles.length}개`);
  console.log(`저장 위치: ${SCREENSHOT_DIR}`);

  const browser = await chromium.launch({ headless: true });
  const summary = [];

  for (const fileName of htmlFiles) {
    const filePath = path.join(HTML_DIR, fileName);
    try {
      const result = await testPage(browser, filePath, fileName);
      summary.push(result);
    } catch (err) {
      console.error(`  오류 발생: ${err.message}`);
      summary.push({ fileName, score: '0/10', passCount: 0, overallPass: false });
    }
  }

  await browser.close();

  // 최종 요약
  console.log(`\n${'='.repeat(60)}`);
  console.log('최종 요약');
  console.log('='.repeat(60));
  for (const r of summary) {
    const icon = r.overallPass ? '✓' : '✗';
    console.log(`  [${icon}] ${r.fileName.padEnd(45)} ${r.score}`);
  }

  const totalPass = summary.filter(r => r.overallPass).length;
  console.log(`\n전체: ${totalPass}/${summary.length} 파일 PASS`);
  console.log(`스크린샷 폴더: ${SCREENSHOT_DIR}`);
}

main().catch(console.error);
