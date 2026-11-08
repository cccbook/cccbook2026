# 07.2-單樣本t檢定
# 由 07.2-單樣本t檢定.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

x = [499.8, 493.1, 498.2, 497.2, 494.8, 487.0, 494.5, 493.3, 498.1,
     495.6, 495.9, 494.5, 496.7, 496.7, 486.9, 503.3]

t = r.t_test(x, mu=500)
print(t)


# --- 區塊 2 ---
t1 = r.t_test(x, mu=500, alternative='less')
print(t1)


# --- 區塊 3 ---
import rstatistics as r

g = r.set_seed(2026)
x = [round(v, 1) for v in g.rnorm(16, mean=497.6, sd=4.2)]
print([round(r.mean(x), 2), round(r.sd(x), 2)])
