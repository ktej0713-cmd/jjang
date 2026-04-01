# -*- coding: utf-8 -*-
"""
짱베이스볼 야구바지 재고 자동 모니터링
Windows 예약 작업(schtasks)으로 매일 오전 8시 실행

사용법:
  python stock-check.py          # 전체 조회 + 메일 발송
  python stock-check.py --nomail # 메일 없이 JSON만 저장
  python stock-check.py --test   # 테스트 (1개 상품만 조회)
"""

import json
import os
import sys
import logging
import smtplib
import base64
import xml.etree.ElementTree as ET
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 패키지 필요: pip install requests")
    sys.exit(1)

# 고도몰5 Open API 엔드포인트
GODOMALL_API_URL = "https://openhub.godo.co.kr/godomall5/goods/Goods_Search.php"

# === 경로 설정 ===
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR.parent / "config" / "stock-monitor.json"
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
LOG_DIR = SCRIPT_DIR / "logs"

# 디렉토리 생성
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# === 로깅 설정 ===
log_file = LOG_DIR / f"stock-check-{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


def load_config():
    """설정 파일 로드"""
    if not CONFIG_PATH.exists():
        log.error(f"설정 파일 없음: {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 필수 키 검증
    partner_key = config.get("godomall", {}).get("partner_key", "")
    if not partner_key or partner_key == "여기에_파트너키_입력":
        log.error("고도몰 partner_key가 설정되지 않았습니다")
        sys.exit(1)

    return config


def fetch_stock_api(config):
    """고도몰5 Open API (openhub.godo.co.kr)로 상품별 옵션/재고 조회

    API: POST https://openhub.godo.co.kr/godomall5/goods/Goods_Search.php
    인증: partner_key + key (사용자키)
    응답: XML (goods_data > optionData > stockCnt)
    """
    partner_key = config["godomall"]["partner_key"]
    secret_key = config["godomall"]["secret_key"]
    products = config["monitor_products"]

    # 고유 goodsNo만 추출 (중복 제거 - 같은 goodsNo에 다른 옵션인 경우)
    unique_goods = {}
    for prod in products:
        gno = prod["goodsNo"]
        if gno not in unique_goods:
            unique_goods[gno] = prod

    results = []
    session = requests.Session()

    for gno, prod in unique_goods.items():
        log.info(f"조회중: {prod['name']} (goodsNo: {gno})")

        try:
            resp = session.post(
                GODOMALL_API_URL,
                data={"partner_key": partner_key, "key": secret_key, "goodsNo": gno},
                timeout=15
            )

            if resp.status_code != 200:
                log.error(f"  -> API HTTP {resp.status_code}")
                continue

            stock_info = parse_api_xml(resp.text, prod)
            if stock_info:
                results.append(stock_info)
                log.info(f"  -> API 성공: {len(stock_info['sizes'])}개 옵션, 총 재고 {stock_info['total']}")
            else:
                log.error(f"  -> XML 파싱 실패")

        except requests.RequestException as e:
            log.error(f"  -> API 요청 실패: {e}")

    return results


def parse_api_xml(xml_text, prod):
    """고도몰5 Open API XML 응답에서 옵션별 재고 추출

    XML 구조:
    <data>
      <header><code>000</code><msg>성공</msg></header>
      <return>
        <goods_data>
          <goodsNo>15304</goodsNo>
          <totalStock>58</totalStock>
          <optionData>
            <sno>1896</sno>
            <optionValue1>28</optionValue1>
            <stockCnt>18</stockCnt>
          </optionData>
          ...
        </goods_data>
      </return>
    </data>
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        log.error(f"  -> XML 파싱 에러: {e}")
        return None

    # 응답 코드 확인
    code = root.findtext(".//header/code", "")
    if code != "000":
        msg = root.findtext(".//header/msg", "")
        log.error(f"  -> API 에러: code={code}, msg={msg}")
        return None

    # 상품 데이터
    goods = root.find(".//goods_data")
    if goods is None:
        return None

    goods_no = goods.findtext("goodsNo", prod["goodsNo"])
    goods_name = goods.findtext("goodsNm", prod["name"])
    total_stock_api = goods.findtext("totalStock", "0")

    # 옵션별 재고
    sizes = {}
    for opt in goods.findall("optionData"):
        opt_val = opt.findtext("optionValue1", "")
        stock_cnt = int(opt.findtext("stockCnt", "0"))
        if opt_val:
            sizes[opt_val] = stock_cnt

    # 옵션 없는 단일 상품
    if not sizes and total_stock_api:
        sizes["단일"] = int(total_stock_api)

    total = sum(sizes.values())
    return {
        "goodsNo": goods_no,
        "name": prod["name"],
        "sizes": sizes,
        "total": total
    }


def analyze_stock(results, config):
    """재고 분석 - 품절/부족/정상 판정"""
    threshold = config.get("alert_threshold_default", 5)
    product_thresholds = {
        p["goodsNo"]: p.get("alert_threshold", threshold)
        for p in config["monitor_products"]
    }

    total_stock = 0
    out_of_stock = []   # 품절 옵션
    low_stock = []      # 부족 옵션
    normal_count = 0

    for prod in results:
        for size, qty in prod["sizes"].items():
            total_stock += max(qty, 0)
            prod_threshold = product_thresholds.get(prod["goodsNo"], threshold)

            if qty == 0:
                out_of_stock.append({
                    "name": prod["name"],
                    "goodsNo": prod["goodsNo"],
                    "size": size,
                    "qty": qty
                })
            elif 0 < qty <= prod_threshold:
                low_stock.append({
                    "name": prod["name"],
                    "goodsNo": prod["goodsNo"],
                    "size": size,
                    "qty": qty
                })
            else:
                normal_count += 1

    return {
        "total_products": len(results),
        "total_stock": total_stock,
        "out_of_stock": out_of_stock,
        "low_stock": low_stock,
        "normal_count": normal_count,
        "out_of_stock_count": len(out_of_stock),
        "low_stock_count": len(low_stock)
    }


def build_html_report(results, analysis, timestamp):
    """스크린샷과 동일한 형태의 HTML 메일 본문 생성"""
    oos = analysis["out_of_stock_count"]
    low = analysis["low_stock_count"]
    total = analysis["total_stock"]
    total_prods = analysis["total_products"]

    # 품절 사이즈 뱃지 HTML
    oos_badges = ""
    for item in analysis["out_of_stock"]:
        # 상품명에서 컬러 부분만 추출
        name = item["name"]
        # "짱베이스볼 야구바지 슬림핏 유니폼바지" 이후 부분 추출
        short = name.replace("짱베이스볼 야구바지 슬림핏 유니폼바지 ", "").replace("짱베이스볼 야구바지 슬림핏 누빔 스판 야구 유니폼 팬츠 ", "")
        oos_badges += (
            f'<span style="display:inline-block;padding:6px 14px;margin:4px;'
            f'border:1px solid #ddd;border-radius:20px;font-size:13px;'
            f'color:#555;">{short} {item["size"]}</span>\n'
        )

    # 부족 사이즈 뱃지 HTML
    low_badges = ""
    for item in analysis["low_stock"]:
        name = item["name"]
        short = name.replace("짱베이스볼 야구바지 슬림핏 유니폼바지 ", "").replace("짱베이스볼 야구바지 슬림핏 누빔 스판 야구 유니폼 팬츠 ", "")
        low_badges += (
            f'<span style="display:inline-block;padding:6px 14px;margin:4px;'
            f'border:1px solid #ddd;border-radius:20px;font-size:13px;'
            f'color:#555;">{short} {item["size"]} ({item["qty"]})</span>\n'
        )

    # 전체 상품별 재고 테이블
    product_rows = ""
    for prod in results:
        sizes_sorted = sorted(prod["sizes"].items(), key=lambda x: x[0])
        for size, qty in sizes_sorted:
            status_color = "#C62828" if qty == 0 else "#E65100" if qty <= 5 else "#222"
            status_text = "품절" if qty == 0 else f"부족({qty})" if qty <= 5 else str(qty)
            product_rows += (
                f'<tr style="border-bottom:1px solid #eee;">'
                f'<td style="padding:8px 12px;font-size:13px;">{prod["goodsNo"]}</td>'
                f'<td style="padding:8px 12px;font-size:13px;">{prod["name"]}</td>'
                f'<td style="padding:8px 12px;font-size:13px;text-align:center;">{size}</td>'
                f'<td style="padding:8px 12px;font-size:13px;text-align:center;color:{status_color};font-weight:600;">{status_text}</td>'
                f'</tr>\n'
            )

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head><body style="margin:0;padding:0;background:#f5f5f5;">
<div style="max-width:700px;margin:20px auto;background:#fff;font-family:'Noto Sans KR',-apple-system,sans-serif;">

  <!-- 헤더 -->
  <div style="padding:28px 32px;border-left:4px solid #C62828;">
    <div style="font-size:22px;font-weight:800;color:#1B2A4A;">짱베이스볼 야구바지 재고 현황</div>
    <div style="font-size:13px;color:#888;margin-top:6px;">
      {timestamp} | 고도몰 Open API 실시간 | {total_prods}개 상품
    </div>
  </div>

  <!-- 요약 카드 -->
  <table style="width:100%;border-collapse:collapse;margin:0;">
    <tr>
      <td style="width:20%;padding:16px;text-align:center;background:#f8f9fa;border:1px solid #eee;">
        <div style="font-size:11px;color:#888;font-weight:600;">전체 재고</div>
        <div style="font-size:22px;font-weight:800;color:#1B2A4A;margin-top:4px;">{total:,}개</div>
      </td>
      <td style="width:20%;padding:16px;text-align:center;background:#f8f9fa;border:1px solid #eee;">
        <div style="font-size:11px;color:#888;font-weight:600;">품절</div>
        <div style="font-size:22px;font-weight:800;color:#C62828;margin-top:4px;">{oos}건</div>
      </td>
      <td style="width:20%;padding:16px;text-align:center;background:#f8f9fa;border:1px solid #eee;">
        <div style="font-size:11px;color:#888;font-weight:600;">부족</div>
        <div style="font-size:22px;font-weight:800;color:#E65100;margin-top:4px;">{low}건</div>
      </td>
    </tr>
  </table>

  <!-- 품절 사이즈 -->
  {"" if oos == 0 else f'''
  <div style="padding:24px 32px;">
    <div style="font-size:16px;font-weight:700;color:#C62828;margin-bottom:12px;">품절 사이즈 ({oos}건)</div>
    <div>{oos_badges}</div>
  </div>'''}

  <!-- 부족 사이즈 -->
  {"" if low == 0 else f'''
  <div style="padding:0 32px 24px;">
    <div style="font-size:16px;font-weight:700;color:#E65100;margin-bottom:12px;">부족 사이즈 ({low}건)</div>
    <div>{low_badges}</div>
  </div>'''}

  <!-- 상세 테이블 (부족/품절만) -->
  {"" if (oos + low) == 0 else f'''
  <div style="padding:0 32px 32px;">
    <table style="width:100%;border-collapse:collapse;border:1px solid #eee;">
      <tr style="background:#1B2A4A;">
        <th style="padding:10px 12px;color:#fff;font-size:12px;text-align:left;">상품번호</th>
        <th style="padding:10px 12px;color:#fff;font-size:12px;text-align:left;">상품명</th>
        <th style="padding:10px 12px;color:#fff;font-size:12px;text-align:center;">사이즈</th>
        <th style="padding:10px 12px;color:#fff;font-size:12px;text-align:center;">재고</th>
      </tr>
      {product_rows}
    </table>
  </div>'''}

  <!-- 푸터 -->
  <div style="padding:16px 32px;background:#f8f9fa;font-size:12px;color:#999;border-top:1px solid #eee;">
    짱베이스볼 재고 자동 모니터링 (v8 Open API) | 매일 오전 8시 자동 실행
  </div>

</div>
</body></html>"""

    return html


def send_gmail(config, subject, html_body):
    """Gmail SMTP로 메일 발송"""
    email_config = config.get("email", {})
    gmail_addr = email_config.get("gmail_address", "")
    app_password = email_config.get("gmail_app_password", "")

    if not gmail_addr or not app_password:
        log.warning("Gmail 설정 없음 (gmail_address 또는 gmail_app_password) - 메일 발송 건너뜀")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_addr
    msg["To"] = gmail_addr  # self 발송
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(gmail_addr, app_password)
            server.send_message(msg)
        log.info(f"메일 발송 완료: {gmail_addr}")
        return True
    except smtplib.SMTPAuthenticationError:
        log.error("Gmail 인증 실패 - 앱 비밀번호를 확인하세요")
        log.error("  설정: Google 계정 > 보안 > 2단계 인증 > 앱 비밀번호")
        return False
    except Exception as e:
        log.error(f"메일 발송 실패: {e}")
        return False


def save_result(results, analysis, timestamp):
    """결과 JSON 저장"""
    output = {
        "timestamp": timestamp,
        "version": "v8",
        "method": "godomall_openhub_api",
        "summary": {
            "total_products": analysis["total_products"],
            "total_stock": analysis["total_stock"],
            "out_of_stock_options": analysis["out_of_stock_count"],
            "low_stock_options": analysis["low_stock_count"],
            "reorder_items": 0
        },
        "all_products": results,
        "reorder": []
    }

    output_path = OUTPUT_DIR / "stock-check-result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    log.info(f"결과 저장: {output_path}")
    return output_path


def main():
    args = sys.argv[1:]
    no_mail = "--nomail" in args
    test_mode = "--test" in args

    log.info("=" * 50)
    log.info("짱베이스볼 재고 모니터링 시작")
    log.info("=" * 50)

    # 1. 설정 로드
    config = load_config()
    products = config["monitor_products"]
    log.info(f"모니터링 대상: {len(products)}개 상품")

    if test_mode:
        config["monitor_products"] = products[:1]
        log.info("[테스트 모드] 첫 번째 상품만 조회")

    # 2. 재고 조회
    results = fetch_stock_api(config)
    if not results:
        log.error("조회 결과 없음 - 종료")
        sys.exit(1)

    # 3. 분석
    analysis = analyze_stock(results, config)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    log.info(f"전체 재고: {analysis['total_stock']:,}개")
    log.info(f"품절: {analysis['out_of_stock_count']}건 / 부족: {analysis['low_stock_count']}건")

    # 4. 결과 저장
    save_result(results, analysis, timestamp)

    # 5. HTML 리포트 생성
    html = build_html_report(results, analysis, timestamp)

    # HTML 파일로도 저장
    html_path = OUTPUT_DIR / "stock-check-report.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    log.info(f"HTML 리포트 저장: {html_path}")

    # 6. 메일 발송
    if not no_mail:
        oos = analysis["out_of_stock_count"]
        low = analysis["low_stock_count"]
        prefix = config["email"].get("subject_prefix", "[짱베이스볼 재고알림]")
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"{prefix} {today} 재고 현황 (품절 {oos}건 / 부족 {low}건)"

        sent = send_gmail(config, subject, html)
        if not sent:
            log.warning("메일 미발송 - HTML 파일로 확인하세요")
    else:
        log.info("[--nomail] 메일 발송 건너뜀")

    # 7. 완료
    log.info("재고 모니터링 완료")
    print(f"\n전체 재고: {analysis['total_stock']:,}개 | 품절: {analysis['out_of_stock_count']}건 | 부족: {analysis['low_stock_count']}건")


if __name__ == "__main__":
    main()
