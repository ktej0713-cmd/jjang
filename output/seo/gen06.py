import json, os, re

output_dir = r"C:\Users\jj1\.claude\output\seo"

def get_naver_cat(cateCd, goodsNm):
    if cateCd.startswith("005"):
        return "50001433"
    elif cateCd.startswith("039"):
        return "50005248"
    elif cateCd.startswith("006"):
        return "50001560"
    elif cateCd.startswith("021"):
        return "50001556"
    elif cateCd == "":
        if any(x in goodsNm for x in ["\xc554\xac00\xb4dc", "\xd48b\xac00\xb4dc", "\ud578\ub4dc\uac00\ub4dc", "\xc190\xb4f1\uac00\ub4dc"]):
            return "50001433"
    return "50001437"