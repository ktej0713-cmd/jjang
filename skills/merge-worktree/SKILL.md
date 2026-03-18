---
name: merge-worktree
description: 현재 워크트리 브랜치를 메인 브랜치에 squash-merge합니다. git 히스토리와 소스를 분석하여 구조화된 커밋 메시지를 작성합니다.
argument-hint: "[대상 브랜치]"
disable-model-invocation: true
---

# 워크트리 병합

현재 워크트리 브랜치를 대상 브랜치에 squash-merge하고, 구조화된 커밋 메시지를 생성합니다.

## 현재 컨텍스트

- Git 디렉토리: `!git rev-parse --git-dir`
- 현재 브랜치: `!git branch --show-current`
- 최근 커밋: `!git log --oneline -20`
- 워킹 트리 상태: `!git status --short`

## 지침

아래 단계를 순서대로 정확히 수행합니다. 단계를 건너뛰지 않습니다.

---

### Phase 1: 유효성 검증

1. **워크트리 확인**: `git rev-parse --git-dir` 출력에 `/worktrees/`가 포함되어야 합니다. 아니라면 즉시 중단:
   > "이 스킬은 git 워크트리 안에서 실행해야 합니다."

2. **현재 브랜치 확인**: `git branch --show-current`로 워크트리 브랜치명을 가져옵니다.

3. **대상 브랜치 결정**:
   - `$ARGUMENTS`가 있으면 대상 브랜치로 사용
   - 없으면 `main` 존재 여부 확인, 없으면 `master` 확인. 둘 다 없으면 사용자에게 질문

4. **원본 저장소 경로 확인**: `git rev-parse --git-common-dir`로 원본 저장소 경로를 파악합니다.

5. **클린 워킹 트리 확인**: `git status --porcelain` 실행. 커밋되지 않은 변경이 있으면 사용자에게 커밋/스태시를 요청하고 중단합니다.

---

### Phase 2: 변경사항 분석

가장 중요한 단계입니다. 커밋 메시지를 작성하기 전에 변경 내용을 깊이 이해해야 합니다.

1. **커밋 히스토리**: `git log --oneline <target>..HEAD`

2. **파일 변경 요약**: `git diff <target>...HEAD --stat`

3. **전체 diff**: `git diff <target>...HEAD`를 읽고 주의 깊게 분석합니다.

4. **주요 파일 읽기**: 가장 크게 변경된 파일, 신규 파일, 삭제 파일을 Read 도구로 전체 맥락을 파악합니다.

5. **변경 분류**:
   - feat: 새 기능
   - fix: 버그 수정
   - refactor: 구조 변경 (동작 변화 없음)
   - content: 상세페이지/기획전 콘텐츠
   - config: 설정/도구 변경
   - docs: 문서 변경

6. **주요 타입 결정**: 전체 작업을 대표하는 타입을 결정합니다.

---

### Phase 3: 대상 브랜치 준비

1. 원본 저장소에서 대상 브랜치 최근 커밋 확인: `git -C <원본경로> log --oneline -10 <target>`

2. **WIP 커밋 탐지**: 대상 브랜치에 `wip:`, `auto-commit` 등의 자동 생성 커밋이 있으면 사용자에게 경고합니다.

3. **최신 상태 동기화**: 리모트가 있으면 `git -C <원본경로> fetch origin <target> 2>/dev/null`

---

### Phase 4: Squash Merge 실행

1. 원본 저장소에서 대상 브랜치 체크아웃:
   ```
   git -C <원본경로> checkout <target>
   ```

2. Squash merge 실행:
   ```
   git -C <원본경로> merge --squash <워크트리브랜치>
   ```

3. **충돌 처리**: 충돌 발생 시 충돌 파일 목록과 마커를 보여주고 사용자에게 보고합니다. 자동 해결을 시도하지 않습니다.

---

### Phase 5: 커밋 메시지 작성 및 커밋

Phase 2 분석을 바탕으로 다음 구조로 커밋 메시지를 작성합니다:

```
<type>: <72자 이내 명령형 요약>

<2-4문장으로 무엇을 왜 했는지 설명. 동기와 접근법 중심.>

Changes:
- <변경사항 그룹별 불릿 포인트>
- <하위 항목은 들여쓰기>

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**규칙:**
- type: `feat`, `fix`, `refactor`, `content`, `config`, `docs` 중 하나
- 요약: 명령형, 마침표 없이, 최대 72자
- 본문: '왜'와 '맥락' 설명
- Changes: 관련 항목 그룹화, 중요한 것부터

```bash
git -C <원본경로> commit -m "$(cat <<'EOF'
<커밋 메시지>
EOF
)"
```

---

### Phase 6: 검증

1. `git -C <원본경로> log --oneline -3`으로 커밋 확인

2. 사용자에게 보고:
   - 최종 커밋 해시
   - 커밋 요약
   - 병합 대상 브랜치
   - 워크트리 삭제 안내: `git worktree remove <경로>`
   - push 안내

---

## 주의사항

- force-push나 파괴적 git 명령은 사용자 확인 없이 절대 실행하지 않습니다.
- pre-commit hook을 건너뛰지 않습니다 (`--no-verify` 금지).
- 예상치 못한 상황에서는 추측하지 말고 중단 후 설명합니다.
