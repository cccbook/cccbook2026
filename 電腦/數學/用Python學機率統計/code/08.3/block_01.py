# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2024)
x = [round(v, 4) for v in g.rnorm(50, 10.0, 2.0)]
y = [round(v, 4) for v in g.rnorm(50, 10.5, 2.0)]
print("x（前 10 筆）:", x[:10])
print("y（前 10 筆）:", y[:10])
print()

def F(v, data):
    return sum(1 for u in data if u <= v) / len(data)

pts = sorted(set(x) | set(y))
print("斷點處的 ECDF 差 |F_x - F_y|（只看前後各 10 個斷點）：")
best = 0.0
bpat = 0.0
for i, p in enumerate(pts):
    d = abs(F(p, x) - F(p, y))
    if d > best:
        best = d
        bpat = p
    if i < 10 or i >= len(pts) - 10:
        print(f"  t = {p:8.4f}   F_x = {F(p,x):.4f}   F_y = {F(p,y):.4f}   |diff| = {d:.4f}")
print("最大距離 D =", round(best, 6), " 出現在 t =", round(bpat, 4))
