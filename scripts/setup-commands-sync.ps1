$gdrive = "C:\Users\NO\내 드라이브\claude\짱베이스볼\commands"
$local = "C:\Users\NO\.claude\commands"

# Google Drive에 폴더 생성 및 파일 복사
if (-not (Test-Path $gdrive)) {
    New-Item -ItemType Directory -Path $gdrive -Force | Out-Null
}
Copy-Item -Path "$local\*" -Destination $gdrive -Force
Write-Host "Google Drive copy done"

# 로컬 폴더 삭제
Remove-Item -Path $local -Recurse -Force
Write-Host "Local folder removed"

# Junction 생성
New-Item -ItemType Junction -Path $local -Target $gdrive | Out-Null
Write-Host "Junction created"

# 결과 확인
Get-ChildItem $local | ForEach-Object { Write-Host $_.Name }
Write-Host "DONE"
