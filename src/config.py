import os


class Config:
    """환경변수 기반 설정 관리"""

    def __init__(self):
        self.godo_partner_key = os.environ["GODO_PARTNER_KEY"]
        self.godo_user_key = os.environ["GODO_USER_KEY"]
        self.godo_shop_url = os.environ["GODO_SHOP_URL"].rstrip("/")

        self.gmail_address = os.environ["GMAIL_ADDRESS"]
        self.gmail_app_password = os.environ["GMAIL_APP_PASSWORD"]
        self.recipient_emails = [
            e.strip() for e in os.environ["RECIPIENT_EMAIL"].split(",")
        ]

        self.target_goods_nos = [
            n.strip() for n in os.environ["TARGET_GOODS_NOS"].split(",")
        ]

        self.low_stock_threshold = int(os.environ.get("LOW_STOCK_THRESHOLD", "10"))
