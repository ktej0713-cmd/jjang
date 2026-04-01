#!/usr/bin/env node
// 상세페이지 HTML 생성기 — 짱베이스볼
// 사용법: node generate-detail-page.js <product-data.json>
// 출력: ~/.claude/output/ 에 HTML 파일 저장, 콘솔에 요약 출력

const fs = require('fs');
const path = require('path');

// ─── 설정 ───
const OUTPUT_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.claude', 'output');
const COLORS = { primary: '#1B2A4A', accent: '#D4A843', bg1: '#ffffff', bg2: '#F9F9F9', dark: '#1B2A4A' };

// ─── 데이터 읽기 ───
const dataFile = process.argv[2];
if (!dataFile) { console.error('Usage: node generate-detail-page.js <data.json>'); process.exit(1); }
const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const exclude = (data.exclude || []).map(s => s.toLowerCase());
const isIncluded = (sec) => !exclude.includes(sec.toLowerCase());

// ─── HTML 이스케이프 ───
const esc = (s) => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');

// ─── 섹션 제목 헬퍼 ───
const secTitle = (text) =>
  `<div style="border-left:4px solid ${COLORS.accent}; padding-left:16px; font-size:24px; font-weight:800; color:${COLORS.primary}; margin-bottom:28px;">${text}</div>`;

const secTitleWhite = (text) =>
  `<div style="border-left:4px solid ${COLORS.accent}; padding-left:16px; font-size:24px; font-weight:800; color:#ffffff; margin-bottom:24px;">${text}</div>`;

// ─── JSON-LD 생성 ───
function genProductSchema(p) {
  return JSON.stringify({
    "@context": "https://schema.org",
    "@type": "Product",
    "name": p.name,
    "alternateName": p.nameEn,
    "description": p.description,
    "brand": { "@type": "Brand", "name": p.brand },
    "sku": p.sku,
    "material": p.material,
    "color": p.color,
    "size": p.size,
    "category": p.category,
    "offers": {
      "@type": "Offer",
      "priceCurrency": "KRW",
      "price": p.price,
      "availability": "https://schema.org/InStock",
      "seller": { "@type": "Organization", "name": "짱베이스볼" }
    }
  }, null, 2);
}

function genFaqSchema(faqs) {
  return JSON.stringify({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.map(f => ({
      "@type": "Question",
      "name": f.q,
      "acceptedAnswer": { "@type": "Answer", "text": f.a }
    }))
  }, null, 2);
}

// ─── 섹션 생성기 ───

function genHero(d) {
  const h = d.hero;
  return `<!-- [SEC:히어로] -->
<div style="position:relative; background:#2C3E6B; text-align:center;">
  <div style="padding:120px 28px 40px; color:${COLORS.accent}; font-size:14px; letter-spacing:1px;">
    <span style="opacity:0.7;">[상품 이미지 영역 — 860 x 420px]</span>
  </div>
  <div style="background:rgba(27,42,74,0.92); padding:32px 28px 36px;">
    <div style="color:${COLORS.accent}; font-size:13px; font-weight:600; letter-spacing:2px; margin-bottom:8px;">${esc(h.tagline)}</div>
    <div style="color:#ffffff; font-size:28px; font-weight:800; line-height:1.3; margin-bottom:12px;">${esc(h.title)}</div>
    <div style="color:rgba(255,255,255,0.75); font-size:15px; font-weight:400;">${esc(h.subtitle)}</div>
  </div>
</div>
<div style="background:#ffffff; padding:28px 28px 20px;">
  <p style="font-size:16px; color:#333333; line-height:1.8; margin:0;">${esc(h.definition)}</p>
</div>
<!-- [/SEC:히어로] -->`;
}

function genNeeds(d) {
  const items = d.needs;
  const rows = [];
  for (let i = 0; i < items.length; i += 2) {
    const left = items[i];
    const right = items[i + 1];
    const isLast = i + 2 >= items.length;
    const borderStyle = isLast ? '' : ' border-bottom:1px solid #E8E8E8;';
    let row = `    <tr>
      <td style="width:50%; padding:12px 14px 12px 0; vertical-align:top;${borderStyle}">
        <div style="font-weight:700; color:${COLORS.primary}; font-size:15px; margin-bottom:4px;">${esc(left.title)}</div>
        <div style="font-size:14px; color:#666666; line-height:1.6;">${esc(left.desc)}</div>
      </td>`;
    if (right) {
      row += `
      <td style="width:50%; padding:12px 0 12px 14px; vertical-align:top;${borderStyle}">
        <div style="font-weight:700; color:${COLORS.primary}; font-size:15px; margin-bottom:4px;">${esc(right.title)}</div>
        <div style="font-size:14px; color:#666666; line-height:1.6;">${esc(right.desc)}</div>
      </td>`;
    }
    row += `\n    </tr>`;
    rows.push(row);
  }

  return `<!-- [SEC:필요상황] -->
<div style="background:${COLORS.bg2}; padding:48px 28px;">
  ${secTitle('이런 상황에서 필요합니다')}
  <table style="width:100%; border-collapse:collapse;">
${rows.join('\n')}
  </table>
</div>
<!-- [/SEC:필요상황] -->`;
}

function genSpecs(d) {
  const specs = d.specs;
  const rows = specs.map((s, i) => {
    const isLast = i === specs.length - 1;
    const headerBorder = isLast ? '' : ' border-bottom:1px solid #2C3E6B;';
    const cellBorder = isLast ? '' : ' border-bottom:1px solid #EEEEEE;';
    return `    <tr>
      <td style="background:${COLORS.primary}; color:#ffffff; font-weight:600; padding:12px 16px; width:30%;${headerBorder}">${esc(s.label)}</td>
      <td style="padding:12px 16px;${cellBorder} color:#333333;">${esc(s.value)}</td>
    </tr>`;
  });

  return `<!-- [SEC:스펙] -->
<div style="background:${COLORS.bg1}; padding:48px 28px;">
  ${secTitle('제품 사양')}
  <table style="width:100%; border-collapse:collapse; font-size:15px;">
${rows.join('\n')}
  </table>
</div>
<!-- [/SEC:스펙] -->`;
}

function genExperience(d) {
  const items = d.experience;
  const blocks = items.map((item, i) => {
    const mb = i < items.length - 1 ? 'margin-bottom:24px;' : 'margin-bottom:0;';
    return `  <div style="${mb}">
    <div style="font-size:17px; font-weight:700; color:${COLORS.primary}; margin-bottom:8px;">${esc(item.title)}</div>
    <p style="font-size:15px; color:#444444; line-height:1.8; margin:0;">${esc(item.desc)}</p>
  </div>`;
  });

  return `<!-- [SEC:체감설명] -->
<div style="background:${COLORS.bg2}; padding:48px 28px;">
  ${secTitle('실사용 포인트')}
${blocks.join('\n\n')}
</div>
<!-- [/SEC:체감설명] -->`;
}

function genPositions(d) {
  const items = d.positions;
  const width = (100 / items.length).toFixed(1) + '%';
  const cells = items.map((p, i) => {
    const borderRight = i < items.length - 1 ? ' border-right:1px solid #EEEEEE;' : '';
    return `      <td style="width:${width}; padding:16px 10px; vertical-align:top; text-align:center;${borderRight}">
        <div style="background:${COLORS.primary}; color:${COLORS.accent}; font-size:13px; font-weight:700; padding:6px 0; margin-bottom:12px;">${esc(p.label)}</div>
        <div style="font-size:14px; color:#444444; line-height:1.7; text-align:left;">${esc(p.desc)}</div>
      </td>`;
  });

  return `<!-- [SEC:포지션] -->
<div style="background:${COLORS.bg1}; padding:48px 28px;">
  ${secTitle('이런 분께 적합합니다')}
  <table style="width:100%; border-collapse:collapse;">
    <tr>
${cells.join('\n')}
    </tr>
  </table>
</div>
<!-- [/SEC:포지션] -->`;
}

function genSizeGuide(d) {
  const sg = d.sizeGuide;
  const headerRow = `    <tr>
      <td style="background:${COLORS.primary}; color:#ffffff; font-weight:600; padding:10px 14px; text-align:center; border:1px solid #2C3E6B;">포지션</td>
      <td style="background:${COLORS.primary}; color:#ffffff; font-weight:600; padding:10px 14px; text-align:center; border:1px solid #2C3E6B;">권장 사이즈</td>
      <td style="background:${COLORS.primary}; color:#ffffff; font-weight:600; padding:10px 14px; text-align:center; border:1px solid #2C3E6B;">비고</td>
    </tr>`;

  const dataRows = sg.rows.map(r => {
    if (r.highlight) {
      return `    <tr style="background:${COLORS.accent};">
      <td style="padding:10px 14px; text-align:center; border:1px solid #DDDDDD; font-weight:700; color:${COLORS.primary};">${esc(r.position)}</td>
      <td style="padding:10px 14px; text-align:center; border:1px solid #DDDDDD; font-weight:700; color:${COLORS.primary};">${esc(r.range)}</td>
      <td style="padding:10px 14px; text-align:center; border:1px solid #DDDDDD; font-weight:700; color:${COLORS.primary};">${esc(r.note)}</td>
    </tr>`;
    }
    return `    <tr>
      <td style="padding:10px 14px; text-align:center; border:1px solid #DDDDDD; color:#666666;">${esc(r.position)}</td>
      <td style="padding:10px 14px; text-align:center; border:1px solid #DDDDDD; color:#666666;">${esc(r.range)}</td>
      <td style="padding:10px 14px; text-align:center; border:1px solid #DDDDDD; color:#666666;">${esc(r.note)}</td>
    </tr>`;
  });

  return `<!-- [SEC:사이즈] -->
<div style="background:${COLORS.bg2}; padding:48px 28px;">
  ${secTitle('사이즈 가이드')}
  <table style="width:100%; border-collapse:collapse; font-size:14px; margin-bottom:20px;">
${headerRow}
${dataRows.join('\n')}
  </table>
  <div style="background:#ffffff; border:1px solid #E0E0E0; padding:16px 18px;">
    <div style="font-weight:700; color:${COLORS.primary}; font-size:15px; margin-bottom:6px;">착용 팁</div>
    <p style="font-size:14px; color:#555555; line-height:1.7; margin:0;">${esc(sg.tip)}</p>
  </div>
</div>
<!-- [/SEC:사이즈] -->`;
}

function genComparison(d) {
  const c = d.comparison;
  const hi = c.highlightIndex || 0;

  const headerCells = c.products.map((name, i) => {
    if (i === hi) {
      return `        <td style="background:${COLORS.accent}; color:${COLORS.primary}; font-weight:700; padding:10px 12px; text-align:center; border:1px solid #C09838;">${esc(name)}</td>`;
    }
    return `        <td style="background:${COLORS.primary}; color:#ffffff; font-weight:600; padding:10px 12px; text-align:center; border:1px solid #2C3E6B;">${esc(name)}</td>`;
  });

  const dataRows = c.rows.map(r => {
    const valueCells = r.values.map((v, i) => {
      const bgStyle = i === hi ? ` background:#FFF9EE;` : '';
      return `        <td style="padding:10px 12px; border:1px solid #EEEEEE; text-align:center; color:#333333;${bgStyle}">${esc(v)}</td>`;
    });
    return `      <tr>
        <td style="padding:10px 12px; border:1px solid #EEEEEE; font-weight:600; color:${COLORS.primary}; background:${COLORS.bg2};">${esc(r.label)}</td>
${valueCells.join('\n')}
      </tr>`;
  });

  return `<!-- [SEC:비교표] -->
<div style="background:${COLORS.bg1}; padding:48px 28px;">
  ${secTitle('동급 제품 비교')}
  <div style="overflow-x:auto;">
    <table style="width:100%; border-collapse:collapse; font-size:14px; min-width:600px;">
      <tr>
        <td style="background:${COLORS.primary}; color:#ffffff; font-weight:600; padding:10px 12px; text-align:center; border:1px solid #2C3E6B;">항목</td>
${headerCells.join('\n')}
      </tr>
${dataRows.join('\n')}
    </table>
  </div>
</div>
<!-- [/SEC:비교표] -->`;
}

function genFaq(d) {
  const faqs = d.faq;
  const items = faqs.map((f, i) => {
    const mb = i < faqs.length - 1 ? 'margin-bottom:8px; ' : 'margin-bottom:0; ';
    return `    <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question" style="${mb}border:1px solid #DDDDDD;">
      <div itemprop="name" style="padding:14px 16px; background:${COLORS.bg2}; font-weight:700; color:${COLORS.primary}; font-size:14px;">
        <span style="color:${COLORS.accent}; font-weight:700; margin-right:4px;">Q.</span>${esc(f.q)}
      </div>
      <div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
        <p itemprop="text" style="padding:14px 16px; font-size:14px; color:#444444; line-height:1.8; background:#ffffff; margin:0;">${esc(f.a)}</p>
      </div>
    </div>`;
  });

  return `<!-- [SEC:FAQ] -->
<div style="background:${COLORS.bg2}; padding:48px 28px;">
  ${secTitle('자주 묻는 질문')}
  <div itemscope itemtype="https://schema.org/FAQPage">
${items.join('\n\n')}
  </div>
</div>
<!-- [/SEC:FAQ] -->`;
}

function genExpert(d) {
  const e = d.expert;
  return `<!-- [SEC:전문가] -->
<div style="background:${COLORS.dark}; padding:48px 28px;">
  ${secTitleWhite('짱베이스볼 상담팀의 한마디')}
  <div style="background:rgba(255,255,255,0.08); padding:24px 20px; border-left:3px solid ${COLORS.accent};">
    <p style="font-size:15px; color:rgba(255,255,255,0.9); line-height:1.9; margin:0;">"${esc(e.quote)}"</p>
    <div style="margin-top:14px; color:${COLORS.accent}; font-size:13px; font-weight:600;">— ${esc(e.author)}</div>
  </div>
</div>
<!-- [/SEC:전문가] -->`;
}

function genSummary(d) {
  const items = d.summary;
  const rows = items.map((s, i) => {
    const borderBottom = i < items.length - 1 ? ' border-bottom:1px solid #EEEEEE;' : '';
    return `    <tr>
      <td style="padding:14px 16px;${borderBottom} vertical-align:top;">
        <div style="font-weight:700; color:${COLORS.primary}; font-size:15px; margin-bottom:4px;">${esc(s.title)}</div>
        <div style="font-size:14px; color:#666666; line-height:1.6;">${esc(s.desc)}</div>
      </td>
    </tr>`;
  });

  return `<!-- [SEC:서머리] -->
<div style="background:${COLORS.bg1}; padding:48px 28px;">
  ${secTitle('추천 포인트')}
  <table style="width:100%; border-collapse:collapse;">
${rows.join('\n')}
  </table>
  <div style="text-align:center; margin-top:32px;">
    <a href="https://8k27y.channel.io" style="display:inline-block; background:${COLORS.accent}; color:${COLORS.primary}; font-size:15px; font-weight:600; padding:12px 32px; text-decoration:none;" target="_blank">채널톡 문의하기</a>
  </div>
</div>
<!-- [/SEC:서머리] -->`;
}

// ─── 조립 ───
const sections = [];
let sectionCount = 0;

// 폰트 링크
sections.push('<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">');

// JSON-LD Product
sections.push(`<script type="application/ld+json">\n${genProductSchema(data.product)}\n</script>`);

// JSON-LD FAQ (FAQ 포함 시에만)
if (isIncluded('faq') && data.faq && data.faq.length > 0) {
  sections.push(`<script type="application/ld+json">\n${genFaqSchema(data.faq)}\n</script>`);
}

// 래퍼 시작
sections.push(`<div style="max-width:860px; margin:0 auto; font-family:'Noto Sans KR',-apple-system,BlinkMacSystemFont,sans-serif; color:#222222; line-height:1.7; font-size:17px;">`);

// 히어로 (필수)
if (data.hero) { sections.push(genHero(data)); sectionCount++; }

// 필요상황
if (isIncluded('필요상황') && data.needs) { sections.push(genNeeds(data)); sectionCount++; }

// 스펙 (필수)
if (data.specs) { sections.push(genSpecs(data)); sectionCount++; }

// 체감설명
if (isIncluded('체감설명') && data.experience) { sections.push(genExperience(data)); sectionCount++; }

// 포지션
if (isIncluded('포지션') && data.positions) { sections.push(genPositions(data)); sectionCount++; }

// 사이즈
if (isIncluded('사이즈') && data.sizeGuide) { sections.push(genSizeGuide(data)); sectionCount++; }

// 비교표
if (isIncluded('비교표') && data.comparison) { sections.push(genComparison(data)); sectionCount++; }

// FAQ
if (isIncluded('faq') && data.faq) { sections.push(genFaq(data)); sectionCount++; }

// 전문가
if (isIncluded('전문가') && data.expert) { sections.push(genExpert(data)); sectionCount++; }

// 서머리
if (isIncluded('서머리') && data.summary) { sections.push(genSummary(data)); sectionCount++; }

// 래퍼 종료
sections.push('</div>');

// ─── 파일 저장 ───
const html = sections.join('\n\n');
const outputPath = path.join(OUTPUT_DIR, data.fileName);

// 출력 디렉토리 확인
if (!fs.existsSync(OUTPUT_DIR)) { fs.mkdirSync(OUTPUT_DIR, { recursive: true }); }

fs.writeFileSync(outputPath, html, 'utf8');

// ─── 요약 출력 ───
const lines = html.split('\n').length;
const sizeKB = (Buffer.byteLength(html, 'utf8') / 1024).toFixed(1);
const excludeInfo = exclude.length > 0 ? ` | 제외: ${exclude.join(', ')}` : '';

console.log(`[상세페이지 생성 완료]`);
console.log(`파일: ${outputPath}`);
console.log(`섹션: ${sectionCount}개 | ${lines}줄 | ${sizeKB}KB${excludeInfo}`);
console.log(`스키마: Product JSON-LD${isIncluded('faq') && data.faq ? ' + FAQPage JSON-LD + 마이크로데이터' : ''}`);
