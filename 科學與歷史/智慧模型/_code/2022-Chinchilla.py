# 2022 - Chinchilla 規模法則: 計算最優的參數-資料配比
# 對應本書: 2022-Chinchilla規模法則.md
# 公式: C ≈ 6ND; L(N,D) = E + A/N^α + B/D^β (Hoffmann 係數: E=1.69,A=406.4,B=410.7,α=0.34,β=0.28)
# 展示: 固定算力下網格搜尋最優 (N,D) -- D_opt ≈ 20·N_opt, N_opt ∝ C^0.5 (GPT-3 欠訓的數學證明)
import numpy as np
from sklearn.linear_model import LinearRegression


def L(N, D, E=1.69, A=406.4, B=410.7, a=0.34, b=0.28):
    return E + A / N ** a + B / D ** b


def main():
    print("固定算力 C=6ND 下的最優配比 (參數曲面 L(N,D) 網格搜尋):")
    Ns, Ds, Cs = [], [], [1e20, 1e21, 1e22, 1e23, 1e24]
    for C in Cs:
        best = None
        for eN in np.arange(8, 13.0, 0.1):           # N: 1e8 ~ 1e13
            N = 10 ** eN
            D = C / (6 * N)
            if D < 1e8:
                continue
            v = L(N, D)
            if best is None or v < best[0]:
                best = (v, N, D)
        _, N, D = best
        Ns.append(N)
        Ds.append(D)
        print(f"  C={C:.0e}: N_opt={N:.2e} D_opt={D:.2e} D/N={D / N:.0f}")
    # N_opt ∝ C^? : log-log 擬合 (論文 IsoFLOP 給 0.50; 參數曲面給 ~0.45, 同指向等比放大)
    eC = np.log10(Cs).reshape(-1, 1)
    pN = LinearRegression().fit(eC, np.log10(Ns)).coef_[0]
    pD = LinearRegression().fit(eC, np.log10(Ds)).coef_[0]
    print(f"擬合: N_opt ∝ C^{pN:.2f}, D_opt ∝ C^{pD:.2f} "
          f"(皆≈0.5 -- 參數與資料等比放大; IsoFLOP 剖面給 0.50/0.50, 比例約 1:20)")
    # GPT-3 覆盤: 同算力下 Chinchilla 配比 vs GPT-3 實際配比
    C3 = 6 * 1.75e11 * 3e11
    N3, D3 = 1.75e11, 3e11
    Nc = (C3 / 120) ** 0.5  # D=20N 且 C=6ND -> N=√(C/120)
    Dc = C3 / (6 * Nc)
    print(f"GPT-3 算力覆盤: GPT-3 用 N={N3:.1e}/D={D3:.1e}, L={L(N3, D3):.3f}; "
          f"Chinchilla 配比 N={Nc:.1e}/D={Dc:.1e}, L={L(Nc, Dc):.3f}")
    print("結論: 同算力下『小模型+多資料』損失更低 -- 70B/1.4T 打敗 280B/0.3T, LLaMA 跟進")


if __name__ == "__main__":
    main()
