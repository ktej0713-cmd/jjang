# 보안 규칙

## 고도몰 코어 보호
- 고도몰 코어 파일(core/, vendor/, framework/)은 절대 직접 수정 금지
- module/ 내에서 이벤트 리스너/서비스 오버라이드로 확장
- 코어 변경이 필요한 경우 반드시 사용자에게 확인

## SQL 보안
- Prepared Statement 필수 (Doctrine ORM 권장)
- 사용자 입력값 직접 쿼리 삽입 절대 금지
- DB 권한은 최소 권한 원칙 적용

## XSS 방지
- 사용자 입력 출력 시 htmlspecialchars() 필수
- JavaScript에 사용자 데이터 삽입 시 json_encode() 사용
- Content-Security-Policy 헤더 설정 권장

## CSRF 방지
- 폼 전송 시 CSRF 토큰 포함
- 고도몰 내장 CSRF 토큰 활용

## 파일 업로드
- 허용 확장자 화이트리스트 방식
- 업로드 파일명 랜덤 변환
- 업로드 디렉토리 실행 권한 제거

## 금지 명령어
- rm -rf /, rm -rf ~
- DROP TABLE, DROP DATABASE (직접 실행 금지)
