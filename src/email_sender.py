import logging
import smtplib
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

KST = timezone(timedelta(hours=9))


def build_html_body(stock_items: list[dict], threshold: int) -> str:
    """재고 현황을 HTML 테이블로 변환"""
    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M")

    low_stock_items = [
        item for item in stock_items
        if not item.get("error") and 0 <= item["stock_qty"] <= threshold
    ]
    out_of_stock = [
        item for item in stock_items
        if not item.get("error") and item["stock_qty"] == 0
    ]

    # 요약 배너
    summary_color = "#4CAF50"  # 초록 (정상)
    summary_text = "모든 상품 재고 정상"
    if out_of_stock:
        summary_color = "#f44336"  # 빨강
        summary_text = f"품절 {len(out_of_stock)}건 / 부족 {len(low_stock_items)}건"
    elif low_stock_items:
        summary_color = "#FF9800"  # 주황
        summary_text = f"재고 부족 {len(low_stock_items)}건"

    rows = ""
    for item in stock_items:
        qty = item["stock_qty"]

        if item.get("error"):
            status = "조회 실패"
            row_style = "background-color: #eeeeee;"
            status_style = "color: #999;"
        elif qty == 0:
            status = "품절"
            row_style = "background-color: #ffebee;"
            status_style = "color: #f44336; font-weight: bold;"
        elif qty <= threshold:
            status = "부족"
            row_style = "background-color: #fff3e0;"
            status_style = "color: #FF9800; font-weight: bold;"
        else:
            status = "정상"
            row_style = ""
            status_style = "color: #4CAF50;"

        # 옵션별 재고 상세
        option_detail = ""
        if item.get("options"):
            option_lines = []
            for opt in item["options"]:
                opt_qty = opt["stock_qty"]
                opt_color = "#f44336" if opt_qty == 0 else (
                    "#FF9800" if opt_qty <= threshold else "#333"
                )
                opt_name = opt["option_name"] or "-"
                option_lines.append(
                    f'<span style="color:{opt_color}">{opt_name}: {opt_qty}개</span>'
                )
            option_detail = "<br>".join(option_lines)

        qty_display = f"{qty}개" if qty >= 0 else "-"

        rows += f"""
        <tr style="{row_style}">
            <td style="padding: 10px; border: 1px solid #ddd;">{item['goods_no']}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{item['goods_name']}</td>
            <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{qty_display}</td>
            <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">
                <span style="{status_style}">{status}</span>
            </td>
            <td style="padding: 10px; border: 1px solid #ddd; font-size: 12px;">{option_detail}</td>
        </tr>"""

    html = f"""
    <html>
    <body style="font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; margin: 0; padding: 20px; background: #f5f5f5;">
        <div style="max-width: 800px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <!-- 헤더 -->
            <div style="background: {summary_color}; color: white; padding: 20px; text-align: center;">
                <h2 style="margin: 0;">재고 현황 리포트</h2>
                <p style="margin: 5px 0 0; opacity: 0.9;">{now} 기준</p>
            </div>

            <!-- 요약 -->
            <div style="padding: 15px 20px; background: #fafafa; border-bottom: 1px solid #eee;">
                <strong>요약:</strong> {summary_text}
                &nbsp;|&nbsp; 전체 {len(stock_items)}개 상품 조회
                (부족 기준: {threshold}개 이하)
            </div>

            <!-- 테이블 -->
            <div style="padding: 20px;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #f0f0f0;">
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">상품번호</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">상품명</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: center;">재고</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: center;">상태</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">옵션별 재고</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def send_inventory_email(
    gmail_address: str,
    gmail_app_password: str,
    recipients: list[str],
    stock_items: list[dict],
    threshold: int,
) -> None:
    """재고 현황 이메일 발송

    Args:
        gmail_address: 발신 Gmail 주소
        gmail_app_password: Gmail 앱 비밀번호
        recipients: 수신자 이메일 목록
        stock_items: 재고 정보 리스트
        threshold: 재고 부족 기준 수량
    """
    now = datetime.now(KST).strftime("%Y-%m-%d")

    low_count = sum(
        1 for item in stock_items
        if not item.get("error") and 0 <= item["stock_qty"] <= threshold
    )

    subject = f"[재고 현황] {now}"
    if low_count > 0:
        subject += f" - 재고 부족 {low_count}건 주의"

    html_body = build_html_body(stock_items, threshold)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_address
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    logger.info("이메일 발송 중: %s -> %s", gmail_address, recipients)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail_address, gmail_app_password)
        server.sendmail(gmail_address, recipients, msg.as_string())

    logger.info("이메일 발송 완료")


def save_html_preview(
    stock_items: list[dict],
    threshold: int,
    output_dir: str = "output",
) -> str:
    """이메일 HTML을 파일로 저장 (dry-run 미리보기용)

    Returns:
        저장된 파일 경로
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    now = datetime.now(KST).strftime("%Y-%m-%d")
    filename = f"inventory_report_{now}.html"
    filepath = os.path.join(output_dir, filename)

    html = build_html_body(stock_items, threshold)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info("HTML 미리보기 저장: %s", filepath)
    return filepath
