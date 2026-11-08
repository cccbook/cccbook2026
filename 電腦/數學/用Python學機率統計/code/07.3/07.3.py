# 07.3-兩樣本t檢定與Welch檢定
# 由 07.3-兩樣本t檢定與Welch檢定.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r
A = [12.1,12.4,11.9,12.3,12.0,12.2,11.8,12.5,12.1,12.0,11.9,12.3]
B = [9.8,11.6,12.9,10.4,11.2,13.1,9.5,12.4,10.8,11.7]

print(r.var_test(A, B))


# --- 區塊 2 ---
print(r.t_test(A, B, var_equal=True))


# --- 區塊 3 ---
print(r.t_test(A, B))


# --- 區塊 4 ---
print(r.t_test(A, B, alternative='greater'))


# --- 區塊 5 ---
before = [148,132,141,155,129,138,150,144,136,147,133,142]
after  = [132,124,128,140,120,130,138,135,126,136,125,130]

d = [before[i] - after[i] for i in range(12)]
print("平均下降", r.mean(d), " 差值的標準差", r.sd(d))
print("組內 sd（before）", r.sd(before), " 組內 sd（after）", r.sd(after))


# --- 區塊 6 ---
print(r.t_test(before, after, paired=True))


# --- 區塊 7 ---
print(r.t_test(before, after))          # 忘了 paired=True


# --- 區塊 8 ---
def sim(n1, n2, sd1, sd2, N=5000, seed=11):
    g = r.set_seed(seed)
    rp = rw = 0
    for i in range(N):
        x = g.rnorm(n1, 0.0, sd1)
        y = g.rnorm(n2, 0.0, sd2)
        if r.t_test(x, y, var_equal=True).p_value < 0.05:
            rp += 1
        if r.t_test(x, y).p_value < 0.05:
            rw += 1
    return rp / N, rw / N

for (n1, n2, sd1, sd2) in [(30,10,1,3), (15,15,1,4), (10,30,1,3)]:
    p_pool, p_welch = sim(n1, n2, sd1, sd2)
    print(f"n1={n1}, n2={n2}, sd1={sd1}, sd2={sd2}")
    print(f"  pooled 拒絕率 = {p_pool:.4f}")
    print(f"  Welch  拒絕率 = {p_welch:.4f}")
