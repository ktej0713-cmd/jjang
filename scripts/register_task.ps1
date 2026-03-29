# 관리자 권한으로 실행: PowerShell을 우클릭 -> 관리자로 실행 후 이 스크립트 실행
# 실행 방법: powershell -ExecutionPolicy Bypass -File "C:\Users\NO\.claude\scripts\register_task.ps1"

$action = New-ScheduledTaskAction `
    -Execute "C:\Users\NO\.claude\scripts\run_daily_briefing.bat"

$trigger = New-ScheduledTaskTrigger -Daily -At "00:00"

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

Register-ScheduledTask `
    -TaskName "Daily Briefing" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "[완료] 작업 스케줄러 등록됨: 매일 00:00 실행" -ForegroundColor Green
