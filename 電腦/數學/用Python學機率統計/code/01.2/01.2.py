# 01.2-集中趨勢
# 由 01.2-集中趨勢.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

w = [28, 30, 32, 32, 35, 36, 38, 40, 42, 45, 48, 52, 55, 60, 220]
print(r.mean(w), r.median(w))


# --- 區塊 2 ---
print(r.mean(w))


# --- 區塊 3 ---
print(r.median(w))
print(r.median([1, 2, 3, 100]))   # 偶數個：取 2 與 3 的平均


# --- 區塊 4 ---
scores = [60, 80, 90]
weights = [0.2, 0.3, 0.5]
print(r.weighted_mean(scores, weights))


# --- 區塊 5 ---
import rstatistics as r

w = [28, 30, 32, 32, 35, 36, 38, 40, 42, 45, 48, 52, 55, 60, 220]

# 候選值：以 0.5 為步距掃過資料範圍
cands = [x + 0.5 * k for x in range(20, 61) for k in range(4)]

best_sq  = min(cands, key=lambda c: sum((xi - c) ** 2 for xi in w))
best_abs = min(cands, key=lambda c: sum(abs(xi - c) for xi in w))

print(best_sq, best_abs)
print(r.mean(w), r.median(w))


# --- 區塊 6 ---
g = r.Graphics(width=7.0, height=4.5)
cs = [x * 1.0 for x in range(25, 75)]
g.plot(cs, [sum((xi - c) ** 2 for xi in w) / 10000 for c in cs])
g.lines(cs, [sum(abs(xi - c) for xi in w) / 100 for c in cs])
g.title("兩種誤差總和的形狀（縮放後）", )
g.save("img/err_curves.svg")


# --- 區塊 7 ---
import rstatistics as r

w = [28, 30, 32, 32, 35, 36, 38, 40, 42, 45, 48, 52, 55, 60, 220]

print("mean   =", r.mean(w))
print("median =", r.median(w))
print("wmean  =", r.weighted_mean(w, [1] * 15))    # 等權重 → 退化成普通平均
