# 2021 - AlphaFold2: 共演化 -> 接觸 -> 結構 (DCA-lite 縮影)
# 對應本書: 2021-AlphaFold2.md
# 鏈條: 序列 -> Evoformer(MSA/對表示互質) -> 結構模組 -> 座標; 此處演示第一步:
#       MSA 共變異 (互信息) 還原接觸對 -- 「演化把結構寫進了序列相關性」
import numpy as np


def mutual_info(msa, i, j, A=4):
    joint = np.zeros((A, A))
    for a, b in msa[:, [i, j]]:
        joint[a, b] += 1
    joint /= len(msa)
    pi, pj = joint.sum(1, keepdims=True), joint.sum(0, keepdims=True)
    nz = joint > 0
    return float((joint[nz] * np.log(joint[nz] / (pi @ pj)[nz])).sum())


def main():
    rng = np.random.default_rng(0)
    L, N, TRUE = 10, 3000, [(1, 6), (2, 7)]  # 真接觸對 (相隔三角不等式的共演化對)
    msa = rng.integers(0, 4, (N, L))
    for i, j in TRUE:  # 埋入共演化: j 的字母由 i 決定 (加 20% 雜訊)
        msa[:, j] = np.where(rng.random(N) < 0.8, (msa[:, i] + 1) % 4, msa[:, j])
    MI = np.zeros((L, L))
    for i in range(L):
        for j in range(i + 1, L):
            MI[i, j] = MI[j, i] = mutual_info(msa, i, j)
    top = sorted([(MI[i, j], (i, j)) for i in range(L) for j in range(i + 1, L)],
                 reverse=True)[:4]
    print("互信息最高的前4對 (位置, MI):", [(p, round(float(m), 3)) for m, p in top])
    hit = sum(1 for _, p in top[:2] if p in TRUE or p[::-1] in TRUE)
    print(f"真接觸對 {TRUE} 命中 {hit}/2 -- 共演化還原接觸 (Evoformer 輸入的對表示即此)")
    print("結論: MSA->對表示->FAPE結構模組->座標+pLDDT; 第一步是統計, 後面是幾何")


if __name__ == "__main__":
    main()
