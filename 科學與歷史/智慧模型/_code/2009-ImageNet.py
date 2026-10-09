# 2009 - ImageNet 資料集: 規模法則 + 增廣管線
# 對應本書: 2009-ImageNet資料集.md
# 公式: Error ∝ N^-α (α≈0.2-0.5); ImageNet = WordNet概念樹 × 百萬級標註影像
# 展示: (1) sklearn 在 log-log 尺度擬合誤差-資料冪律, 估出 α
#       (2) torchvision 資料增廣管線 (裁剪/翻轉/抖色) 的張量級演示
import numpy as np
import torch
import torchvision.transforms as T
from sklearn.linear_model import LinearRegression


def main():
    # (1) 冪律擬合: 論文風的誤差點 (N: 資料量, err: top-5錯誤率示意, 仿 Sun et al. 2017 曲線形狀)
    N = np.array([1e4, 1e5, 1e6, 1e7, 1.4e7])
    err = np.array([0.62, 0.38, 0.22, 0.13, 0.10])
    reg = LinearRegression().fit(np.log10(N).reshape(-1, 1), np.log10(err))
    alpha = -reg.coef_[0]
    print(f"擬合 log(err) = a - α·log(N): α={alpha:.2f} (書中 α≈0.2-0.5, 資料每增10倍誤差打 {10 ** -alpha:.1%} 折)")
    print(f"  R²={reg.score(np.log10(N).reshape(-1, 1), np.log10(err)):.3f} (冪律在log-log下是直線)")

    # (2) 增廣管線: AlexNet 靠它把 120萬張洗成等效數倍 -- 單張影像走一遍管線
    aug = T.Compose([T.RandomResizedCrop(32, scale=(0.5, 1.0)),
                     T.RandomHorizontalFlip(p=1.0),
                     T.ColorJitter(0.4, 0.4, 0.4),
                     T.ToTensor()])
    from PIL import Image
    img = Image.fromarray((np.random.default_rng(0).random((64, 64, 3)) * 255).astype("uint8"))
    outs = torch.stack([aug(img) for _ in range(4)])
    print(f"增廣輸出: {tuple(outs.shape)} (4個版本, 均值={outs.mean():.3f}, 標準差={outs.std():.3f})")
    print("結論: 資料集×增廣 = 2012 年的燃料; 沒有 ImageNet 就沒有 AlexNet")


if __name__ == "__main__":
    main()
