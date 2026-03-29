param($outDir = C:\Users\jj1\.claude\output\seo)
function Get-NaverCat($c, $n) {
    if ($c -match "^005") { return "50001433" }
    elseif ($c -match "^039") { return "50005248" }
    elseif ($c -match "^006") { return "50001560" }
    elseif ($c -match "^021") { return "50001556" }
    elseif ($c -eq "") { if ($n -match "암가드|풋가드|핸드가드|손등가드") { return "50001433" } }
    return "50001437"
}
function Get-Player($n) {
    if ($n -match "([가-힣]{2,6}(?:\s[가-힣]{2,6})*)\s*선수모델") { return $Matches[1].Trim() }
    return ""
}
function Get-Title($n) {
    if ($n -match "암가드") { $p="암가드" }
    elseif ($n -match "풋가드") { $p="풋가드" }
    elseif ($n -match "손등가드|핸드가드") { $p="손등가드" }
    elseif ($n -match "수비장갑") { $p="수비장갑" }
    elseif ($n -match "글러브") { $p="글러브" }
    elseif ($n -match "트레이닝 바지|팬츠") { $p="트레이닝팬츠" }
    elseif ($n -match "자켓|후드") { $p="트레이닝자켓" }
    else { $p="" }
    if ($n -match "골드") { $b="골드" }
    elseif ($n -match "SSK") { $b="SSK" }
    elseif ($n -match "미즈노") { $b="미즈노" }
    else { $b="" }
    $core = ("b p").Trim()
