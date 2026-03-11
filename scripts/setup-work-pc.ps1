# ============================================
#  짱베이스볼 Google Drive 동기화 - 회사 PC 셋업
#  PowerShell에서 실행 (관리자 권한 불필요)
# ============================================

$ErrorActionPreference = "Stop"

# === 경로 설정 (회사 PC 환경에 맞게 수정) ===
$UserHome = $env:USERPROFILE
$GDrive = Join-Path $UserHome "내 드라이브\claude\짱베이스볼"
$ClaudeDir = Join-Path $UserHome ".claude"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  짱베이스볼 Google Drive 동기화 - 회사 PC" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Google Drive 폴더 확인
if (-not (Test-Path $GDrive)) {
    Write-Host "[오류] Google Drive 경로를 찾을 수 없습니다: $GDrive" -ForegroundColor Red
    Write-Host "Google Drive 데스크톱 앱 설치 후 동기화를 완료하세요." -ForegroundColor Yellow
    Write-Host "다운로드: https://www.google.com/drive/download/" -ForegroundColor Yellow
    exit 1
}

Write-Host "[확인] Google Drive 경로: $GDrive" -ForegroundColor Green

# .claude 폴더 존재 확인
if (-not (Test-Path $ClaudeDir)) {
    New-Item -ItemType Directory -Path $ClaudeDir -Force | Out-Null
    Write-Host "[생성] .claude 폴더 생성됨" -ForegroundColor Yellow
}

# === 폴더 Junction 생성 ===
$folders = @("agents", "rules", "knowledge", "output", "tasks", "scripts", "plans", "commands")

foreach ($folder in $folders) {
    $target = Join-Path $GDrive $folder
    $link = Join-Path $ClaudeDir $folder

    if (Test-Path $link) {
        $backup = Join-Path $ClaudeDir "_backup_work_pc"
        if (-not (Test-Path $backup)) { New-Item -ItemType Directory -Path $backup -Force | Out-Null }

        $item = Get-Item $link -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            $item.Delete()
        } else {
            Copy-Item $link -Destination (Join-Path $backup $folder) -Recurse -Force
            Remove-Item $link -Recurse -Force
        }
    }

    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    $count = (Get-ChildItem $link -File -ErrorAction SilentlyContinue).Count
    Write-Host "[OK] $folder -> Google Drive ($count 파일)" -ForegroundColor Green
}

# === 파일 HardLink 생성 ===
$files = @(
    @{ Name = "jjang.md"; Source = Join-Path $GDrive "jjang.md"; Dest = Join-Path $ClaudeDir "jjang.md" },
    @{ Name = "settings.json"; Source = Join-Path $GDrive "settings.json"; Dest = Join-Path $ClaudeDir "settings.json" },
    @{ Name = "session-log.txt"; Source = Join-Path $GDrive "session-log.txt"; Dest = Join-Path $ClaudeDir "session-log.txt" },
    @{ Name = "CLAUDE.md"; Source = Join-Path $GDrive "CLAUDE.md"; Dest = Join-Path $UserHome "CLAUDE.md" }
)

foreach ($file in $files) {
    if (Test-Path $file.Dest) {
        Remove-Item $file.Dest -Force
    }

    New-Item -ItemType HardLink -Path $file.Dest -Target $file.Source | Out-Null
    $size = (Get-Item $file.Dest).Length
    Write-Host "[OK] $($file.Name) -> Google Drive ($size bytes)" -ForegroundColor Green
}

# === MEMORY.md 링크 (프로젝트별 메모리) ===
Write-Host ""
Write-Host "[메모리 동기화]" -ForegroundColor Yellow

$memoryDir = Join-Path $GDrive "memory"
$projectPaths = @(
    @{ Name = "home"; ProjDir = "C--Users-$($env:USERNAME)"; File = "MEMORY-home.md" },
    @{ Name = "claude"; ProjDir = "c--Users-$($env:USERNAME)--claude"; File = "MEMORY-claude.md" }
)

foreach ($mem in $projectPaths) {
    $projMemDir = Join-Path $ClaudeDir "projects\$($mem.ProjDir)\memory"
    $source = Join-Path $memoryDir $mem.File
    $dest = Join-Path $projMemDir "MEMORY.md"

    if (Test-Path $source) {
        if (-not (Test-Path $projMemDir)) {
            New-Item -ItemType Directory -Path $projMemDir -Force | Out-Null
        }
        if (Test-Path $dest) { Remove-Item $dest -Force }
        New-Item -ItemType HardLink -Path $dest -Target $source | Out-Null
        Write-Host "[OK] MEMORY ($($mem.Name)) -> Google Drive" -ForegroundColor Green
    } else {
        Write-Host "[건너뜀] MEMORY ($($mem.Name)) - 소스 없음" -ForegroundColor DarkGray
    }
}

# === 검증 ===
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  설정 완료!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "동기화 항목:" -ForegroundColor Yellow
Write-Host "  [폴더] agents, rules, knowledge, output, tasks, scripts, plans, commands" -ForegroundColor White
Write-Host "  [파일] jjang.md, settings.json, session-log.txt, CLAUDE.md" -ForegroundColor White
Write-Host "  [메모리] MEMORY.md (프로젝트별)" -ForegroundColor White
Write-Host ""
Write-Host "세션 시작 시 동기화 상태가 자동 체크됩니다." -ForegroundColor Green
Write-Host ""
