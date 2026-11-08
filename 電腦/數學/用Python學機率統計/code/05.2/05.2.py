# 05.2-中央極限定理
# 由 05.2-中央極限定理.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

def ascii_hist(x, nb=20, width=60):
    lo, hi = min(x), max(x)
    step = (hi - lo) / nb
    counts = [0] * nb
    for v in x:
        counts[min(nb - 1, int((v - lo) / step))] += 1
    mx = max(counts)
    for i, c in enumerate(counts):
        if c == 0: continue
        m = lo + (i + 0.5) * step
        bar = "#" * max(1, round(width * c / mx))
        print(f"{m:8.2f} |{bar} {c}")

B = 20000

print("=== (1) 均勻母體 U(0,10)，n=30 ===")
g = r.set_seed(7)
xb = []
for _ in range(B):
    xb.append(r.mean(g.runif(30, 0.0, 10.0)))
print(f"平均 = {r.mean(xb):.4f} (母體平均 5)，sd = {r.sd(xb):.4f} (理論 {(10/12**0.5)/30**0.5:.4f})")
ascii_hist(xb, nb=20)

print()
print("=== (2) 指數母體 Exp(rate=1)，n=30 ===")
g = r.set_seed(7)
xe = []
for _ in range(B):
    xe.append(r.mean(g.rexp(30, 1.0)))
print(f"平均 = {r.mean(xe):.4f} (母體平均 1)，sd = {r.sd(xe):.4f} (理論 {1/30**0.5:.4f})")
ascii_hist(xe, nb=20)

print()
print("=== (3) 二項母體 Bin(10, 0.3)，n=30 ===")
g = r.set_seed(7)
xo = []
for _ in range(B):
    xo.append(r.mean([float(v) for v in g.rbinom(30, 10, 0.3)]))
print(f"平均 = {r.mean(xo):.4f} (母體平均 3)，sd = {r.sd(xo):.4f} (理論 {(10*0.3*0.7)**0.5/30**0.5:.4f})")
ascii_hist(xo, nb=20)


# --- 區塊 2 ---
print("=== n 要多大？指數母體，n = 5 / 30 / 100 ===")
for n in (5, 30, 100):
    g = r.set_seed(7)
    xs = []
    for _ in range(B):
        xs.append(r.mean(g.rexp(n, 1.0)))
    skew_note = {5: "仍看到右偏尾巴", 30: "已接近鐘形", 100: "幾乎完美鐘形"}[n]
    print(f"n={n:3d}: sd={r.sd(xs):.4f} (理論 {1/n**0.5:.4f})  {skew_note}")
    if n == 5:
        ascii_hist(xs, nb=18)

print()
print("=== n=100 指數母體的 xbar 直方圖（對照鐘形）===")
g = r.set_seed(7)
xs = []
for _ in range(B):
    xs.append(r.mean(g.rexp(100, 1.0)))
ascii_hist(xs, nb=18)


# --- 區塊 3 ---
import rstatistics as r

B = 8000
NS = [5, 30, 100]


def sample_means(vals, n):
    """把 B*n 個抽樣值切成 B 組、每組 n 個，取各組平均。"""
    out = []
    for i in range(B):
        out.append(r.mean(vals[i * n:(i + 1) * n]))
    return out


def normal_overlay(g, xlo, xhi, mu, sigma, n, col="red"):
    """在目前的圖窗上疊上 N(mu, sigma^2/n) 的密度曲線。"""
    xs = []
    ys = []
    for i in range(201):
        x = xlo + (xhi - xlo) * float(i) / 200.0
        xs.append(x)
        ys.append(r.dnorm(x, mu, sigma / n ** 0.5))
    g.lines(xs, ys, col, 2.0)


def one_figure(name, title, label, mu, sigma, breaks, draw):
    g = r.Graphics(width=7.0, height=7.0, mfrow=[2, 2])
    g.hist(draw(20000), main="母體：" + title, xlab=label, ylab="Density",
           freq=False, breaks=breaks)
    for k in range(3):
        n = NS[k]
        g.next_panel()
        xs = sample_means(draw(B * n), n)
        h = g.hist(xs, main="xbar 的抽樣分布，n = " + str(n), xlab="xbar",
                   ylab="Density", freq=False, breaks="FD")
        normal_overlay(g, h.breaks[0], h.breaks[len(h.breaks) - 1], mu, sigma, n)
    g.save("05.2-clt-" + name + ".svg")
    print("寫出 05.2-clt-" + name + ".svg")


g1 = r.set_seed(11)
one_figure("coin", "銅板（0 或 1，p=0.5）", "0 或 1", 0.5, 0.5, "FD",
           lambda k: [float(v) for v in g1.rbinom(k, 1, 0.5)])

g2 = r.set_seed(12)
one_figure("dice", "骰子（1~6）", "點數", 3.5, (35.0 / 12.0) ** 0.5, "FD",
           lambda k: g2.sample_from([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], k, True))

g3 = r.set_seed(13)
one_figure("uniform", "均勻 U(0,10)", "x", 5.0, (100.0 / 12.0) ** 0.5, "FD",
           lambda k: g3.runif(k, 0.0, 10.0))

g4 = r.set_seed(14)
one_figure("exponential", "指數 Exp(rate=1)", "x", 1.0, 1.0, "FD",
           lambda k: g4.rexp(k, 1.0))

g5 = r.set_seed(15)
one_figure("normal", "常態 N(0,1)", "x", 0.0, 1.0, "FD",
           lambda k: g5.rnorm(k, 0.0, 1.0))
