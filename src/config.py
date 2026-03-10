import os


class Config:
    """환경변수 기반 설정 관리"""

    def __init__(self):
        self.dry_run = os.environ.get("DRY_RUN", "").lower() in ("true", "1", "yes")

        if self.dry_run:
            self.godo_partner_key = ""
            self.godo_user_key = ""
            self.godo_shop_url = ""
            self.gmail_address = ""
            self.gmail_app_password = ""
            self.recipient_emails = []
        else:
            self.godo_partner_key = os.environ["GODO_PARTNER_KEY"]
            self.godo_user_key = os.environ["GODO_USER_KEY"]
            self.godo_shop_url = os.environ["GODO_SHOP_URL"].rstrip("/")
            self.gmail_address = os.environ["GMAIL_ADDRESS"]
            self.gmail_app_password = os.environ["GMAIL_APP_PASSWORD"]
            self.recipient_emails = [
                e.strip() for e in os.environ["RECIPIENT_EMAIL"].split(",")
            ]

        self.target_goods_nos = [
            n.strip()
            for n in os.environ.get("TARGET_GOODS_NOS", "1000,1001,1002").split(",")
        ]

        self.low_stock_threshold = int(os.environ.get("LOW_STOCK_THRESHOLD", "10"))
