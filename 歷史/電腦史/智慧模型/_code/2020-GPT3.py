# 2020 - GPT-3 規模湧現: 冪律 + 少樣本上下文學習 (few-shot, 無梯度)
# 對應本書: 2020-GPT-3規模湧現.md
# 公式: L ∝ N^-α (α≈0.076); P(答案|範例1..k, 問題) vs P(答案|問題)
# 展示: (1) sklearn 擬合 GPT-3 論文風的損失-參數冪律
#       (2) 凍結隨機投影特徵 + 最近質心: 示範數 0->5, 準確率湧現 (in-context 縮影)
import numpy as np
import torch
from sklearn.linear_model import LinearRegression


def main():
    # (1) 參數冪律: 論文風的 (參數量, 交叉熵損失) 點 -- 嚴格冪律 L=3.3·(N/1e8)^-0.076
    N = np.array([1.25e8, 3.5e8, 7.6e8, 1.3e9, 2.7e9, 6.7e9, 1.3e10, 1.75e11])
    L = 3.3 * (N / 1e8) ** -0.076
    reg = LinearRegression().fit(np.log10(N[:-1]).reshape(-1, 1), np.log10(L[:-1]))
    pred = 10 ** reg.predict([[np.log10(N[-1])]])[0]
    print(f"擬合 L ∝ N^-α: α={-reg.coef_[0]:.3f} (論文 α≈0.076; R²={reg.score(np.log10(N[:-1]).reshape(-1, 1), np.log10(L[:-1])):.3f})")
    print(f"  前7點外推175B損失={pred:.2f} (實際 {L[-1]:.2f} -- 小規模實驗預測大規模, GPT-4 路線)")

    # (2) 少樣本湧現: 高斯混合分類, 特徵凍結 (把「預訓練」凍成隨機投影), 只改示範數 k
    torch.manual_seed(0)
    P = torch.randn(2, 16)  # 凍結特徵 (模擬預訓練好的表徵, 此處用隨機投影代替)
    def feats(n):
        y = torch.randint(0, 2, (n,))
        X = torch.randn(n, 2) * 0.6 + torch.tensor([[-1.5, 0.0], [1.5, 0.0]])[y]
        return (X @ P), y
    _, yte = feats(0)
    Xte, yte = feats(400)
    for k in [0, 1, 5]:
        if k == 0:
            acc = 0.50
        else:
            Xd, yd = feats(2 * k)
            proto = torch.stack([Xd[yd == c].mean(0) for c in (0, 1)])  # 類質心 = 上下文示範
            acc = (torch.cdist(Xte, proto).argmin(1) == yte).float().mean().item()
        print(f"  {k}-shot 準確率={acc:.2f}")
    print("結論: 零梯度、只加示範, 準確率從猜測爬升 -- in-context learning 的玩具版; "
          "規模把這條曲線整條上移 (L∝N^-α)")


if __name__ == "__main__":
    main()
