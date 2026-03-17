@echo off
chcp 65001 >nul
echo 짱베이스볼 예약 작업 설정
echo ================================
echo.
echo 관리자 권한이 필요합니다.
echo.

REM 매일 오전 9시: 시즌 알림 브리핑
schtasks /create /tn "짱베이스볼_시즌알림" /tr "python %USERPROFILE%\.claude\automation\season-alert.py" /sc daily /st 09:00 /f
if %errorlevel%==0 (echo [OK] 시즌 알림: 매일 09:00) else (echo [FAIL] 시즌 알림 설정 실패)

REM 매주 월요일 오전 10시: SEO 체크
schtasks /create /tn "짱베이스볼_SEO체크" /tr "python %USERPROFILE%\.claude\automation\seo-checker.py" /sc weekly /d MON /st 10:00 /f
if %errorlevel%==0 (echo [OK] SEO 체크: 매주 월요일 10:00) else (echo [FAIL] SEO 체크 설정 실패)

REM 매주 수요일 오전 10시: 경쟁몰 모니터링
schtasks /create /tn "짱베이스볼_경쟁몰모니터링" /tr "python %USERPROFILE%\.claude\automation\competitor-monitor.py" /sc weekly /d WED /st 10:00 /f
if %errorlevel%==0 (echo [OK] 경쟁몰 모니터링: 매주 수요일 10:00) else (echo [FAIL] 경쟁몰 모니터링 설정 실패)

echo.
echo 설정 완료! 예약 작업 확인:
schtasks /query /tn "짱베이스볼_시즌알림" /fo list 2>nul | findstr "작업 이름 상태 다음"
schtasks /query /tn "짱베이스볼_SEO체크" /fo list 2>nul | findstr "작업 이름 상태 다음"
schtasks /query /tn "짱베이스볼_경쟁몰모니터링" /fo list 2>nul | findstr "작업 이름 상태 다음"
echo.
pause
