---
name: Playwright 배너 캡처 워크플로
description: 구글 드라이브 동기화 폴더에서 Playwright 실행 시 UNC 경로 오류 우회 방법
type: project
---

output 폴더(C:/Users/jj1/.claude/output/)는 구글 드라이브 동기화 경로(G:\내 드라이브\claude-config\output\)로 매핑됨.

Node.js에서 이 경로에 직접 npm/playwright를 설치하면 UNC 경로 파싱 오류 발생.

**Why:** Windows에서 구글 드라이브 동기화 폴더는 UNC 경로 형태로 인식되어 Node.js package.json 파서가 실패함.

**How to apply:**
1. C 드라이브 임시 폴더(C:/Users/jj1/tmp-banner-capture)에 playwright 설치 및 스크립트 실행
2. HTML 파일을 임시 폴더로 복사 후 캡처
3. 생성된 PNG를 C:/Users/jj1/AppData/Local/Temp/banner-output/ 에 저장
4. 최종 output 폴더로 cp 복사
5. 작업 완료 후 임시 폴더 삭제
