"""
고도몰 오더갤러리 이미지 자동 업로드 스크립트

흐름:
    1. 폴더에서 새 이미지 스캔
    2. NHN 이미지호스팅(FTP)에 이미지 업로드 → URL 획득
    3. 고도몰 Open API로 게시물 등록 (이미지 URL 첨부)

사용법:
    python upload.py              # 폴더 내 모든 이미지 업로드
    python upload.py --dry-run    # 실제 업로드 없이 대상 파일만 확인
    python upload.py --test       # API/FTP 연결 테스트

사전 준비:
    1. pip install requests
    2. config.ini에 고도몰 API 키 + FTP 정보 입력
"""

import argparse
import configparser
import ftplib
import json
import os
import shutil
import ssl
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

UPLOAD_LOG_FILE = "upload_log.json"


def load_config(config_path="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


def load_upload_log():
    if os.path.exists(UPLOAD_LOG_FILE):
        with open(UPLOAD_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"uploaded_files": []}


def save_upload_log(log):
    with open(UPLOAD_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def get_image_files(image_folder, extensions):
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


def ftp_upload(image_path, ftp_host, ftp_user, ftp_pass, ftp_upload_dir, image_base_url):
    """NHN 이미지호스팅 FTP에 이미지 업로드 후 URL 반환"""
    filename = Path(image_path).name

    ftp = None
    try:
        # FTP 연결 (일반 FTP 시도, 실패 시 FTPS 시도)
        try:
            ftp = ftplib.FTP(ftp_host, timeout=30)
            ftp.login(ftp_user, ftp_pass)
        except Exception:
            print(f"  [FTP] 일반 FTP 실패, FTPS로 재시도...")
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            ftp = ftplib.FTP_TLS(ftp_host, timeout=30)
            ftp.login(ftp_user, ftp_pass)
            ftp.prot_p()

        # 업로드 디렉토리 이동 (없으면 생성)
        dirs = ftp_upload_dir.strip("/").split("/")
        for d in dirs:
            try:
                ftp.cwd(d)
            except ftplib.error_perm:
                ftp.mkd(d)
                ftp.cwd(d)

        # 파일 업로드
        with open(image_path, "rb") as f:
            ftp.storbinary(f"STOR {filename}", f)

        # URL 생성
        image_url = f"{image_base_url.rstrip('/')}/{ftp_upload_dir.strip('/')}/{filename}"
        print(f"  [FTP] 업로드 성공: {image_url}")
        return image_url

    except Exception as e:
        print(f"  [FTP 오류] {e}")
        return None

    finally:
        if ftp:
            try:
                ftp.quit()
            except Exception:
                pass


def ftp_test(ftp_host, ftp_user, ftp_pass):
    """FTP 연결 테스트"""
    print(f"[테스트] FTP 연결 테스트: {ftp_host}")
    try:
        try:
            ftp = ftplib.FTP(ftp_host, timeout=10)
            ftp.login(ftp_user, ftp_pass)
            print(f"[테스트] FTP 연결 성공! (일반 FTP)")
        except Exception:
            print(f"  [FTP] 일반 FTP 실패, FTPS로 재시도...")
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            ftp = ftplib.FTP_TLS(ftp_host, timeout=10)
            ftp.login(ftp_user, ftp_pass)
            ftp.prot_p()
            print(f"[테스트] FTP 연결 성공! (FTPS)")

        # 현재 디렉토리 목록 출력
        print(f"  현재 경로: {ftp.pwd()}")
        files = ftp.nlst()
        print(f"  파일/폴더: {files[:10]}{'...' if len(files) > 10 else ''}")
        ftp.quit()
        return True

    except Exception as e:
        print(f"[테스트] FTP 연결 실패: {e}")
        return False


def write_board_article(godo_api_url, partner_key, user_key, board_id, subject, contents, files_data=None):
    """고도몰 Open API로 게시물 등록"""
    data = {
        "partner_key": partner_key,
        "key": user_key,
        "bdId": board_id,
        "subject": subject,
        "contents": contents,
        "notice": "n",
    }

    if files_data:
        data["filesData"] = files_data

    resp = requests.post(godo_api_url, data=data, timeout=30)
    print(f"  [고도몰] POST board_write -> {resp.status_code}")

    if resp.status_code == 200:
        try:
            result = resp.json()
            print(f"  [고도몰] 응답: {json.dumps(result, ensure_ascii=False)[:300]}")
            return result
        except (json.JSONDecodeError, ValueError):
            print(f"  [고도몰] 응답: {resp.text[:300]}")
            return resp.text
    else:
        print(f"  [고도몰 오류] Status: {resp.status_code}")
        print(f"  [고도몰 오류] Response: {resp.text[:300]}")
        return None


def move_to_done(image_path, done_folder):
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
    parser = argparse.ArgumentParser(description="고도몰 오더갤러리 이미지 자동 업로드")
    parser.add_argument("--config", default="config.ini", help="설정 파일 경로")
    parser.add_argument("--dry-run", action="store_true", help="실제 업로드 없이 대상 파일만 확인")
    parser.add_argument("--test", action="store_true", help="API/FTP 연결 테스트")
    args = parser.parse_args()

    config = load_config(args.config)

    try:
        api_config = config["api"]
        ftp_config = config["ftp"]
        settings = config["settings"]
    except KeyError as e:
        print(f"[오류] config.ini에 [{e}] 섹션이 없습니다.")
        sys.exit(1)

    godo_api_url = api_config.get("godo_api_url")
    partner_key = api_config.get("partner_key")
    user_key = api_config.get("user_key")
    board_id = api_config.get("board_id", "customgallery")

    ftp_host = ftp_config.get("ftp_host")
    ftp_user = ftp_config.get("ftp_user")
    ftp_pass = ftp_config.get("ftp_pass")
    ftp_upload_dir = ftp_config.get("ftp_upload_dir", "/data/image/ORDER_GALLERY")
    image_base_url = ftp_config.get("image_base_url")

    # 연결 테스트
    if args.test:
        print("=" * 50)
        ftp_test(ftp_host, ftp_user, ftp_pass)
        print()
        print("[테스트] 고도몰 API 연결 테스트...")
        result = write_board_article(
            godo_api_url, partner_key, user_key,
            board_id, "API 테스트", "자동 업로드 시스템 테스트"
        )
        if result is not None:
            print("[테스트] 고도몰 API 성공!")
        else:
            print("[테스트] 고도몰 API 실패.")
        print("=" * 50)
        return

    image_folder = settings.get("image_folder")
    extensions = settings.get("image_extensions", ".jpg,.jpeg,.png,.gif,.webp,.bmp")
    done_folder = settings.get("done_folder", "")
    upload_delay = int(settings.get("upload_delay", "2"))
    title_format = settings.get("post_title_format", "{filename}")
    content_format = settings.get("post_content_format", "")

    # 이미지 파일 스캔
    image_files = get_image_files(image_folder, extensions)

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
    print(f"  FTP: {ftp_host}")
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
            content = content_format.replace("{filename}", filename) if content_format else title

            # 1. FTP에 이미지 업로드
            print(f"  [1/2] FTP에 이미지 업로드 중...")
            image_url = ftp_upload(
                str(image_path), ftp_host, ftp_user, ftp_pass,
                ftp_upload_dir, image_base_url
            )
            if not image_url:
                print(f"  [실패] FTP 업로드 실패, 건너뜁니다.")
                fail_count += 1
                continue

            # 2. 고도몰 게시판에 글 등록
            print(f"  [2/2] 고도몰 게시판에 등록 중...")
            result = write_board_article(
                godo_api_url, partner_key, user_key,
                board_id, title, content, files_data=image_url
            )

            if result is not None:
                print(f"  [성공] {image_path.name} 업로드 완료!")
                upload_log["uploaded_files"].append(str(image_path.resolve()))
                save_upload_log(upload_log)
                move_to_done(image_path, done_folder)
                success_count += 1
            else:
                print(f"  [실패] 고도몰 게시판 등록 실패")
                fail_count += 1

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
