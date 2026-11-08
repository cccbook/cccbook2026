# 09.4-變異數分析
# 由 09.4-變異數分析.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import math
import rstatistics as r

D05 = [4.20, 11.50, 7.30, 5.80, 6.40, 10.00, 11.20, 11.20, 5.20, 7.00,
       15.20, 21.50, 17.60, 9.70, 14.50, 10.00, 8.20, 9.40, 16.50, 9.70]
D10 = [16.50, 16.50, 15.20, 17.30, 22.50, 17.30, 13.60, 14.50, 18.80, 15.50,
       19.70, 23.30, 23.60, 26.40, 20.00, 25.20, 25.80, 21.20, 14.50, 27.30]
D20 = [23.60, 18.50, 33.90, 25.50, 26.40, 32.50, 26.70, 21.50, 23.30, 29.50,
       25.50, 26.40, 22.40, 24.50, 24.80, 30.90, 26.40, 27.30, 29.40, 23.00]

y = D05 + D10 + D20
group = ["0.5"] * 20 + ["1.0"] * 20 + ["2.0"] * 20

# ---------- 手算單因子 ANOVA ----------
groups = {"0.5": D05, "1.0": D10, "2.0": D20}
grand = r.mean(y)
n = len(y)
k = 3
ssb = 0.0
ssw = 0.0
print("組別    n   平均數")
for name in ["0.5", "1.0", "2.0"]:
    xs = groups[name]
    mj = r.mean(xs)
    ssb += len(xs) * (mj - grand) ** 2
    ssw += sum((v - mj) ** 2 for v in xs)
    print("%-5s %3d   %7.3f" % (name, len(xs), mj))
print("總平均 = %.4f" % grand)
dfb = k - 1
dfw = n - k
msb = ssb / dfb
msw = ssw / dfw
F = msb / msw
p = r.pf(F, dfb, dfw, lower_tail=False)
print()
print("SS_between = %.4f (df = %d), MS_between = %.4f" % (ssb, dfb, msb))
print("SS_within  = %.4f (df = %d), MS_within  = %.4f" % (ssw, dfw, msw))
print("F = %.4f, p = %.6g" % (F, p))

# ---------- r.aov ----------
a = r.aov(y, group, formula="len ~ dose")
print()
print(a)
print()
print(a.summary())

# ---------- 與 Kruskal-Wallis 對照 ----------
print()
print(r.kruskal_test(y, group))

# ---------- 圖：三組的箱型圖 ----------
gr = r.Graphics(width=8.0, height=3.6, mfrow=[1, 3])
for name in ["0.5", "1.0", "2.0"]:
    gr.boxplot(groups[name], main="劑量 %s" % name, xlab="牙齒生長長度", ylab="len")
    if name != "2.0":
        gr.next_panel()
gr.save("img/09.4-groups.svg")
print()
print("已存 09.4-groups.svg")


# --- 區塊 2 ---
import rstatistics as r

g2 = r.set_seed(2024)
y2 = []
grp2 = []
for name in ["A", "B", "C"]:
    for _ in range(20):
        y2.append(g2.rnorm(1)[0] + 10.0)
        grp2.append(name)
y2[40] = 70.0        # C 組的一個離群值
print()
print("離群值的影響：")
print("  各組平均數: %.3f %.3f %.3f" % (r.mean(y2[0:20]), r.mean(y2[20:40]), r.mean(y2[40:60])))
print("  各組中位數: %.3f %.3f %.3f" % (r.median(y2[0:20]), r.median(y2[20:40]), r.median(y2[40:60])))
a2 = r.aov(y2, grp2, formula="y ~ g")
print()
print(a2.summary())
print()
print(r.kruskal_test(y2, grp2))
