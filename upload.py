"""
고도몰 오더갤러리 이미지 자동 업로드 스크립트

사용법:
    python upload.py              # 폴더 내 모든 이미지 업로드
    python upload.py --dry-run    # 실제 업로드 없이 대상 파일만 확인
"""

import argparse
import configparser
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

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


def create_driver(headless=False):
    """Chrome WebDriver 생성"""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver


def login(driver, config, wait):
    """고도몰 관리자 로그인"""
    login_url = config.get("godo", "admin_login_url")
    admin_id = config.get("godo", "admin_id")
    admin_pw = config.get("godo", "admin_pw")
    selectors = config["selectors"]

    print(f"[로그인] {login_url} 접속 중...")
    driver.get(login_url)
    time.sleep(2)

    # ID 입력
    id_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, selectors.get("id_input"))
    ))
    id_field.clear()
    id_field.send_keys(admin_id)

    # 비밀번호 입력
    pw_field = driver.find_element(By.CSS_SELECTOR, selectors.get("pw_input"))
    pw_field.clear()
    pw_field.send_keys(admin_pw)

    # 로그인 버튼 클릭
    login_btn = driver.find_element(By.CSS_SELECTOR, selectors.get("login_button"))
    login_btn.click()

    time.sleep(3)
    print("[로그인] 로그인 완료")


def upload_image(driver, config, wait, image_path):
    """이미지를 게시판에 업로드"""
    board_url = config.get("godo", "board_write_url")
    selectors = config["selectors"]
    settings = config["settings"]

    filename = image_path.stem  # 확장자 제외 파일명
    title = settings.get("post_title_format", "{filename}").replace("{filename}", filename)
    content = settings.get("post_content_format", "").replace("{filename}", filename)

    print(f"[업로드] 게시판 글쓰기 페이지 이동: {image_path.name}")
    driver.get(board_url)
    time.sleep(2)

    # 제목 입력
    title_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, selectors.get("title_input"))
    ))
    title_field.clear()
    title_field.send_keys(title)

    # 내용 입력 (있는 경우)
    if content:
        try:
            content_field = driver.find_element(
                By.CSS_SELECTOR, selectors.get("content_textarea")
            )
            content_field.clear()
            content_field.send_keys(content)
        except Exception:
            print(f"  [경고] 내용 입력란을 찾을 수 없습니다. 건너뜁니다.")

    # 파일 업로드 (input[type=file]에 파일 경로 전송)
    file_input = driver.find_element(By.CSS_SELECTOR, selectors.get("file_input"))
    file_input.send_keys(str(image_path.resolve()))
    time.sleep(2)

    # 등록 버튼 클릭
    submit_btn = driver.find_element(By.CSS_SELECTOR, selectors.get("submit_button"))
    submit_btn.click()
    time.sleep(3)

    print(f"[업로드] 완료: {image_path.name}")


def move_to_done(image_path, done_folder):
    """업로드 완료된 파일을 done 폴더로 이동"""
    if not done_folder:
        return

    done_path = Path(done_folder)
    done_path.mkdir(parents=True, exist_ok=True)

    dest = done_path / image_path.name
    # 동일 파일명이 있으면 타임스탬프 추가
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
    args = parser.parse_args()

    # 설정 로드
    config = load_config(args.config)
    settings = config["settings"]

    image_folder = settings.get("image_folder")
    extensions = settings.get("image_extensions", ".jpg,.jpeg,.png,.gif,.webp,.bmp")
    done_folder = settings.get("done_folder", "")
    upload_delay = int(settings.get("upload_delay", "3"))
    headless = settings.get("headless", "false").lower() == "true"

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
    print(f"{'='*50}")
    for i, f in enumerate(new_files, 1):
        print(f"  {i}. {f.name}")
    print()

    if args.dry_run:
        print("[Dry Run] 실제 업로드는 수행하지 않습니다.")
        return

    # Selenium 브라우저 시작
    driver = None
    try:
        driver = create_driver(headless=headless)
        wait = WebDriverWait(driver, 15)

        # 로그인
        login(driver, config, wait)

        # 각 이미지 업로드
        success_count = 0
        fail_count = 0

        for i, image_path in enumerate(new_files, 1):
            try:
                print(f"\n--- [{i}/{len(new_files)}] ---")
                upload_image(driver, config, wait, image_path)

                # 업로드 기록 저장
                upload_log["uploaded_files"].append(str(image_path.resolve()))
                save_upload_log(upload_log)

                # 완료 폴더로 이동
                move_to_done(image_path, done_folder)

                success_count += 1

                # 다음 업로드 전 대기
                if i < len(new_files):
                    print(f"  [대기] {upload_delay}초 후 다음 업로드...")
                    time.sleep(upload_delay)

            except Exception as e:
                print(f"  [오류] {image_path.name} 업로드 실패: {e}")
                fail_count += 1
                continue

        print(f"\n{'='*50}")
        print(f"  업로드 결과: 성공 {success_count}개 / 실패 {fail_count}개")
        print(f"{'='*50}")

    except Exception as e:
        print(f"[오류] {e}")
        sys.exit(1)

    finally:
        if driver:
            driver.quit()
            print("[브라우저] 종료")


if __name__ == "__main__":
    main()
