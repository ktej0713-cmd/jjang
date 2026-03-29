# -*- coding: utf-8 -*-
import json, os

def get_naver_cat(c, nm):
    if c.startswith("001") or c.startswith("021"): return "50001556"
    if c.startswith("002"): return "50001558"
    if c.startswith("003"): return "50001557"
    if c.startswith("005"): return "50001433"
    if c.startswith("006"): return "50001560"
    if "글러브" in nm or "미트" in nm: return "50001556"
    if "배트" in nm: return "50001557"
    if "야구화" in nm or "포인트화" in nm: return "50001558"
    if "헬멧" in nm or "가드" in nm or "마스크" in nm: return "50001433"
    if "배팅장갑" in nm or "슬라이딩" in nm: return "50001560"
    return "50001437"

def clamp(s, n, sep):
    if len(s) <= n: return s
    r = ""
    for p in s.split(sep):
        c = (r + sep + p) if r else p
        if len(c) <= n: r = c
        else: break
    return r

seo_json_file = "C:/Users/jj1/.claude/output/seo/batch18_seo_data.json"
with open(seo_json_file, "r", encoding="utf-8") as f:
    seo = json.load(f)

with open("C:/Users/jj1/.claude/output/seo/batch_18.json", "r", encoding="utf-8") as f:
    items = json.load(f)

ok = []
for item in items:
    gno = item["goodsNo"]
    nm = item["goodsNm"]
    model = item["modelNo"]
    maker_raw = item["maker"]
    cateCd = item.get("cateCd", "")
    if "개인결제" in nm:
        print(f"SKIP: {gno}")
        continue
    d = seo.get(gno)
    if not d:
        print(f"NODATA: {gno}")
        continue
    maker = maker_raw[:30]
    ncat = get_naver_cat(cateCd, nm)
    kw = clamp(d[0], 250, ",")
    title15 = d[1][:15] + " | 짱베이스볼"
    desc = d[2][:80]
    keys = ",".join(d[3].split(",")[:10])
    ntag = clamp(d[4], 100, "|")
    attr = d[5]
    out = {"_상품번호": gno, "_상품명": nm, "검색키워드": kw, "SEO태그": {"meta_title": title15, "meta_description": desc, "meta_keywords": keys, "meta_author": "짱베이스볼"}, "네이버EP": {"카테고리코드": ncat, "제조사": maker, "모델명": model, "검색태그": ntag, "속성": attr}}
    path = f"C:/Users/jj1/.claude/output/seo/seo_data_{gno}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    ok.append(gno)
    print(f"OK {gno}")

print(f"완료 {len(ok)}개")