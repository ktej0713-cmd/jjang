# 회사 ↔ 집 Claude Code 작업 공유 플랜

## Context
회사 PC와 집 PC에서 각각 Claude Code를 사용 중이며, 두 환경 간 작업 내용을 실시간 동기화하고 싶음.
공유 대상: 에이전트 정의, 규칙, 지식 베이스, 메모리(MEMORY.md), 생성 결과물, 태스크 현황.

---

## 접근 방법: GitHub Private Repository

`~/.claude/` 폴더를 GitHub 비공개 저장소로 관리한다.
두 PC 모두 같은 저장소를 clone하여 push/pull로 동기화.

---

## 공유 대상 파일 (git에 포함)

| 폴더/파일 | 이유 |
|-----------|------|
| `agents/` | 에이전트 10개 정의 |
| `rules/` | brand-voice, copywriting 등 6개 규칙 |
| `knowledge/` | 지식 베이스 (브랜드, 경쟁사, 템플릿 등) |
| `output/` | 생성된 HTML 결과물 |
| `tasks/` | 태스크 진행 현황 |
| `commands/` | 커스텀 명령어 |
| `jjang.md` | MD팀 운영 가이드 |
| `settings.json` | 설정 (credentials 제외) |
| `projects/C--Users-jj1/memory/MEMORY.md` | 세션 간 메모리 |
| `~/CLAUDE.md` | 프로젝트 지시 파일 |

## 제외 파일 (.gitignore)

```
.credentials.json        # API 키/토큰 - 절대 공유 금지
history.jsonl            # 세션 기록 - 기기별 독립
projects/**/*.jsonl      # 대화 로그 - 용량 크고 기기별 독립
projects/**/subagents/   # 서브에이전트 로그
cache/
debug/
telemetry/
shell-snapshots/
session-env/
backups/
downloads/
file-history/
ide/
mcp-needs-auth-cache.json
session-log.txt
*.lock
```

---

## 구현 단계

### Step 1: GitHub에 비공개 저장소 생성
- 저장소명: `jjang-claude-config` (Private)
- GitHub 계정 필요

### Step 2: 회사 PC — git 초기화
```bash
cd ~/.claude
git init
# .gitignore 생성 (위 내용)
git add .
git commit -m "initial: 짱베이스볼 Claude Code 설정"
git remote add origin https://github.com/{계정}/jjang-claude-config.git
git push -u origin main
```

CLAUDE.md도 별도로:
```bash
cd ~
git init jjang-claude-md
cp CLAUDE.md jjang-claude-md/
cd jjang-claude-md && git add . && git commit -m "CLAUDE.md"
git remote add origin ... && git push
```
※ 또는 CLAUDE.md를 .claude/ 폴더로 이동하고 심볼릭 링크 처리

### Step 3: 집 PC — clone
```bash
# 집 PC ~/.claude 기존 내용 백업
mv ~/.claude ~/.claude.backup

# clone
git clone https://github.com/{계정}/jjang-claude-config.git ~/.claude
```

### Step 4: 일상 동기화 워크플로우
```bash
# 작업 시작 전 (최신 내용 받기)
cd ~/.claude && git pull

# 작업 후 (변경 내용 올리기)
cd ~/.claude && git add . && git commit -m "작업내용 메모" && git push
```

### Step 5 (선택): 자동 동기화 스크립트
- 회사 PC 퇴근 시: `jjang-push.bat` 실행
- 집 PC 시작 시: `jjang-pull.bat` 실행

`jjang-push.bat`:
```batch
cd %USERPROFILE%\.claude
git add .
git commit -m "auto: %date% %time%"
git push
```

`jjang-pull.bat`:
```batch
cd %USERPROFILE%\.claude
git pull
```

---

## 주의사항

- `.credentials.json` 은 **절대 git에 포함하지 않음** (Claude API 토큰)
- 집 PC에 Claude Code 설치 및 `claude login` 은 별도로 진행
- 두 PC에서 동시에 같은 파일 수정 시 충돌 발생 가능 → 한 번에 한 PC에서 작업 권장
- `output/` 폴더가 커지면 `.gitignore`에 추가하거나 Git LFS 사용 고려

---

## 검증 방법

1. 회사 PC에서 knowledge/ 파일 수정 → push
2. 집 PC에서 pull → 같은 내용 반영 확인
3. 집 PC에서 Claude Code 실행 → MEMORY.md, agents/ 정상 로드 확인
4. `/agents`로 에이전트 목록 확인
