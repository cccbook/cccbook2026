# 08.6-多重比較與p_adjust
# 由 08.6-多重比較與p_adjust.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

m = 20
p_none = (1 - 0.05) ** m
print(f"做了 {m} 個獨立檢定，每個在 5% 水準下：")
print(f"  全部都不顯著的機率 = 0.95^{m} = {p_none:.6f}")
print(f"  至少一個偽陽性（第一型錯誤）的機率 = 1 - 0.95^{m} = {1-p_none:.6f}")
print()
for k in [1, 5, 10, 20, 50, 100]:
    print(f"  k = {k:4d} 個檢定 → 至少一個偽陽性的機率 = {1 - 0.95**k:.4f}")


# --- 區塊 2 ---
import rstatistics as r

srt = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]
n = len(srt)
alpha = 0.05

print("=== Bonferroni 手算：p_adj = min(1, m * p) ===")
for i, p in enumerate(srt, start=1):
    print(f"  第 {i} 小的 p = {p:.3f}  × {n} = {min(1.0, p*n):.6f}")


# --- 區塊 3 ---
import rstatistics as r

srt = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]
n = len(srt)
alpha = 0.05

print("=== Holm 手算：p_adj = max_{j<=i} (m-j+1) * p_(j) ===")
acc = 0.0
for i, p in enumerate(srt, start=1):
    v = (n - i + 1) * p
    acc = max(acc, v)
    adj = min(1.0, acc)
    print(f"  第 {i} 小的 p = {p:.3f}   (m-i+1)*p = {(n-i+1)*p:.6f}   累積最大 = {adj:.6f}   "
          f"{'拒絕' if adj < alpha else '不拒絕'}")


# --- 區塊 4 ---
import rstatistics as r

ps = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]
alpha = 0.05
m = len(ps)
srt = sorted(ps)
print("BH 的門檻：把 p 值排序後，第 i 小的門檻是 i/m * alpha")
for i, p in enumerate(srt, start=1):
    thr = i / m * alpha
    print(f"  第 {i} 小的 p = {p:.3f}，門檻 = {i}/{m} * {alpha} = {thr:.4f}   {'拒絕' if p <= thr else '不拒絕'}")


# --- 區塊 5 ---
import rstatistics as r

ps = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]
print("原始 p 值（已由小到大排序）：", ps)
print()
methods = ["bonferroni", "holm", "hochberg", "hommel", "BH", "BY", "none"]
for m_ in methods:
    adj = r.p_adjust(ps, method=m_)
    print(f"{m_:11s}", " ".join(f"{v:.6f}" for v in adj))
print()

print("各方法在 alpha = 0.05 下拒絕幾個：")
for m_ in methods:
    adj = r.p_adjust(ps, method=m_)
    print(f"  {m_:11s} {sum(1 for v in adj if v < 0.05)} 個")


# --- 區塊 6 ---
import rstatistics as r

N = 2000
alpha = 0.05
m = 20

g = r.set_seed(123)
methods = ["none", "bonferroni", "holm", "hochberg", "hommel", "BH", "BY"]
counts = {mm: 0 for mm in methods}
for _ in range(N):
    ps = [g.runif(1)[0] for _ in range(m)]
    for mm in methods:
        adj = r.p_adjust(ps, method=mm)
        if any(v < alpha for v in adj):
            counts[mm] += 1
print(f"全部為零假設、m = {m} 個獨立檢定、重複 {N} 次：")
for mm in methods:
    print(f"  {mm:11s} 至少一次偽陽性的機率 = {counts[mm]/N:.3f}")


# --- 區塊 7 ---
import rstatistics as r

N = 2000
alpha = 0.05
m = 20

g = r.set_seed(123)
true_rej = {mm: 0 for mm in methods}
false_rej = {mm: 0 for mm in methods}
for _ in range(N):
    ps = [g.runif(1)[0] * 0.01 for _ in range(3)] + [g.runif(1)[0] for _ in range(m - 3)]
    for mm in methods:
        adj = r.p_adjust(ps, method=mm)
        t = sum(1 for v in adj[:3] if v < alpha)
        f = sum(1 for v in adj[3:] if v < alpha)
        true_rej[mm] += t
        false_rej[mm] += f
print(f"前 3 個真陽性、後 {m-3} 個零假設（總共 {N} 次）：")
print("  方法          真陽性平均數   偽陽性平均數")
for mm in methods:
    print(f"  {mm:11s}   {true_rej[mm]/N:8.2f}      {false_rej[mm]/N:8.2f}")
