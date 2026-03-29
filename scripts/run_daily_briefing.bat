@echo off
:: 일일 브리핑 자동 실행 배치파일
:: Windows 작업 스케줄러에 등록하여 매일 아침 자동 실행

cd /d C:\Users\NO
claude --print "DailyBriefingLead 에이전트를 실행해서 오늘 일일 브리핑을 생성하고 이메일로 발송해줘" --model claude-sonnet-4-6 >> C:\Users\NO\.claude\output\daily-briefing\run_log.txt 2>&1
