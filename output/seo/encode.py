import base64, sys
ps = open("C:/Users/jj1/.claude/output/seo/gen06_raw.ps1", encoding="utf-8").read()
enc = base64.b64encode(ps.encode("utf-16-le")).decode("ascii")
print(enc)
