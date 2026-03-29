"""
일일 브리핑 이메일 자동 발송 스크립트
- Gmail SMTP SSL (포트 465) 사용
- .env 파일에서 계정 정보 로드
- 사용법: python send_briefing.py <html_file_path>
"""

import smtplib
import sys
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

# ── 로깅 설정 ──────────────────────────────────────────
LOG_DIR = Path(__file__).parent.parent / "output" / "daily-briefing"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "send_log.txt",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)

# ── .env 수동 로드 (python-dotenv 없어도 동작) ───────────
def load_env():
    # .env는 보안상 OneDrive 밖 로컬 폴더에서 로드 (각 PC에 별도 생성)
    env_path = Path.home() / ".secrets" / ".env"
    if not env_path.exists():
        raise FileNotFoundError(f".env 파일 없음: {env_path}\nC:\\Users\\<사용자>\\.secrets\\.env 파일을 생성하세요.")
    with open(env_path, encoding="utf-8-sig") as f:  # BOM 자동 처리
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

# ── 이메일 발송 ─────────────────────────────────────────
def send_email(html_content: str, subject: str):
    sender   = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["GMAIL_RECIPIENT"]

    msg = MIMEMultipart("alternative")
    msg["From"]    = sender
    msg["To"]      = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # 재시도 3회
    last_error = None
    for attempt in range(1, 4):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender, password)
                server.send_message(msg)
            logging.info(f"발송 성공 → {recipient} | {subject}")
            print(f"[성공] {recipient} 으로 발송 완료")
            return
        except Exception as e:
            last_error = e
            logging.warning(f"발송 시도 {attempt}/3 실패: {e}")
            if attempt < 3:
                import time; time.sleep(5)

    logging.error(f"발송 최종 실패: {last_error}")
    print(f"[실패] {last_error}", file=sys.stderr)
    sys.exit(1)

# ── 메인 ────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        # 인수 없으면 latest.html 자동 사용
        html_file = LOG_DIR / "latest.html"
    else:
        html_file = Path(sys.argv[1])

    if not html_file.exists():
        print(f"[오류] HTML 파일 없음: {html_file}", file=sys.stderr)
        sys.exit(1)

    html_content = html_file.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"[일일 브리핑] {today} — YouTube / GitHub / Claude Code"

    load_env()
    send_email(html_content, subject)

if __name__ == "__main__":
    main()
