# jjang-md-team 태스크 관리

## 태스크 파일 구조
각 태스크는 `task-{번호}.md` 파일로 관리한다.

## 태스크 상태
```
pending → assigned → in_progress → review → completed
                                      ↓
                                    failed → escalated
```

## 태스크 템플릿
```markdown
# TASK-{번호}: {제목}

- 상태: pending | assigned | in_progress | review | completed | failed
- 담당: {에이전트명}
- 우선순위: 긴급 | 높음 | 보통 | 낮음
- 생성일: YYYY-MM-DD
- 마감일: YYYY-MM-DD (있을 경우)
- 의존성: TASK-{번호} (선행 작업이 있을 경우)

## 요청 내용
{구체적인 작업 설명}

## 산출물
{기대하는 결과물}

## 진행 기록
- [날짜] {진행 내용}

## 검증 결과
- 고객검증 MD: PASS / 수정필요 / FAIL
- 사유: {검증 코멘트}
```

## 운영 규칙
1. Lead MD가 태스크를 생성하고 담당자를 지정한다
2. 담당 에이전트가 상태를 in_progress로 변경하고 작업한다
3. 작업 완료 시 review로 변경하고 검증을 요청한다
4. 고객검증 MD가 PASS 판정 시 completed로 변경한다
5. FAIL 시 피드백과 함께 담당자에게 반려한다
