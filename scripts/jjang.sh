#!/bin/bash
# 짱베이스볼 자동화 런처 (jjang CLI)
# 사용법: bash ~/.claude/scripts/jjang.sh [명령]

CLAUDE_DIR="$HOME/.claude"
OUTPUT_DIR="$HOME/output"
SCRIPTS_DIR="$CLAUDE_DIR/scripts"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

show_banner() {
    echo -e "${CYAN}"
    echo "  ⚾ 짱베이스볼 자동화 시스템"
    echo "  ================================"
    echo -e "${NC}"
}

show_help() {
    show_banner
    echo -e "${GREEN}사용 가능한 명령:${NC}"
    echo ""
    echo -e "  ${YELLOW}MD팀 작업${NC}"
    echo "    campaign <이름>     기획전 기획 (MD팀 병렬 투입)"
    echo "    product <상품명>    상품 상세페이지 생성"
    echo "    category            카테고리 구조 분석/제안"
    echo "    season              이번 달 시즌 전략 브리핑"
    echo ""
    echo -e "  ${YELLOW}모니터링${NC}"
    echo "    monitor-seo         SEO 키워드 순위 체크"
    echo "    monitor-competitor  경쟁몰 가격/상품 모니터링"
    echo "    monitor-all         전체 모니터링 실행"
    echo ""
    echo -e "  ${YELLOW}콘텐츠 자동화${NC}"
    echo "    batch-product       상품 일괄 상세페이지 생성"
    echo "    batch-seo           SEO 메타태그 일괄 생성"
    echo ""
    echo -e "  ${YELLOW}스마트스토어${NC}"
    echo "    smartstore <mode>   상품 일괄 수정 (all|api|selenium)"
    echo "      옵션: --dry-run  시뮬레이션 모드"
    echo ""
    echo -e "  ${YELLOW}시스템${NC}"
    echo "    team                에이전트 팀 소집"
    echo "    status              현재 자동화 상태 확인"
    echo "    schedule            예약 작업 확인/설정"
    echo ""
}

# 기획전 자동화: MD팀 병렬 투입
run_campaign() {
    local name="${1:-시즌기획전}"
    echo -e "${BLUE}[기획전] ${name} - MD팀 병렬 투입 시작${NC}"
    claude -p "
짱베이스볼 기획전을 기획해주세요.
기획전명: ${name}

소싱/콘텐츠/구조/프로모션 MD를 병렬로 투입하고,
완료 후 고객검증 MD가 최종 검증해주세요.

결과물은 output 폴더에 HTML로 생성해주세요.
" --model opus
}

# 상품 상세페이지 자동 생성
run_product() {
    local product="${1:-글러브}"
    echo -e "${BLUE}[상품] ${product} - 상세페이지 생성${NC}"
    claude -p "
짱베이스볼 상품 상세페이지를 만들어주세요.
상품: ${product}

콘텐츠 MD가 8단계 표준 구조로 작성하고,
SEO전문가가 메타태그를 최적화하고,
스킨디자이너가 HTML을 생성해주세요.

결과물은 output/product-pages/ 에 HTML로 저장.
"
}

# 시즌 전략 브리핑
run_season() {
    local month=$(date +%-m)
    echo -e "${BLUE}[시즌] ${month}월 전략 브리핑${NC}"
    claude -p "
현재 ${month}월입니다.
knowledge/seasonal-calendar.md 기반으로 이번 달 짱베이스볼 전략을 브리핑해주세요.

포함 항목:
1. 이번 달 핵심 이벤트
2. 주력 상품 TOP 5
3. 추천 기획전 2~3개
4. 프로모션 키워드
5. 경쟁몰 대비 차별화 포인트

MD팀 병렬 투입으로 작업해주세요.
" --model opus
}

# SEO 모니터링
run_monitor_seo() {
    echo -e "${BLUE}[SEO] 키워드 모니터링 시작${NC}"
    claude -p "
짱베이스볼 핵심 키워드의 네이버 쇼핑 노출 상태를 분석해주세요.

핵심 키워드:
- 야구글러브, 야구배트, 야구화, 야구장갑
- 미즈노글러브, SSK글러브, 윌슨글러브
- 사회인야구 장비, 유소년야구 장비

각 키워드별로:
1. 예상 검색량 트렌드
2. 짱베이스볼 SEO 최적화 제안
3. 메타태그 개선안

결과를 output/seo-reports/ 에 HTML로 저장.
"
}

# 경쟁몰 모니터링
run_monitor_competitor() {
    echo -e "${BLUE}[경쟁] 경쟁몰 모니터링 시작${NC}"
    claude -p "
짱베이스볼 경쟁몰 현황을 분석해주세요.
knowledge/competitor-tracking.md 기반으로 업데이트하고,

체크 항목:
1. 경쟁몰 신규 기획전/이벤트
2. 가격 변동 감지 (주요 상품)
3. 신규 입점 브랜드
4. 차별화 기회 포인트

소싱 MD + 구조 MD 병렬 투입.
결과를 output/competitor-reports/ 에 저장.
"
}

# 에이전트 팀 소집
run_team() {
    echo -e "${BLUE}[팀] MD팀 소집${NC}"
    claude --model opus -w "md-team-$(date +%Y%m%d)"
}

# 상태 확인
run_status() {
    show_banner
    echo -e "${GREEN}환경 상태:${NC}"
    echo "  Node.js: $(node -v 2>/dev/null || echo 'N/A')"
    echo "  Python:  $(python --version 2>/dev/null || echo 'N/A')"
    echo "  Git:     $(git --version 2>/dev/null || echo 'N/A')"
    echo ""
    echo -e "${GREEN}에이전트 ($(ls "$CLAUDE_DIR/agents/" 2>/dev/null | wc -l)개):${NC}"
    ls "$CLAUDE_DIR/agents/" 2>/dev/null | sed 's/.md$//' | while read agent; do
        echo "  - $agent"
    done
    echo ""
    echo -e "${GREEN}지식 베이스 ($(ls "$CLAUDE_DIR/knowledge/" 2>/dev/null | wc -l)개):${NC}"
    ls "$CLAUDE_DIR/knowledge/" 2>/dev/null | sed 's/.md$//' | while read kb; do
        echo "  - $kb"
    done
    echo ""
    echo -e "${GREEN}최근 결과물:${NC}"
    find "$OUTPUT_DIR" -name "*.html" -mtime -7 2>/dev/null | head -10 | while read f; do
        echo "  - $(basename $f) ($(date -r "$f" '+%m/%d %H:%M'))"
    done
    echo ""
}

# 카테고리 분석
run_category() {
    echo -e "${BLUE}[카테고리] 구조 분석 시작${NC}"
    claude -p "
짱베이스볼 카테고리 구조를 분석하고 개선안을 제시해주세요.

구조 MD + SEO전문가 병렬 투입.
- 현재 카테고리 3depth 구조 점검
- 네이버 쇼핑 카테고리 매핑 확인
- SEO 키워드 포함 여부 체크
- 개선 권고사항

결과를 output/category-analysis/ 에 HTML로 저장.
"
}

# 스마트스토어 상품 일괄 수정
run_smartstore() {
    local mode="${1:-all}"
    local extra_args="${@:2}"
    echo -e "${BLUE}[스마트스토어] 상품 일괄 수정 (모드: ${mode})${NC}"
    python "$CLAUDE_DIR/automation/smartstore-updater/main.py" --mode "$mode" $extra_args
}

# 메인 라우터
case "${1}" in
    campaign)    run_campaign "${@:2}" ;;
    product)     run_product "${@:2}" ;;
    category)    run_category ;;
    season)      run_season ;;
    monitor-seo) run_monitor_seo ;;
    monitor-competitor) run_monitor_competitor ;;
    monitor-all)
        run_monitor_seo
        run_monitor_competitor
        ;;
    smartstore)  run_smartstore "${@:2}" ;;
    team)        run_team ;;
    status)      run_status ;;
    help|--help|-h|"") show_help ;;
    *)
        echo -e "${RED}알 수 없는 명령: ${1}${NC}"
        echo "  'bash ~/.claude/scripts/jjang.sh help' 으로 도움말 확인"
        ;;
esac
