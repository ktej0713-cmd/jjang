"""
짱베이스볼 스마트스토어 구역별 추가 클립 캡처
- 뷰포트 기준 클립 (full_page=False 상태에서 스크롤 후 캡처)
"""

from playwright.sync_api import sync_playwright
import time

URL = "https://smartstore.naver.com/jjang_baseball"
OUTPUT_DIR = "C:/Users/jj1/.claude/output/smartstore-screenshots"

STEALTH_JS = """
() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['ko-KR', 'ko', 'en-US'] });
    window.chrome = { runtime: {} };
}
"""

DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def open_page(playwright, url, w, h, wait_sec=8):
    browser = playwright.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--lang=ko-KR"]
    )
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        user_agent=DESKTOP_UA,
        locale="ko-KR",
        timezone_id="Asia/Seoul",
        extra_http_headers={"Accept-Language": "ko-KR,ko;q=0.9"}
    )
    ctx.add_init_script(STEALTH_JS)
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(wait_sec)
    # 전체 스크롤 (lazy-load)
    sh = page.evaluate("document.body.scrollHeight")
    pos = 0
    while pos < sh:
        page.evaluate(f"window.scrollTo(0, {pos})")
        time.sleep(0.3)
        pos += h
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(1.5)
    return browser, page


def scroll_and_capture(page, scroll_y, output_path):
    """특정 Y 위치로 스크롤 후 뷰포트 캡처"""
    page.evaluate(f"window.scrollTo(0, {scroll_y})")
    time.sleep(0.8)
    page.screenshot(path=output_path, full_page=False)
    print(f"  저장: {output_path} (scrollY={scroll_y})")


if __name__ == "__main__":
    with sync_playwright() as p:
        # ── 데스크톱 추가 구역 ──────────────────────────────
        print("\n[데스크톱] 추가 구역 캡처...")
        browser, page = open_page(p, URL, 1920, 1080)

        total_h = page.evaluate("document.body.scrollHeight")
        print(f"  전체 페이지 높이: {total_h}px")

        # 배너 아래 상품 영역 (스크롤 600px)
        scroll_and_capture(page, 600, f"{OUTPUT_DIR}/desktop_mid.png")
        # 중간 지점
        scroll_and_capture(page, total_h // 2, f"{OUTPUT_DIR}/desktop_scroll_mid.png")
        # 하단 (마지막 1080px)
        scroll_and_capture(page, max(0, total_h - 1080), f"{OUTPUT_DIR}/desktop_bottom.png")

        # 카테고리 메뉴 정보 수집
        nav_info = page.evaluate("""() => {
            const allA = document.querySelectorAll('a');
            return Array.from(allA)
                .map(e => ({ text: e.innerText.trim(), href: e.href }))
                .filter(o => o.text && o.text.length < 20 && o.text.length > 0)
                .slice(0, 50);
        }""")
        print(f"\n  네비게이션 링크:")
        for item in nav_info:
            print(f"    [{item['text']}]  {item['href'][:70]}")

        # 이미지 목록
        imgs = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('img'))
                .map(e => ({ src: e.src, alt: e.alt, w: e.naturalWidth, h: e.naturalHeight }))
                .filter(i => i.src && !i.src.startsWith('data:'));
        }""")
        print(f"\n  이미지 목록 ({len(imgs)}개):")
        for img in imgs:
            print(f"    alt='{img['alt']}' ({img['w']}x{img['h']}) {img['src'][:80]}")

        browser.close()

        # ── 모바일 375px 추가 구역 ──────────────────────────
        print("\n[모바일] 추가 구역 캡처...")
        browser, page = open_page(p, URL, 375, 812)

        total_h_m = page.evaluate("document.body.scrollHeight")
        print(f"  전체 페이지 높이: {total_h_m}px")

        # 배너 구역 (스크롤 300)
        scroll_and_capture(page, 300, f"{OUTPUT_DIR}/mobile_banner.png")
        # 상품 목록 (스크롤 800)
        scroll_and_capture(page, 800, f"{OUTPUT_DIR}/mobile_products.png")
        # 하단
        scroll_and_capture(page, max(0, total_h_m - 812), f"{OUTPUT_DIR}/mobile_bottom.png")

        # 모바일 링크 텍스트
        mob_links = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('a'))
                .map(e => e.innerText.trim())
                .filter(t => t && t.length > 0 && t.length < 25)
                .slice(0, 30);
        }""")
        print(f"\n  모바일 링크 텍스트: {mob_links}")

        browser.close()

    print("\n=== 구역별 캡처 완료 ===")
