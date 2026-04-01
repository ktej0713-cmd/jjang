@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  짱베이스볼 재고체크 예약 작업 등록
echo ========================================
echo.
echo  관리자 권한으로 실행해야 합니다.
echo  (우클릭 → 관리자 권한으로 실행)
echo.

REM === 설정 ===
set TASK_NAME=짱베이스볼_재고체크
set PYTHON_PATH=python
set SCRIPT_PATH=%USERPROFILE%\.claude\automation\stock-check.py
set RUN_TIME=08:00

REM === 기존 작업 삭제 (있으면) ===
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

REM === 예약 작업 등록: 매일 오전 8시 ===
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
  /sc daily ^
  /st %RUN_TIME% ^
  /f ^
  /rl HIGHEST

if %errorlevel%==0 (
    echo.
    echo  [OK] 등록 완료!
    echo.
    echo  작업명: %TASK_NAME%
    echo  실행시간: 매일 %RUN_TIME%
    echo  스크립트: %SCRIPT_PATH%
    echo.
    echo ----------------------------------------
    echo  등록된 작업 확인:
    echo ----------------------------------------
    schtasks /query /tn "%TASK_NAME%" /fo list
) else (
    echo.
    echo  [FAIL] 등록 실패
    echo  관리자 권한으로 다시 실행하세요.
)

echo.
pause
