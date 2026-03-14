"""
고도몰 오더갤러리 이미지 자동 업로드 스크립트 (Open API 방식)

사용법:
    python upload.py              # 폴더 내 모든 이미지 업로드
    python upload.py --dry-run    # 실제 업로드 없이 대상 파일만 확인

사전 준비:
    1. pip install requests
    2. config.ini에 API 키와 설정값 입력
    3. 고도몰 개발자센터에서 API 키 발급 필요
       https://devcenter.nhn-commerce.com
"""

import argparse
import base64
import configparser
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# 업로드 기록 파일
UPLOAD_LOG_FILE = "upload_log.json"


def load_config(config_path="config.ini"):
    """설정 파일 로드"""
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


def load_upload_log():
    """업로드 기록 로드"""
    if os.path.exists(UPLOAD_LOG_FILE):
        with open(UPLOAD_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"uploaded_files": []}


def save_upload_log(log):
    """업로드 기록 저장"""
    with open(UPLOAD_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def get_image_files(image_folder, extensions):
    """폴더에서 이미지 파일 목록 가져오기"""
    ext_list = [ext.strip().lower() for ext in extensions.split(",")]
    files = []
    folder = Path(image_folder)

    if not folder.exists():
        print(f"[오류] 이미지 폴더가 존재하지 않습니다: {image_folder}")
        sys.exit(1)

    for file in sorted(folder.iterdir()):
        if file.is_file() and file.suffix.lower() in ext_list:
            files.append(file)

    return files


class GodoAPI:
    """고도몰 Open API 클라이언트"""

    def __init__(self, shop_url, partner_key, user_key):
        self.shop_url = shop_url.rstrip("/")
        self.partner_key = partner_key
        self.user_key = user_key
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "GodoUploader/1.0",
        })

    def _get_auth_params(self):
        """인증 파라미터 반환"""
        return {
            "partner_key": self.partner_key,
            "key": self.user_key,
        }

    def _api_url(self, endpoint):
        """API URL 생성"""
        return f"{self.shop_url}/openapi/{endpoint}"

    def _request(self, method, endpoint, data=None, files=None):
        """API 요청 실행"""
        url = self._api_url(endpoint)
        params = self._get_auth_params()

        try:
            if method == "GET":
                resp = self.session.get(url, params={**params, **(data or {})}, timeout=30)
            elif method == "POST":
                if files:
                    resp = self.session.post(url, data={**params, **(data or {})}, files=files, timeout=60)
                else:
                    resp = self.session.post(url, data={**params, **(data or {})}, timeout=30)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")

            print(f"  [API] {method} {endpoint} -> {resp.status_code}")

            if resp.status_code != 200:
                print(f"  [API 오류] Status: {resp.status_code}")
                print(f"  [API 오류] Response: {resp.text[:500]}")
                return None

            # JSON 또는 텍스트 응답 처리
            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                return resp.json()
            elif "xml" in content_type:
                return resp.text
            else:
                # JSON 파싱 시도
                try:
                    return resp.json()
                except (json.JSONDecodeError, ValueError):
                    return resp.text

        except requests.exceptions.ConnectionError as e:
            print(f"  [연결 오류] API 서버에 연결할 수 없습니다: {e}")
            return None
        except requests.exceptions.Timeout:
            print(f"  [타임아웃] API 요청 시간 초과")
            return None

    def test_connection(self):
        """API 연결 테스트"""
        print("[API] 연결 테스트 중...")
        result = self._request("GET", "board/list")
        if result is not None:
            print("[API] 연결 성공!")
            return True
        else:
            print("[API] 연결 실패. API 키와 URL을 확인해주세요.")
            return False

    def get_board_list(self):
        """게시판 목록 조회"""
        return self._request("GET", "board/list")

    def get_articles(self, board_id, page=1):
        """게시물 목록 조회"""
        return self._request("GET", "board/article/list", data={
            "bdId": board_id,
            "page": page,
        })

    def write_article(self, board_id, subject, content, image_path=None):
        """게시물 등록 (이미지 첨부)"""
        data = {
            "bdId": board_id,
            "subject": subject,
            "contents": content or subject,
        }

        files = None
        if image_path and os.path.exists(image_path):
            mime_types = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".bmp": "image/bmp",
            }
            ext = Path(image_path).suffix.lower()
            mime = mime_types.get(ext, "application/octet-stream")
            filename = Path(image_path).name
            files = {
                "uploadFile": (filename, open(image_path, "rb"), mime)
            }

        try:
            result = self._request("POST", "board/article/write", data=data, files=files)
            return result
        finally:
            if files and "uploadFile" in files:
                files["uploadFile"][1].close()


def move_to_done(image_path, done_folder):
    """업로드 완료된 파일을 done 폴더로 이동"""
    if not done_folder:
        return

    done_path = Path(done_folder)
    done_path.mkdir(parents=True, exist_ok=True)

    dest = done_path / image_path.name
    if dest.exists():
        stem = image_path.stem
        suffix = image_path.suffix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = done_path / f"{stem}_{timestamp}{suffix}"

    shutil.move(str(image_path), str(dest))
    print(f"  [이동] {image_path.name} -> {dest}")


def main():
    parser = argparse.ArgumentParser(description="고도몰 오더갤러리 이미지 자동 업로드 (API)")
    parser.add_argument("--config", default="config.ini", help="설정 파일 경로")
    parser.add_argument("--dry-run", action="store_true", help="실제 업로드 없이 대상 파일만 확인")
    parser.add_argument("--test", action="store_true", help="API 연결 테스트만 실행")
    args = parser.parse_args()

    # 설정 로드
    config = load_config(args.config)

    try:
        api_config = config["api"]
        settings = config["settings"]
    except KeyError as e:
        print(f"[오류] config.ini에 [{e}] 섹션이 없습니다. 설정 파일을 확인해주세요.")
        sys.exit(1)

    shop_url = api_config.get("shop_url")
    partner_key = api_config.get("partner_key")
    user_key = api_config.get("user_key")
    board_id = api_config.get("board_id", "customgallery")

    # API 키 확인
    if partner_key == "YOUR_PARTNER_KEY" or user_key == "YOUR_USER_KEY":
        print("[오류] config.ini에 API 키를 입력해주세요.")
        print("  partner_key = 제휴사 고유키")
        print("  user_key = API 승인시 발급된 사용자 키")
        print("  발급: https://devcenter.nhn-commerce.com")
        sys.exit(1)

    # API 클라이언트 생성
    api = GodoAPI(shop_url, partner_key, user_key)

    # 연결 테스트 모드
    if args.test:
        api.test_connection()
        return

    image_folder = settings.get("image_folder")
    extensions = settings.get("image_extensions", ".jpg,.jpeg,.png,.gif,.webp,.bmp")
    done_folder = settings.get("done_folder", "")
    upload_delay = int(settings.get("upload_delay", "2"))
    title_format = settings.get("post_title_format", "{filename}")
    content_format = settings.get("post_content_format", "")

    # 이미지 파일 목록
    image_files = get_image_files(image_folder, extensions)

    # 업로드 기록 로드 (이미 업로드된 파일 제외)
    upload_log = load_upload_log()
    uploaded_set = set(upload_log["uploaded_files"])
    new_files = [f for f in image_files if str(f.resolve()) not in uploaded_set]

    if not new_files:
        print("[완료] 새로 업로드할 이미지가 없습니다.")
        return

    print(f"\n{'='*50}")
    print(f"  업로드 대상: {len(new_files)}개 이미지")
    print(f"  이미지 폴더: {image_folder}")
    print(f"  게시판 ID: {board_id}")
    print(f"  API: {shop_url}")
    print(f"{'='*50}")
    for i, f in enumerate(new_files, 1):
        print(f"  {i}. {f.name}")
    print()

    if args.dry_run:
        print("[Dry Run] 실제 업로드는 수행하지 않습니다.")
        return

    # 업로드 실행
    success_count = 0
    fail_count = 0

    for i, image_path in enumerate(new_files, 1):
        try:
            print(f"\n--- [{i}/{len(new_files)}] {image_path.name} ---")

            filename = image_path.stem
            title = title_format.replace("{filename}", filename)
            content = content_format.replace("{filename}", filename) if content_format else ""

            result = api.write_article(
                board_id=board_id,
                subject=title,
                content=content,
                image_path=str(image_path.resolve()),
            )

            if result is not None:
                print(f"  [성공] {image_path.name} 업로드 완료")
                upload_log["uploaded_files"].append(str(image_path.resolve()))
                save_upload_log(upload_log)
                move_to_done(image_path, done_folder)
                success_count += 1
            else:
                print(f"  [실패] {image_path.name} 업로드 실패")
                fail_count += 1

            # 다음 업로드 전 대기
            if i < len(new_files):
                print(f"  [대기] {upload_delay}초...")
                time.sleep(upload_delay)

        except Exception as e:
            print(f"  [오류] {image_path.name}: {e}")
            fail_count += 1
            continue

    print(f"\n{'='*50}")
    print(f"  업로드 결과: 성공 {success_count}개 / 실패 {fail_count}개")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
