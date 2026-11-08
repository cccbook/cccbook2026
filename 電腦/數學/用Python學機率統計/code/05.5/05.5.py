# 05.5-可重現的亂數
# 由 05.5-可重現的亂數.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

# ---- (1) 同 seed 必得同序列（確定性）----
print("同 seed 兩次呼叫：")
print("  第一次:", r.set_seed(2026).rnorm(5))
print("  第二次:", r.set_seed(2026).rnorm(5))
print("  不同 seed:", r.set_seed(2027).rnorm(5))

# ---- (2) 拼接性：前 3 個 + 後 2 個 == 一次抽 5 個 ----
print()
a = r.set_seed(2026)
b = r.set_seed(2026)
print("一次抽 5 個        :", a.rnorm(5))
print("先抽 3 個再抽 2 個 :", b.rnorm(3), "+", b.rnorm(2))

# ---- (3) 位元等價：與 R 的 set.seed(42) 比對 ----
print()
print("r.set_seed(42) 的前兩個均勻亂數:", r.RNG(42).runif(2))
print("r.set_seed(42) 的前三個標準常態:", r.RNG(42).rnorm(3))


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(42)
x = g.rnorm(30, mean=0.0, sd=1.0)
y = g.rnorm(25, mean=0.5, sd=1.0)
print(r.t_test(x, y))
