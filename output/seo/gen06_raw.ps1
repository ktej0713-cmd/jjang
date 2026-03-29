$outDir = 'C:\Users\jj1\.claude\output\seo'
function Get-NaverCat($c, $n) {
    if ($c -match '^005') { return '50001433' }
    elseif ($c -match '^039') { return '50005248' }
    elseif ($c -match '^006') { return '50001560' }
    elseif ($c -match '^021') { return '50001556' }
    elseif ($c -eq '') { if ($n -match '암가드|풋가드|핸드가드|손등가드') { return '50001433' } }
    return '50001437'
}
function Get-Player($n) {
    if ($n -match '([가-힣]{2,6}(?:\s[가-힣]{2,6})*)\s*선수모델') { return $Matches[1].Trim() }
    return ''
}
function Get-Title($n) {
    if ($n -match '암가드') { $p='암가드' } elseif ($n -match '풋가드') { $p='풋가드' }
    elseif ($n -match '손등가드|핸드가드') { $p='손등가드' } elseif ($n -match '수비장갑') { $p='수비장갑' }
    elseif ($n -match '글러브') { $p='글러브' } elseif ($n -match '트레이닝 바지|팬츠') { $p='트레이닝팬츠' }
    elseif ($n -match '자켓|후드') { $p='트레이닝자켓' } else { $p='' }
    if ($n -match '골드') { $b='골드' } elseif ($n -match 'SSK') { $b='SSK' }
    elseif ($n -match '미즈노') { $b='미즈노' } else { $b='' }
    $core = ($b+' '+$p).Trim(); if ($core.Length -gt 12) { $core=$core.Substring(0,12) }
    return $core+' | 짱베이스볼'
}
function Get-SearchKw($n, $mn) {
    $pl=Get-Player $n; $k=[System.Collections.Generic.List[string]]::new()
    if ($n -match '골드') { $k.Add('골드'); $k.Add('GOLD야구') }
    elseif ($n -match 'SSK') { $k.Add('SSK'); $k.Add('사사키'); $k.Add('SSK야구') }
    elseif ($n -match '미즈노') { $k.Add('미즈노'); $k.Add('MIZUNO'); $k.Add('미즈노야구') }
    if ($n -match '암가드') {
        $k.Add('암가드'); $k.Add('야구암가드'); $k.Add('타자암가드'); $k.Add('팔꿈치보호대'); $k.Add('야구보호장비')
        if ($pl) { $k.Add($pl+'암가드'); $k.Add($pl+'선수모델') }
        $k.Add('골드암가드'); $k.Add('G쉴드암가드'); $k.Add('KBO암가드')
    } elseif ($n -match '풋가드') {
        $k.Add('풋가드'); $k.Add('야구풋가드'); $k.Add('발등보호대'); $k.Add('발보호대'); $k.Add('야구보호장비')
        if ($pl) { $k.Add($pl+'풋가드'); $k.Add($pl+'선수모델') }
        $k.Add('골드풋가드'); $k.Add('G쉴드풋가드'); $k.Add('KBO풋가드')
    } elseif ($n -match '손등가드|핸드가드') {
        $k.Add('손등가드'); $k.Add('핸드가드'); $k.Add('야구손등가드'); $k.Add('야구핸드가드'); $k.Add('야구보호장비')
        if ($pl) { $k.Add($pl+'손등가드'); $k.Add($pl+'선수모델') }
        $k.Add('골드손등가드'); $k.Add('G쉴드핸드가드')
    } elseif ($n -match '수비장갑') {
        $k.Add('수비장갑'); $k.Add('야구장갑'); $k.Add('미즈노장갑'); $k.Add('유소년야구장갑'); $k.Add('야구수비장갑'); $k.Add('유소년수비장갑'); $k.Add('어린이야구장갑')
    } elseif ($n -match '글러브') {
        $k.Add('야구글러브'); $k.Add('미즈노글러브'); $k.Add('연식글러브'); $k.Add('아동글러브'); $k.Add('유소년글러브'); $k.Add('키즈글러브'); $k.Add('아동야구글러브'); $k.Add('어린이글러브')
    } elseif ($n -match '트레이닝 바지|팬츠') {
        $k.Add('트레이닝팬츠'); $k.Add('야구바지'); $k.Add('기모바지'); $k.Add('SSK트레이닝'); $k.Add('동계야구바지'); $k.Add('야구훈련바지')
    } elseif ($n -match '자켓|후드') {
        $k.Add('트레이닝자켓'); $k.Add('야구자켓'); $k.Add('기모자켓'); $k.Add('SSK자켓'); $k.Add('동계야구자켓'); $k.Add('야구후드자켓')
    }
    if ($mn) { $k.Add($mn) }
    $r = $k -join ','; while ($r.Length -gt 250 -and $k.Count -gt 1) { $k.RemoveAt($k.Count-1); $r=$k -join ',' }
    return $r
}
function Get-Desc($n) {
    $pl=Get-Player $n
    if ($n -match '암가드') {
        if ($pl) { $d='골드 2025 G쉴드 어센틱 '+$pl+' 선수모델 암가드. KBO 선수 동일 사양의 타석용 보호장비입니다.' }
        else { $d='골드 2025 G쉴드 어센틱 암가드. KBO 선수 동일 사양의 타석용 보호장비입니다.' }
    } elseif ($n -match '풋가드') {
        if ($pl) { $d='골드 2025 G쉴드 어센틱 '+$pl+' 선수모델 풋가드. 발등을 보호하는 타석용 보호장비입니다.' }
        else { $d='골드 2025 G쉴드 어센틱 풋가드. 발등을 보호하는 타석용 보호장비입니다.' }
    } elseif ($n -match '손등가드|핸드가드') {
        if ($pl) { $d='골드 2025 G쉴드 어센틱 '+$pl+' 선수모델 손등가드. KBO 선수 동일 사양의 핸드가드입니다.' }
        else { $d='골드 2025 G쉴드 어센틱 손등가드. KBO 선수 동일 사양의 핸드가드입니다.' }
    } elseif ($n -match '수비장갑') { $d='미즈노 유소년 야구 수비장갑. 어린이 손에 맞는 사이즈로 수비 시 안전하게 착용 가능합니다.' }
    elseif ($n -match '글러브') { $d='미즈노 아동용 연식 와일드 키즈 올라운드 글러브. 9인치 소형 사이즈로 유소년 야구 입문용입니다.' }
    elseif ($n -match '트레이닝 바지|팬츠') { $d='SSK 동계 기모 경량 트레이닝 바지. 보온성과 활동성을 동시에 갖춘 야구 동계 훈련용 팬츠입니다.' }
    elseif ($n -match '자켓|후드') { $d='SSK 동계 기모 경량 풀집업 후드 트레이닝 자켓. 보온성과 활동성을 동시에 갖춘 야구 동계 훈련용입니다.' }
    else { $d=$n+'. 짱베이스볼에서 만나보세요.' }
    if ($d.Length -gt 80) { $d=$d.Substring(0,79)+'.' }
    return $d
}
function Get-SeoKw($n, $mn) {
    $pl=Get-Player $n; $k=[System.Collections.Generic.List[string]]::new()
    if ($n -match '골드') { $k.Add('골드야구') } elseif ($n -match 'SSK') { $k.Add('SSK야구') } elseif ($n -match '미즈노') { $k.Add('미즈노야구') }
    if ($n -match '암가드') { $k.Add('암가드'); $k.Add('야구보호장비'); $k.Add('타자보호대'); if ($pl) { $k.Add($pl+'선수모델') }; $k.Add('G쉴드'); $k.Add('KBO야구') }
    elseif ($n -match '풋가드') { $k.Add('풋가드'); $k.Add('야구보호장비'); $k.Add('발등보호대'); if ($pl) { $k.Add($pl+'선수모델') }; $k.Add('G쉴드'); $k.Add('KBO야구') }
    elseif ($n -match '손등가드|핸드가드') { $k.Add('손등가드'); $k.Add('핸드가드'); $k.Add('야구보호장비'); if ($pl) { $k.Add($pl+'선수모델') }; $k.Add('G쉴드') }
    elseif ($n -match '수비장갑') { $k.Add('수비장갑'); $k.Add('야구장갑'); $k.Add('유소년야구'); $k.Add('어린이야구장갑') }
    elseif ($n -match '글러브') { $k.Add('야구글러브'); $k.Add('연식글러브'); $k.Add('유소년글러브'); $k.Add('아동야구'); $k.Add('키즈글러브') }
    elseif ($n -match '트레이닝 바지|팬츠') { $k.Add('트레이닝팬츠'); $k.Add('야구바지'); $k.Add('기모바지'); $k.Add('동계훈련') }
    elseif ($n -match '자켓|후드') { $k.Add('트레이닝자켓'); $k.Add('야구자켓'); $k.Add('기모자켓'); $k.Add('동계훈련') }
    if ($mn) { $k.Add($mn) }
    return ($k | Select-Object -First 10) -join ','
}
function Get-NaverTag($n) {
    $pl=Get-Player $n; $t=[System.Collections.Generic.List[string]]::new()
    if ($n -match '골드') { $t.Add('골드야구'); $t.Add('G쉴드') }
    elseif ($n -match 'SSK') { $t.Add('SSK야구'); $t.Add('사사키') }
    elseif ($n -match '미즈노') { $t.Add('미즈노야구'); $t.Add('미즈노') }
    if ($n -match '암가드') { $t.Add('암가드'); $t.Add('야구보호장비'); if ($pl) { $t.Add($pl) } }
    elseif ($n -match '풋가드') { $t.Add('풋가드'); $t.Add('야구보호장비'); if ($pl) { $t.Add($pl) } }
    elseif ($n -match '손등가드|핸드가드') { $t.Add('손등가드'); $t.Add('핸드가드'); if ($pl) { $t.Add($pl) } }
    elseif ($n -match '수비장갑') { $t.Add('수비장갑'); $t.Add('야구장갑'); $t.Add('유소년야구') }
    elseif ($n -match '글러브') { $t.Add('야구글러브'); $t.Add('아동글러브'); $t.Add('유소년야구') }
    elseif ($n -match '트레이닝 바지|팬츠') { $t.Add('트레이닝팬츠'); $t.Add('야구바지'); $t.Add('동계훈련') }
    elseif ($n -match '자켓|후드') { $t.Add('트레이닝자켓'); $t.Add('야구자켓'); $t.Add('동계훈련') }
    $r=$t -join '|'; while ($r.Length -gt 100 -and $t.Count -gt 1) { $t.RemoveAt($t.Count-1); $r=$t -join '|' }
    return $r
}
function Get-NaverAttr($n) {
    $a=[System.Collections.Generic.List[string]]::new()
    if ($n -match '골드') { $a.Add('브랜드:골드(GOLD)') } elseif ($n -match 'SSK') { $a.Add('브랜드:SSK') } elseif ($n -match '미즈노') { $a.Add('브랜드:미즈노(MIZUNO)') }
    $a.Add('종목:야구')
    if ($n -match '암가드') { $a.Add('품목:암가드') } elseif ($n -match '풋가드') { $a.Add('품목:풋가드') }
    elseif ($n -match '손등가드|핸드가드') { $a.Add('품목:핸드가드') }
    elseif ($n -match '수비장갑') { $a.Add('품목:수비장갑'); if ($n -match '유소년') { $a.Add('대상:유소년') } }
    elseif ($n -match '글러브') { $a.Add('품목:글러브'); if ($n -match '아동|키즈') { $a.Add('대상:아동') } }
    elseif ($n -match '트레이닝 바지|팬츠') { $a.Add('품목:트레이닝바지'); $a.Add('소재:기모') }
    elseif ($n -match '자켓|후드') { $a.Add('품목:트레이닝자켓'); $a.Add('소재:기모') }
    if ($n -match '2025') { $a.Add('시즌:2025') }
    return $a -join '|'
}
$products = @(
  @{g='49161';n='골드 2025 G쉴드 어센틱 고승민 선수모델 암가드 화이트/블랙';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49160';n='골드 2025 G쉴드 어센틱 레이예스 선수모델 손등가드 핸드가드 레드/네이비';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49159';n='골드 2025 G쉴드 어센틱 레이예스 선수모델 풋가드 레드/네이비';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49158';n='골드 2025 G쉴드 어센틱 레이예스 선수모델 암가드 네이비/레드';m='G쉴드';mk='골드(GOLD)';c=''},
  @{g='49157';n='골드 2025 G쉴드 어센틱 윤도현 김태진 선수모델 손등가드 핸드가드 블랙';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49156';n='골드 2025 G쉴드 어센틱 김태진 선수모델 풋가드 블랙/화이트';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49155';n='골드 2025 G쉴드 어센틱 김태진 선수모델 암가드 블랙/화이트';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49154';n='골드 2025 G쉴드 어센틱 황성빈 선수모델 손등가드 핸드가드 블랙';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49153';n='골드 2025 G쉴드 어센틱 황성빈 선수모델 풋가드 블랙';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49152';n='골드 2025 G쉴드 어센틱 황성빈 선수모델 암가드 블랙';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49151';n='골드 2025 G쉴드 어센틱 오스틴 선수모델 손등가드 핸드가드 레드';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49150';n='골드 2025 G쉴드 어센틱 오스틴 선수모델 풋가드 레드/골드';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49149';n='골드 2025 G쉴드 어센틱 오스틴 선수모델 암가드 레드/골드';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49148';n='골드 2025 G쉴드 어센틱 김도영 선수모델 손등가드 핸드가드 화이트/레드';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49147';n='골드 2025 G쉴드 어센틱 김도영 선수모델 풋가드 화이트/레드';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49146';n='골드 2025 G쉴드 어센틱 김도영 선수모델 싱글 암가드 화이트/레드';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49144';n='골드 2025 G쉴드 어센틱 노시환 선수모델 풋가드 화이트/그레이';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49143';n='골드 2025 G쉴드 어센틱 노시환 선수모델 암가드 화이트/그레이';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49142';n='골드 2025 G쉴드 어센틱 김태연 선수모델 손등가드 핸드가드 오렌지/네이비';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49141';n='골드 2025 G쉴드 어센틱 김태연 선수모델 풋가드 오렌지/네이비';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49140';n='골드 2025 G쉴드 어센틱 김태연 선수모델 암가드 오렌지/네이비';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49139';n='골드 2025 G쉴드 어센틱 데이비슨 김형준 선수모델 손등가드 핸드가드 화이트/네이비';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49138';n='골드 2025 G쉴드 어센틱 데이비슨 선수모델 풋가드 화이트';m='G쉴드';mk='골드(GOLD)';c=''},
  @{g='49137';n='골드 2025 G쉴드 어센틱 데이비슨 선수모델 암가드 화이트';m='G쉴드';mk='골드(GOLD)';c=''},
  @{g='49136';n='골드 2025 G쉴드 어센틱 박건우 선수모델 손등가드 핸드가드 블랙';m='G쉴드';mk='골드(GOLD)';c=''},
  @{g='49135';n='골드 2025 G쉴드 어센틱 박건우 선수모델 풋가드 블랙/실버';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49134';n='골드 2025 G쉴드 어센틱 박건우 선수모델 암가드 블랙/실버';m='G쉴드';mk='골드(GOLD)';c=''},
  @{g='49133';n='골드 2025 G쉴드 어센틱 최주환 이도윤 선수모델 손등가드 핸드가드 화이트';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49132';n='골드 2025 G쉴드 어센틱 이도윤 선수모델 풋가드 화이트/오렌지';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49131';n='골드 2025 G쉴드 어센틱 이도윤 선수모델 암가드 화이트/오렌지';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49130';n='골드 2025 G쉴드 어센틱 김재성 선수모델 손등가드 핸드가드 블루/화이트';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49129';n='골드 2025 G쉴드 어센틱 김재성 선수모델 풋가드 블루/실버';m='G쉴드';mk='골드(GOLD)';c=''},
  @{g='49128';n='골드 2025 G쉴드 어센틱 김재성 선수모델 암가드 블루/실버';m='G쉴드';mk='골드(GOLD)';c=''},
  @{g='49127';n='골드 2025 G쉴드 어센틱 안치홍 선수모델 손등가드 핸드가드 화이트/블랙';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49126';n='골드 2025 G쉴드 어센틱 안치홍 선수모델 풋가드 화이트/블랙';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49125';n='골드 2025 G쉴드 어센틱 안치홍 선수모델 암가드 화이트/블랙';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49124';n='골드 2025 G쉴드 어센틱 노시환 배정대 선수모델 손등가드 핸드가드 화이트';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49123';n='골드 2025 G쉴드 어센틱 배정대 선수모델 풋가드 화이트';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49122';n='골드 2025 G쉴드 어센틱 배정대 선수모델 암가드 화이트';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49121';n='골드 2025 G쉴드 어센틱 김도영 선수모델 손등가드 핸드가드 블랙/레드';m='G쉴드';mk='골드(GOLD)';c='005013'},
  @{g='49120';n='골드 2025 G쉴드 어센틱 김도영 선수모델 풋가드 블랙/레드';m='G쉴드';mk='골드(GOLD)';c='005003'},
  @{g='49119';n='골드 2025 G쉴드 어센틱 김도영 선수모델 싱글 암가드 블랙/레드';m='G쉴드';mk='골드(GOLD)';c='005002'},
  @{g='49118';n='SSK 동계 기모 경량 트레이닝 바지 팬츠 DRF025P 블랙';m='DRF025P';mk='사사키(SSK)';c='039022002'},
  @{g='49117';n='SSK 동계 기모 경량 풀집업 후드 트레이닝 자켓 DRF024 네이비';m='DRF024';mk='사사키(SSK)';c='039022002'},
  @{g='49116';n='SSK 동계 기모 경량 풀집업 후드 트레이닝 자켓 DRF024 그레이';m='DRF024';mk='사사키(SSK)';c='039022002'},
  @{g='49115';n='SSK 동계 기모 경량 풀집업 후드 트레이닝 자켓 DRF024 블랙';m='DRF024';mk='사사키(SSK)';c='039022002'},
  @{g='49106';n='미즈노 유소년 야구 수비장갑 21062 레드/블랙 우투용';m='1EJEY21062';mk='미즈노(MIZUNO)';c='006002'},
  @{g='49105';n='미즈노 유소년 야구 수비장갑 21014 네이비/화이트 우투용';m='1EJEY21014NW';mk='미즈노(MIZUNO)';c='006002'},
  @{g='49073';n='미즈노 아동용 연식 와일드 키즈 올라운드 글러브 9인치 5S 33900 블랙';m='1AJGY3390009ARBK';mk='미즈노(MIZUNO)';c='021001'},
  @{g='49070';n='미즈노 아동용 연식 와일드 키즈 올라운드 글러브 9인치 5S 33900 오렌지';m='1AJGY339005109ARBK';mk='미즈노(MIZUNO)';c='021001'}
)

$cnt=0
foreach ($p in $products) {
    $nm=$p.n; $gno=$p.g; $mk=$p.mk; $mn=$p.m; $cd=$p.c
    $mkS = if ($mk.Length -gt 30) { $mk.Substring(0,30) } else { $mk }
    $data=[ordered]@{
        goodsNo=$gno; goodsNm=$nm
        searchKeyword=(Get-SearchKw $nm $mn)
        seoTitle=(Get-Title $nm)
        seoDescription=(Get-Desc $nm)
        seoKeyword=(Get-SeoKw $nm $mn)
        naverSearchTag=(Get-NaverTag $nm)
        naverAttribute=(Get-NaverAttr $nm)
        manufacturer=$mkS; meta_author='짱베이스볼'
        naverCategory=(Get-NaverCat $cd $nm)
    }
    $json=$data | ConvertTo-Json -Depth 5
    $fp=Join-Path $outDir ('seo_data_'+$gno+'.json')
    [System.IO.File]::WriteAllText($fp, $json, [System.Text.Encoding]::UTF8)
    $cnt++; Write-Host ('OK seo_data_'+$gno+'.json')
}
Write-Host ('완료: '+$cnt)
