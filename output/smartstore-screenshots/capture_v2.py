"""
짱베이스볼 스마트스토어 메인 페이지 스크린샷 캡처 스크립트 v2
- 네이버 봇 차단 우회를 위한 실제 브라우저 헤더 설정
- stealth 모드 적용 (webdriver 속성 숨김)
"""

from playwright.sync_api import sync_playwright
import time

URL = "https://smartstore.naver.com/jjangbaseball"
OUTPUT_DIR = "C:/Users/jj1/.claude/output/smartstore-screenshots"

DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

MOBILE_UA = (
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Mobile Safari/537.36"
)

# webdriver 감지 우회 스크립트
STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
Object.defineProperty(navigator, 'languages', { get: () => ['ko-KR', 'ko', 'en-US'] });
window.chrome = { runtime: {} };
"""

def capture(url, output_path, viewport_width=1920, viewport_height=1080,
            full_page=True, mobile=False, wait_sec=8):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--window-size={},{}".format(viewport_width, viewport_height),
                "--lang=ko-KR",
            ]
        )

        ua = MOBILE_UA if mobile else DESKTOP_UA

        context = browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height},
            user_agent=ua,
            locale="ko-KR",
            timezone_id="Asia/Seoul",
            extra_http_headers={
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "Sec-Ch-Ua-Mobile": "?1" if mobile else "?0",
                "Sec-Ch-Ua-Platform": '"Android"' if mobile else '"Windows"',
            }
        )

        page = context.new_page()

        # webdriver 감지 우회 적용
        page.add_init_script(STEALTH_JS)

        print(f"  접속 중: {url}  (뷰포트: {viewport_width}x{viewport_height}, "
              f"{'모바일' if mobile else '데스크톱'})")

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"  goto 오류 (계속 진행): {e}")

        # 페이지 로딩 대기
        time.sleep(wait_sec)

        # 현재 URL 확인 (리다이렉트/캡차 감지)
        current_url = page.url
        print(f"  현재 URL: {current_url}")

        # 페이지 타이틀 확인
        title = page.title()
        print(f"  페이지 타이틀: {title}")

        # 전체 스크롤 시 lazy-load 이미지 로딩 유도
        if full_page:
            page_height = page.evaluate("document.body.scrollHeight")
            scroll_step = viewport_height // 2
            for y in range(0, page_height, scroll_step):
                page.evaluate(f"window.scrollTo(0, {y})")
                time.sleep(0.3)
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)

        page.screenshot(path=output_path, full_page=full_page)
        print(f"  저장 완료: {output_path}")
        browser.close()

if __name__ == "__main__":
    captures = [
        # (파일명, 너비, 높이, 전체스크롤, 모바일여부, 설명)
        ("desktop_full_v2.png",  1920, 1080, True,  False, "데스크톱 전체"),
        ("desktop_atf_v2.png",   1920, 1080, False, False, "데스크톱 ATF"),
        ("mobile_full_v2.png",   375,  812,  True,  True,  "모바일 전체"),
        ("mobile_atf_v2.png",    375,  812,  False, True,  "모바일 ATF"),
        ("tablet_full_v2.png",   768,  1024, True,  False, "태블릿 전체"),
    ]

    for filename, w, h, full, mob, desc in captures:
        output_path = f"{OUTPUT_DIR}/{filename}"
        print(f"\n[{desc}] 캡처 시작...")
        try:
            capture(URL, output_path, viewport_width=w, viewport_height=h,
                    full_page=full, mobile=mob)
        except Exception as e:
            print(f"  오류: {e}")

    print("\n모든 캡처 완료.")
