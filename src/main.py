import logging
import sys

from config import Config
from godo_api import GodoApiClient, MockGodoApiClient
from email_sender import send_inventory_email, save_html_preview

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=== 고도몰 재고 확인 자동화 시작 ===")

    try:
        config = Config()
    except KeyError as e:
        logger.error("필수 환경변수가 설정되지 않았습니다: %s", e)
        sys.exit(1)

    if config.dry_run:
        logger.info("[DRY-RUN 모드] mock 데이터 사용, 이메일 미발송")

    logger.info("대상 상품: %s (%d건)", config.target_goods_nos, len(config.target_goods_nos))
    logger.info("재고 부족 기준: %d개 이하", config.low_stock_threshold)

    # 재고 조회
    if config.dry_run:
        client = MockGodoApiClient()
    else:
        client = GodoApiClient(
            shop_url=config.godo_shop_url,
            partner_key=config.godo_partner_key,
            user_key=config.godo_user_key,
        )
    stock_items = client.get_stock_info(config.target_goods_nos)

    # 결과 요약 로그
    for item in stock_items:
        if item.get("error"):
            logger.warning("  [실패] 상품 %s: %s", item["goods_no"], item["goods_name"])
        elif item["stock_qty"] <= config.low_stock_threshold:
            logger.warning("  [부족] 상품 %s (%s): %d개", item["goods_no"], item["goods_name"], item["stock_qty"])
        else:
            logger.info("  [정상] 상품 %s (%s): %d개", item["goods_no"], item["goods_name"], item["stock_qty"])

    # 이메일 발송 또는 HTML 미리보기 저장
    if config.dry_run:
        filepath = save_html_preview(
            stock_items=stock_items,
            threshold=config.low_stock_threshold,
        )
        logger.info("브라우저에서 열어 확인하세요: %s", filepath)
    else:
        send_inventory_email(
            gmail_address=config.gmail_address,
            gmail_app_password=config.gmail_app_password,
            recipients=config.recipient_emails,
            stock_items=stock_items,
            threshold=config.low_stock_threshold,
        )

    logger.info("=== 완료 ===")


if __name__ == "__main__":
    main()
