"""
짱베이스볼 스마트스토어 구역별 상세 캡처 및 모바일 재시도 스크립트
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


def open_page(playwright, url, viewport_width=1920, viewport_height=1080, wait_sec=10):
    browser = playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--lang=ko-KR",
        ]
    )
    context = browser.new_context(
        viewport={"width": viewport_width, "height": viewport_height},
        user_agent=DESKTOP_UA,
        locale="ko-KR",
        timezone_id="Asia/Seoul",
        extra_http_headers={
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }
    )
    context.add_init_script(STEALTH_JS)
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(wait_sec)
    return browser, page


def scroll_all(page, viewport_height):
    """전체 페이지 스크롤 (lazy-load 트리거)"""
    scroll_height = page.evaluate("document.body.scrollHeight")
    pos = 0
    while pos < scroll_height:
        page.evaluate(f"window.scrollTo(0, {pos})")
        time.sleep(0.3)
        pos += viewport_height
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(1.5)


def clip_screenshot(page, output_path, clip=None, full_page=False):
    """특정 영역 또는 전체 스크린샷"""
    if clip:
        page.screenshot(path=output_path, clip=clip)
    else:
        page.screenshot(path=output_path, full_page=full_page)
    print(f"  저장: {output_path}")


if __name__ == "__main__":
    with sync_playwright() as p:
        # ── 데스크톱 (1920x1080) ──────────────────────────────
        print("\n[데스크톱] 페이지 로딩...")
        browser, page = open_page(p, URL, 1920, 1080, wait_sec=10)
        scroll_all(page, 1080)

        # 전체 페이지
        clip_screenshot(page, f"{OUTPUT_DIR}/desktop_full.png", full_page=True)
        # ATF (뷰포트 영역만)
        clip_screenshot(page, f"{OUTPUT_DIR}/desktop_atf.png", full_page=False)

        # 헤더 영역 (상단 0~120px)
        clip_screenshot(page, f"{OUTPUT_DIR}/desktop_header.png",
                        clip={"x": 0, "y": 0, "width": 1920, "height": 120})
        # GNB 네비게이션 (120~180px)
        clip_screenshot(page, f"{OUTPUT_DIR}/desktop_gnb.png",
                        clip={"x": 0, "y": 0, "width": 1920, "height": 200})
        # 메인 배너 영역 (200~600px)
        clip_screenshot(page, f"{OUTPUT_DIR}/desktop_banner.png",
                        clip={"x": 0, "y": 200, "width": 1920, "height": 400})

        # 페이지 구조 정보 수집
        info = page.evaluate("""() => {
            const getAll = (sel, prop) => {
                return Array.from(document.querySelectorAll(sel))
                    .slice(0, 20)
                    .map(e => prop === 'src' ? e.src : (prop === 'href' ? e.href : e.innerText.trim()))
                    .filter(t => t && t.length > 0);
            };
            const countEls = (sel) => document.querySelectorAll(sel).length;
            const getBBox = (sel) => {
                const el = document.querySelector(sel);
                if (!el) return null;
                const r = el.getBoundingClientRect();
                return { top: r.top, bottom: r.bottom, height: r.height, width: r.width };
            };

            return {
                title: document.title,
                url: location.href,
                bodyHeight: document.body.scrollHeight,
                imgCount: countEls('img'),
                imgSrcs: getAll('img', 'src'),
                allLinks: getAll('a', null),
                h1: getAll('h1', null),
                h2: getAll('h2', null),
                h3: getAll('h3', null),
            };
        }""")

        print(f"\n[데스크톱 페이지 정보]")
        print(f"  타이틀: {info['title']}")
        print(f"  URL: {info['url']}")
        print(f"  페이지 높이: {info['bodyHeight']}px")
        print(f"  이미지 수: {info['imgCount']}")
        print(f"  H1: {info['h1']}")
        print(f"  H2: {info['h2'][:8]}")
        print(f"  H3: {info['h3'][:8]}")
        print(f"  링크 텍스트: {info['allLinks'][:20]}")
        print(f"  이미지 URL 샘플: {info['imgSrcs'][:8]}")

        browser.close()

        # ── 모바일 (375x812, 데스크톱 UA로 우회) ────────────────
        print("\n[모바일 뷰포트] 페이지 로딩 (데스크톱 UA 사용)...")
        browser, page = open_page(p, URL, 375, 812, wait_sec=10)
        scroll_all(page, 812)

        clip_screenshot(page, f"{OUTPUT_DIR}/mobile_full.png", full_page=True)
        clip_screenshot(page, f"{OUTPUT_DIR}/mobile_atf.png", full_page=False)

        mobile_info = page.evaluate("""() => ({
            url: location.href,
            title: document.title,
            bodyHeight: document.body.scrollHeight,
            bodyWidth: document.body.scrollWidth,
            imgCount: document.querySelectorAll('img').length,
        })""")

        print(f"\n[모바일 뷰포트 정보]")
        print(f"  URL: {mobile_info['url']}")
        print(f"  타이틀: {mobile_info['title']}")
        print(f"  페이지 크기: {mobile_info['bodyWidth']}x{mobile_info['bodyHeight']}px")
        print(f"  이미지 수: {mobile_info['imgCount']}")

        browser.close()

    print("\n=== 모든 캡처 완료 ===")
