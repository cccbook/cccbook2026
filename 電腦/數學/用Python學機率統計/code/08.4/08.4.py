# 08.4-Fisher精確檢定與列聯表
# 由 08.4-Fisher精確檢定與列聯表.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

m, n, k = 4, 4, 4
xx = 3
p = r.dhyper(xx, m, n, k)
print("P(X = 3) =", p, " （超幾何 C(4,3)C(4,1)/C(8,4) =", r.choose(4,3)*r.choose(4,1)/r.choose(8,4), "）")
print("全部可能格子的機率：")
tot = 0.0
for v in range(0, 5):
    pv = r.dhyper(v, m, n, k)
    tot += pv
    print(f"  X = {v}: P = {pv:.6f}")
print("  總和 =", round(tot, 6))


# --- 區塊 2 ---
import rstatistics as r

# 女士品茶：列 = 是否先倒奶，欄 = 是否猜對
tab = [[3, 1], [1, 3]]
print("列聯表（列=是否先倒茶，欄=是否猜對）：")
for row in tab:
    print("  ", row)
print()

h = r.fisher_test(tab)
print(h)
print("  h.method         =", h.method)
print("  h.p_value        =", h.p_value)
print("  h.estimate       =", h.estimate)
print("  h.conf_int       =", h.conf_int)
print("  h.alternative    =", h.alternative)
print("  h.null_name      =", h.null_name)


# --- 區塊 3 ---
import rstatistics as r

tab = [[3, 1], [1, 3]]
print("alternative='less'   :", r.fisher_test(tab, alternative="less").p_value)
print("alternative='greater':", r.fisher_test(tab, alternative="greater").p_value)


# --- 區塊 4 ---
import rstatistics as r

def expected(table):
    rows = [sum(r) for r in table]
    cols = [sum(table[i][j] for i in range(len(table))) for j in range(len(table[0]))]
    total = sum(rows)
    return [[rows[i] * cols[j] / total for j in range(len(cols))] for i in range(len(rows))]

for name, tb in [("[[36,16],[24,24]]", [[36,16],[24,24]]),
                 ("[[15,5],[5,15]]", [[15,5],[5,15]]),
                 ("[[3,2],[1,0]]", [[3,2],[1,0]])]:
    e = expected(tb)
    mn = min(min(r) for r in e)
    print(f"{name} 的期望次數 = {[[round(v,3) for v in row] for row in e]}   最小 = {mn:.3f}")


# --- 區塊 5 ---
import rstatistics as r

big = [[15, 5], [5, 15]]
print("較大的表 [[15,5],[5,15]]：")
print(r.fisher_test(big))
print()
print(r.chisq_test_table(big))
print()
print(r.chisq_test_table(big, correct=False))
print()

small = [[3, 2], [1, 0]]
print("小期望次數的表 [[3,2],[1,0]]：")
print(r.fisher_test(small))
print()
print(r.chisq_test_table(small))
print()
print(r.chisq_test_table(small, correct=False))


# --- 區塊 6 ---
import rstatistics as r

smoke = ["抽菸"] * 52 + ["不抽菸"] * 48
sick = ["患病"] * 36 + ["未患病"] * 16 + ["患病"] * 24 + ["未患病"] * 24
print("抽菸與疾病的列聯表：")
print(r.table(smoke, sick, "抽菸", "狀態"))
print()

tab2 = [[36, 16], [24, 24]]
print(r.fisher_test(tab2))
print()
print(r.chisq_test_table(tab2))
