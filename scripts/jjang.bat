@echo off
chcp 65001 >nul
REM 짱베이스볼 자동화 런처 (Windows)
REM 사용법: 더블클릭 또는 CMD에서 jjang [명령]

set CLAUDE_DIR=%USERPROFILE%\.claude
set SCRIPTS_DIR=%CLAUDE_DIR%\scripts

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="campaign" goto campaign
if "%1"=="product" goto product
if "%1"=="season" goto season
if "%1"=="monitor-seo" goto monitor_seo
if "%1"=="monitor-competitor" goto monitor_comp
if "%1"=="monitor-all" goto monitor_all
if "%1"=="status" goto status
if "%1"=="team" goto team
goto unknown

:help
echo.
echo   짱베이스볼 자동화 시스템
echo   ================================
echo.
echo   MD팀 작업:
echo     jjang campaign [이름]     기획전 기획 (MD팀 병렬)
echo     jjang product [상품명]    상품 상세페이지 생성
echo     jjang season              이번 달 시즌 전략 브리핑
echo.
echo   모니터링:
echo     jjang monitor-seo         SEO 키워드 체크
echo     jjang monitor-competitor  경쟁몰 모니터링
echo     jjang monitor-all         전체 모니터링
echo.
echo   시스템:
echo     jjang team                에이전트 팀 소집
echo     jjang status              상태 확인
echo.
goto end

:campaign
bash "%SCRIPTS_DIR%\jjang.sh" campaign %2 %3 %4
goto end

:product
bash "%SCRIPTS_DIR%\jjang.sh" product %2 %3 %4
goto end

:season
bash "%SCRIPTS_DIR%\jjang.sh" season
goto end

:monitor_seo
python "%CLAUDE_DIR%\automation\seo-checker.py"
goto end

:monitor_comp
python "%CLAUDE_DIR%\automation\competitor-monitor.py"
goto end

:monitor_all
echo [1/3] SEO 모니터링...
python "%CLAUDE_DIR%\automation\seo-checker.py"
echo [2/3] 경쟁몰 모니터링...
python "%CLAUDE_DIR%\automation\competitor-monitor.py"
echo [3/3] 시즌 알림...
python "%CLAUDE_DIR%\automation\season-alert.py"
echo.
echo 전체 모니터링 완료!
goto end

:status
bash "%SCRIPTS_DIR%\jjang.sh" status
goto end

:team
bash "%SCRIPTS_DIR%\jjang.sh" team
goto end

:unknown
echo 알 수 없는 명령: %1
echo 'jjang help' 로 도움말 확인
goto end

:end
