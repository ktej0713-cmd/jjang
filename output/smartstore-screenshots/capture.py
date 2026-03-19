"""
짱베이스볼 스마트스토어 메인 페이지 스크린샷 캡처 스크립트
네이버 봇 탐지 우회: stealth 모드, 실제 브라우저 UA, 충분한 대기
- 데스크톱 (1920x1080) 전체 스크롤 캡처
- 데스크톱 above-the-fold 캡처 (1920x1080 뷰포트 기준)
- 모바일 (375x812) 전체 스크롤 캡처
- 모바일 above-the-fold 캡처
"""

from playwright.sync_api import sync_playwright
import time

URL = "https://smartstore.naver.com/jjang_baseball"
OUTPUT_DIR = "C:/Users/jj1/.claude/output/smartstore-screenshots"

# 봇 탐지 우회를 위한 JavaScript 주입
STEALTH_JS = """
() => {
    // webdriver 속성 제거
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    // 플러그인 배열 조작
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    // 언어 설정
    Object.defineProperty(navigator, 'languages', { get: () => ['ko-KR', 'ko', 'en-US', 'en'] });
    // Chrome 객체 추가
    window.chrome = { runtime: {} };
}
"""

def capture(url, output_path, viewport_width=1920, viewport_height=1080,
            full_page=True, wait_sec=8, is_mobile=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-web-security",
                "--lang=ko-KR",
            ]
        )

        # 모바일/데스크톱 설정 분리
        if is_mobile:
            ua = (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
            )
        else:
            ua = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )

        context = browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height},
            user_agent=ua,
            locale="ko-KR",
            timezone_id="Asia/Seoul",
            extra_http_headers={
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            }
        )

        # 봇 탐지 우회 스크립트 주입
        context.add_init_script(STEALTH_JS)

        page = context.new_page()
        print(f"  접속 중: {url} (뷰포트: {viewport_width}x{viewport_height})")

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"  goto 오류 (계속 진행): {e}")

        # 충분한 대기
        time.sleep(wait_sec)

        # 페이지 상태 확인
        current_url = page.url
        page_title = page.title()
        print(f"  현재 URL: {current_url}")
        print(f"  페이지 타이틀: {page_title}")

        # 봇 탐지 여부 확인
        body_text = page.evaluate("document.body ? document.body.innerText.substring(0, 200) : 'no body'")
        print(f"  페이지 텍스트 미리보기: {body_text[:100]}")

        # 스크롤 (lazy-load 이미지 트리거)
        if full_page:
            scroll_height = page.evaluate("document.body.scrollHeight")
            step = viewport_height
            pos = 0
            while pos < scroll_height:
                page.evaluate(f"window.scrollTo(0, {pos})")
                time.sleep(0.4)
                pos += step
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(2)

        page.screenshot(path=output_path, full_page=full_page)
        print(f"  저장 완료: {output_path}")
        browser.close()


if __name__ == "__main__":
    captures = [
        # (파일명, 너비, 높이, 전체스크롤, 대기초, 모바일여부, 설명)
        ("desktop_full.png",  1920, 1080, True,  10, False, "데스크톱 전체 스크롤"),
        ("desktop_atf.png",   1920, 1080, False, 10, False, "데스크톱 Above-the-fold"),
        ("mobile_full.png",   375,  812,  True,  10, True,  "모바일 전체 스크롤"),
        ("mobile_atf.png",    375,  812,  False, 10, True,  "모바일 Above-the-fold"),
    ]

    for filename, w, h, full, wait, mobile, desc in captures:
        output_path = f"{OUTPUT_DIR}/{filename}"
        print(f"\n[{desc}] 캡처 시작...")
        try:
            capture(URL, output_path,
                    viewport_width=w, viewport_height=h,
                    full_page=full, wait_sec=wait, is_mobile=mobile)
        except Exception as e:
            print(f"  오류 발생: {e}")

    print("\n모든 캡처 완료.")
