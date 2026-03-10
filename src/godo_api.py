import logging
import random
import time

import requests

logger = logging.getLogger(__name__)

# Mock 상품 데이터 (dry-run 모드용)
MOCK_PRODUCTS = {
    "1000": {
        "goods_name": "[테스트] 기본 티셔츠 - 재고 정상",
        "stock_qty": 150,
        "options": [],
    },
    "1001": {
        "goods_name": "[테스트] 여름 반바지 - 재고 부족",
        "stock_qty": 7,
        "options": [
            {"option_name": "S", "stock_qty": 0},
            {"option_name": "M", "stock_qty": 3},
            {"option_name": "L", "stock_qty": 4},
        ],
    },
    "1002": {
        "goods_name": "[테스트] 한정판 스니커즈 - 품절",
        "stock_qty": 0,
        "options": [
            {"option_name": "260mm", "stock_qty": 0},
            {"option_name": "270mm", "stock_qty": 0},
        ],
    },
    "1003": {
        "goods_name": "[테스트] 겨울 패딩 - 옵션별 다양",
        "stock_qty": 45,
        "options": [
            {"option_name": "블랙/M", "stock_qty": 20},
            {"option_name": "블랙/L", "stock_qty": 15},
            {"option_name": "네이비/M", "stock_qty": 8},
            {"option_name": "네이비/L", "stock_qty": 2},
        ],
    },
}


class MockGodoApiClient:
    """고도몰 API mock 클라이언트 (dry-run 테스트용)"""

    def get_stock_info(self, goods_nos: list[str]) -> list[dict]:
        results = []
        for goods_no in goods_nos:
            if goods_no in MOCK_PRODUCTS:
                mock = MOCK_PRODUCTS[goods_no]
            else:
                # 등록되지 않은 상품번호는 랜덤 재고 생성
                mock = {
                    "goods_name": f"테스트 상품 #{goods_no}",
                    "stock_qty": random.randint(0, 200),
                    "options": [],
                }
            results.append({
                "goods_no": goods_no,
                "goods_name": mock["goods_name"],
                "stock_qty": mock["stock_qty"],
                "options": mock["options"],
                "error": False,
            })
        return results


class GodoApiClient:
    """고도몰 오픈 API 클라이언트

    고도몰5 오픈 API를 통해 상품 정보 및 재고를 조회합니다.
    API 스펙: https://server-docs.godomall.com/
    """

    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    def __init__(self, shop_url: str, partner_key: str, user_key: str):
        self.base_url = shop_url
        self.partner_key = partner_key
        self.user_key = user_key
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: dict | None = None) -> dict:
        """API 요청 실행 (재시도 로직 포함)"""
        url = f"{self.base_url}/{endpoint}"

        payload = {
            "partner_key": self.partner_key,
            "key": self.user_key,
        }
        if params:
            payload.update(params)

        last_error = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = self.session.post(url, data=payload, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                last_error = e
                logger.warning(
                    "API 요청 실패 (시도 %d/%d): %s", attempt, self.MAX_RETRIES, e
                )
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.RETRY_DELAY * attempt)

        raise ConnectionError(
            f"API 요청이 {self.MAX_RETRIES}회 실패했습니다: {last_error}"
        )

    def get_goods_info(self, goods_no: str) -> dict:
        """개별 상품 정보 조회

        Args:
            goods_no: 상품번호

        Returns:
            상품 정보 dict (goodsNo, goodsNm, stockQty, options 등)
        """
        # 고도몰 오픈 API 상품 조회 엔드포인트
        # 실제 엔드포인트는 고도몰 API 스펙 정의서 참고하여 수정 필요
        # https://devcenter.nhn-commerce.com/godomall5/openapi/specDownload
        data = self._make_request(
            "api/goods/Goods_Search.php",
            params={"goodsNo": goods_no},
        )
        return data

    def get_stock_info(self, goods_nos: list[str]) -> list[dict]:
        """복수 상품의 재고 정보 조회

        Args:
            goods_nos: 상품번호 목록

        Returns:
            각 상품의 재고 정보 리스트
            [{"goods_no": "1000", "goods_name": "...", "stock_qty": 50, "options": [...]}]
        """
        results = []

        for goods_no in goods_nos:
            try:
                data = self.get_goods_info(goods_no)
                item = self._parse_goods_response(goods_no, data)
                results.append(item)
            except Exception as e:
                logger.error("상품 %s 조회 실패: %s", goods_no, e)
                results.append({
                    "goods_no": goods_no,
                    "goods_name": f"(조회 실패: {e})",
                    "stock_qty": -1,
                    "options": [],
                    "error": True,
                })

        return results

    def _parse_goods_response(self, goods_no: str, data: dict) -> dict:
        """API 응답을 파싱하여 재고 정보 추출

        고도몰 API 응답 구조에 따라 파싱합니다.
        실제 응답 구조가 다를 경우 이 메서드를 수정하세요.
        """
        # 응답이 리스트인 경우 (검색 결과)
        if isinstance(data, list) and len(data) > 0:
            goods = data[0]
        elif isinstance(data, dict):
            # "goods" 또는 "data" 키로 감싸진 경우
            goods = data.get("goods", data.get("data", data))
            if isinstance(goods, list) and len(goods) > 0:
                goods = goods[0]
        else:
            goods = {}

        # 옵션별 재고 파싱
        options = []
        option_data = goods.get("option", goods.get("options", []))
        if isinstance(option_data, list):
            for opt in option_data:
                options.append({
                    "option_name": opt.get("optionNm", opt.get("name", "")),
                    "stock_qty": int(opt.get("stockQty", opt.get("stock", 0))),
                })

        # 전체 재고 수량 (옵션이 있으면 옵션 합산, 없으면 상품 자체 재고)
        if options:
            total_stock = sum(o["stock_qty"] for o in options)
        else:
            total_stock = int(
                goods.get("stockQty", goods.get("totalStock", goods.get("stock", 0)))
            )

        return {
            "goods_no": goods_no,
            "goods_name": goods.get("goodsNm", goods.get("name", f"상품 #{goods_no}")),
            "stock_qty": total_stock,
            "options": options,
            "error": False,
        }
