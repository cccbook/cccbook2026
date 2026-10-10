# 1949 - Hebb 學習規則
# 對應本書: 1949-Hebb學習規則.md
# 公式: Δw_i = η x_i y ; 矩陣版 W = Σ_k a_k a_k^T (外積和)
# 展示: 只給一半線索, 聯想喚起完整模式 (內容定址記憶)
import numpy as np


def hebb_store(patterns):
    """patterns: list of {+1,-1} 向量, 回傳 Hebb 權重矩陣 (對角線歸零)."""
    n = len(patterns[0])
    W = sum(np.outer(p, p) for p in patterns)
    np.fill_diagonal(W, 0)
    return W / n


def recall(W, cue, steps=5):
    s = cue.astype(float).copy()
    for _ in range(steps):
        s = np.sign(W @ s)
        s[s == 0] = 1
    return s.astype(int)


def main():
    a = np.array([1, 1, -1, -1, 1, -1])    # 模式 A (書中範例)
    b = np.array([-1, 1, 1, -1, -1, 1])    # 模式 B
    W = hebb_store([a, b])
    cue = np.array([1, 1, -1, -1, 0, 0])   # 只給前 4 位
    cue = np.where(cue == 0, 0, cue)
    # 缺位補 0 當作未知, 喚起時以 sign 決定
    s = recall(W, np.where(cue == 0, 0.0, cue.astype(float)))
    print("模式 A:", a)
    print("模式 B:", b)
    print("線索 :", cue, "(0=未知)")
    print("喚起 :", s)
    print("喚起==模式A:", bool(np.array_equal(s, a)),
          "(只給一半線索即補全 = 聯想的矩陣實作)")
    # 展示 Δw = η x y 的單突觸版
    w, eta = 0.2, 0.5
    x, y = 1, 1
    print(f"單突觸 Hebb 更新: w {w} + {eta}*{x}*{y} -> {w + eta * x * y}")


if __name__ == "__main__":
    main()
