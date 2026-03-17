/**
 * 짱베이스볼 상세페이지 E2E 테스트
 * @playwright/test 형식 — VSCode에서 ▶ 클릭으로 실행
 */

const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

// 상세페이지 폴더 경로
const HTML_DIR = path.join(__dirname, '..');

// 테스트할 HTML 파일 목록 (ref_ 제외)
const htmlFiles = fs.readdirSync(HTML_DIR)
  .filter(f => f.endsWith('.html') && !f.startsWith('ref_'));

// 10단계 표준 구조 키워드
const SECTIONS = [
  { step: 1, name: '히어로 + 핵심 카피',  keywords: ['hero', 'section-hero', 'sec01', 'sec-hero', 'headline', 'product-title', 'main-title'] },
  { step: 2, name: '필요 상황',          keywords: ['필요', '상황', '고민', '이런', '공감', 'situation', 'need', 'sec02'] },
  { step: 3, name: '핵심 스펙 표',       keywords: ['스펙', 'spec', 'table', '규격', '소재', '중량', 'sec03'] },
  { step: 4, name: '체감 설명',          keywords: ['체감', '착용', '사용감', '실사용', '느낌', 'sec04', 'feel'] },
  { step: 5, name: '포지션별 추천',      keywords: ['포지션', '추천', 'position', '사회인', '유소년', '엘리트', 'sec05'] },
  { step: 6, name: '사이즈 가이드',      keywords: ['사이즈', 'size', '치수', '가이드', 'guide', 'sec06'] },
  { step: 7, name: '비교표',            keywords: ['비교', 'compare', '차이', 'vs', 'sec07'] },
  { step: 8, name: 'FAQ',              keywords: ['faq', 'FAQ', '자주', '질문', '궁금', 'Q&A', '문의', 'sec08'] },
  { step: 9, name: '추천 포인트',        keywords: ['추천', '포인트', 'point', '이유', '장점', 'sec09'] },
  { step: 10, name: '배송/교환/반품',    keywords: ['배송', '교환', '반품', '안내', 'delivery', 'sec10', 'shipping'] },
];

// 파일마다 테스트 생성
for (const fileName of htmlFiles) {
  const filePath = path.join(HTML_DIR, fileName);
  const fileUrl = `file:///${filePath.replace(/\\/g, '/')}`;
  const baseName = fileName.replace('.html', '');

  test.describe(fileName, () => {

    test('페이지 로드 및 제목 확인', async ({ page }) => {
      await page.goto(fileUrl);
      // 페이지가 정상적으로 로드되면 body가 존재
      await expect(page.locator('body')).toBeVisible();
      // 제목 태그 확인 (고도몰 버전은 title 없을 수 있으므로 소프트 체크)
      const title = await page.title();
      if (title) {
        expect(title).toContain('짱베이스볼');
      } else {
        console.log('  title 태그 없음 (고도몰 버전은 정상)');
      }
    });

    test('10단계 구조 검증 (7개 이상 통과)', async ({ page }) => {
      await page.goto(fileUrl);
      const content = await page.evaluate(() =>
        document.documentElement.innerHTML.toLowerCase()
      );

      let passCount = 0;
      for (const section of SECTIONS) {
        const found = section.keywords.some(kw => content.includes(kw.toLowerCase()));
        if (found) passCount++;
        console.log(`  [${found ? '✓' : '✗'}] Step ${section.step}: ${section.name}`);
      }

      console.log(`  결과: ${passCount}/10`);
      // 70% 이상 감지되면 PASS
      expect(passCount).toBeGreaterThanOrEqual(7);
    });

    test('깨진 이미지 없음', async ({ page }) => {
      await page.goto(fileUrl);
      const broken = await page.evaluate(() =>
        Array.from(document.images)
          // 로컬 파일 경로 이미지는 제외 (서버 업로드 전 정상)
          .filter(img => !img.src.startsWith('file://') && (!img.complete || img.naturalWidth === 0))
          .map(img => img.src)
      );
      if (broken.length > 0) console.log('깨진 이미지:', broken);
      expect(broken.length).toBe(0);
    });

    test('전체 페이지 스크린샷', async ({ page }) => {
      await page.goto(fileUrl);
      await page.screenshot({
        path: path.join(__dirname, '..', 'screenshots', `${baseName}.png`),
        fullPage: true,
      });
      // 스크린샷 파일이 생성됐으면 PASS
      const screenshotExists = fs.existsSync(
        path.join(__dirname, '..', 'screenshots', `${baseName}.png`)
      );
      expect(screenshotExists).toBe(true);
    });

  });
}
