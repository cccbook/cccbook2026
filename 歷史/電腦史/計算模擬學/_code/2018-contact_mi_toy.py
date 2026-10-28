# -*- coding: utf-8 -*-
"""2018 玩具 MSA 互資訊接觸預測 (對應 wiki：計算模擬學 / 蛋白質共演化・DCA/互資訊)。

背景：Morcos 等 (2011) DCA、Marks 等 (2011) EVfold：MSA 中共演化位點對
互資訊 (MI) 高，暗示空間接觸。此處玩具 MSA：200 條序列、10 位點、字母表 q=4，
預設位點 2 與 8（0-based）共演化（95% 相同字母），其餘獨立均勻。
計算 10×10 MI 矩陣（nats），驗證 MI[2,8] 為最大值且超過次大值 2 倍以上。

只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(2018)

NSEQ, L, Q = 200, 10, 4
PAIR = (2, 8)
NOISE = 0.05


def compute_mi(msa):
    n, L = msa.shape
    mi = np.zeros((L, L))
    for i in range(L):
        for j in range(i + 1, L):
            joint = np.zeros((Q, Q))
            for a in range(n):
                joint[msa[a, i], msa[a, j]] += 1
            joint /= n
            pi = joint.sum(axis=1, keepdims=True)
            pj = joint.sum(axis=0, keepdims=True)
            m = 0.0
            for a in range(Q):
                for b in range(Q):
                    if joint[a, b] > 0:
                        m += joint[a, b] * np.log(joint[a, b] / (pi[a, 0] * pj[0, b]))
            mi[i, j] = mi[j, i] = m
    return mi


def main():
    msa = np.random.randint(0, Q, size=(NSEQ, L))
    # 植入共演化：位點 2、8 以 95% 機率取相同字母
    for s in range(NSEQ):
        val = np.random.randint(0, Q)
        msa[s, PAIR[0]] = val
        if np.random.rand() > NOISE:
            msa[s, PAIR[1]] = val
        else:
            msa[s, PAIR[1]] = np.random.randint(0, Q)

    mi = compute_mi(msa)
    # 找最大與次大（上三角、排除對角線）
    triu = [(mi[i, j], i, j) for i in range(L) for j in range(i + 1, L)]
    triu.sort(reverse=True)
    (m1, i1, j1), (m2, i2, j2) = triu[0], triu[1]
    ratio = m1 / (m2 + 1e-12)

    print(f"MSA: {NSEQ} 條 × {L} 位點, q={Q}, 植入共演化位點 {PAIR}")
    print("MI 矩陣 (nats, 取上三角前幾大):")
    for val, i, j in triu[:5]:
        print(f"  MI[{i},{j}] = {val:.4f}")
    print(f"最大 MI[{i1},{j1}]={m1:.4f}, 次大 MI[{i2},{j2}]={m2:.4f}, 比值={ratio:.2f} (要求>2)")
    ok = ((i1, j1) == PAIR) and (ratio > 2.0)
    assert ok, "MI 驗證失敗"
    print(f"VERIFICATION: MI28={m1:.4f} second={m2:.4f} ratio={ratio:.2f} PASS")


if __name__ == "__main__":
    main()
