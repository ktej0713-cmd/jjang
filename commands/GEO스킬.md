---
description: GEO 스킬 자동 업데이트 관리 (조회/수정/실행)
---

~/skill-auto-update/ 폴더의 GEO 스킬 자동 업데이트 시스템을 관리한다.

## 기본 동작 (인자 없이 호출 시)
아래 파일들을 읽고 현재 상태를 요약 보고한다:
- ~/skill-auto-update/update-log.txt — 최근 업데이트 이력
- ~/skill-auto-update/run-log.txt — 최근 실행 로그
- 스케줄러 상태: `powershell.exe -Command "Get-ScheduledTask -TaskName 'GEO스킬자동업데이트' | Get-ScheduledTaskInfo"`

보고 형식:
```
[GEO 스킬 현황]
- 마지막 실행: yyyy-MM-dd HH:mm
- 결과: 성공/실패
- 현재 원칙 수: N개
- 최근 추가: (마지막 update-log 내용)
- 다음 실행: yyyy-MM-dd 07:00
```

## 사용자가 수정을 요청하면
해당 파일을 읽고 수정한다:
- "프롬프트 수정" → ~/skill-auto-update/prompt.txt
- "메일 수정" → ~/skill-auto-update/email-template.html
- "스크립트 수정" → ~/skill-auto-update/run-update.ps1
- "스킬 확인" → SKILL.md 원본 읽기

## 사용자가 실행을 요청하면
`powershell.exe -Command "Start-ScheduledTask -TaskName 'GEO스킬자동업데이트'"` 실행 후 결과 확인.

## 관련 파일 경로
- SKILL.md: ~/AppData/Local/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/Claude/local-agent-mode-sessions/skills-plugin/10aac6b3-d9f1-493b-914e-883980269d41/13b0d56a-3740-46c5-b9f1-d0f0d35505fa/skills/premium-geo-detail/SKILL.md
- 작업 폴더: ~/skill-auto-update/
