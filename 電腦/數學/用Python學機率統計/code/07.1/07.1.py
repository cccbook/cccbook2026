# 07.1-檢定的邏輯
# 由 07.1-檢定的邏輯.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(42)
N = 10000
ps = []
for i in range(N):
    x = g.rnorm(20)              # H0 為真：mu = 0
    t = r.t_test(x, mu=0.0)
    ps.append(t.p_value)

cnt = sum(1 for p in ps if p < 0.05)
print("H0 為真時 p<0.05 的比例：", cnt/N)

b = [0]*10                          # 十個等寬桶
for p in ps:
    b[min(int(p*10), 9)] += 1
print("各桶計數（每桶理論值 1000）:")
for i, c in enumerate(b):
    print(f"  [{i/10:.1f},{(i+1)/10:.1f}): {c}")


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(1)
N = 10000
ps = []
for i in range(N):
    x = g.rnorm(20, mean=0.5)    # 真實 mu = 0.5，效應存在
    t = r.t_test(x, mu=0.0)
    ps.append(t.p_value)

cnt = sum(1 for p in ps if p < 0.05)
print("H1 為真（delta=0.5）時 p<0.05 的比例：", cnt/N)

b = [0]*10
for p in ps:
    b[min(int(p*10), 9)] += 1
print("各桶計數:")
for i, c in enumerate(b):
    print(f"  [{i/10:.1f},{(i+1)/10:.1f}): {c}")


# --- 區塊 3 ---
import rstatistics as r
print("效應存在時 p<0.1 的比例：", 0.5575 + 0.1212)
print("無效應時   p<0.1 的比例：", 0.0992)
