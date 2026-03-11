// @playwright/test 설정 파일
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  // 스크린샷 저장 위치
  outputDir: './screenshots',
  // 테스트 실패 시 스크린샷 자동 저장
  use: {
    viewport: { width: 860, height: 900 },
    screenshot: 'on',
    // 로컬 HTML 파일 기준 경로
    baseURL: 'file:///C:/Users/NO/.claude/output/상세페이지/',
  },
  // HTML 리포트 생성
  reporter: [['list'], ['html', { outputFolder: 'playwright-report', open: 'never' }]],
});
