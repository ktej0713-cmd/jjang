# 보안 규칙

## SQL: Prepared Statement 필수, 사용자 입력 직접 쿼리 삽입 금지
## XSS: 출력 시 htmlspecialchars(), JS 삽입 시 json_encode()
## CSRF: 폼 전송 시 고도몰 내장 CSRF 토큰 포함
## 파일 업로드: 확장자 화이트리스트, 파일명 랜덤화, 실행 권한 제거
## 금지: rm -rf /, DROP TABLE/DATABASE 직접 실행
