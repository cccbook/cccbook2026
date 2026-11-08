# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

print("=== ppoints ===")
print("ppoints(10) =", [round(v, 4) for v in r.ppoints(10)])
print("ppoints(5)  =", [round(v, 4) for v in r.ppoints(5)])
print("ppoints(60) 的前後三個 =", [round(v, 4) for v in r.ppoints(60)[:3]], [round(v, 4) for v in r.ppoints(60)[-3:]])
