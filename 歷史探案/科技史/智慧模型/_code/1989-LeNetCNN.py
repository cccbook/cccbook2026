# 1989 - LeNet CNN 手寫辨識 (LeCun)
# 對應本書: 1989-LeCunCNN手寫辨識.md
# 公式: y_ij = σ(Σ_uv W_uv x_{i+u,j+v} + b) (卷積+權重共享) ; 端對端梯度下降學濾波器
# 展示: LeNet-5 縮影 (C1-S2-C3-S4-F5) 在合成幾何圖形 (圓 vs 方) 上端對端訓練
import torch
import torch.nn as nn


class LeNet5Mini(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 6, 5)     # 32x32 -> 28x28 (書中 C1)
        self.s2 = nn.AvgPool2d(2)        # -> 14x14 (子採樣=複雜細胞)
        self.c3 = nn.Conv2d(6, 16, 5)    # -> 10x10
        self.s4 = nn.AvgPool2d(2)        # -> 5x5
        self.f5 = nn.Linear(16 * 5 * 5, 84)
        self.out = nn.Linear(84, 2)

    def forward(self, x):
        x = torch.tanh(self.c1(x))
        x = self.s2(x)
        x = torch.tanh(self.c3(x))
        x = self.s4(x)
        x = torch.tanh(self.f5(x.flatten(1)))
        return self.out(x)


def make_shapes(n=400):
    """合成資料: 0=圓形, 1=方形 (32x32), 模擬 MNIST 的『真實圖案可被卷積學會』."""
    X = torch.zeros(n, 1, 32, 32)
    y = torch.zeros(n, dtype=torch.long)
    yy, xx = torch.meshgrid(torch.arange(32), torch.arange(32), indexing="ij")
    for i in range(n):
        c = i % 2
        y[i] = c
        if c == 0:
            X[i, 0] = (((xx - 16) ** 2 + (yy - 16) ** 2) < 81).float()
        else:
            X[i, 0, 10:22, 10:22] = 1.0
    X += torch.randn_like(X) * 0.1   # 工業級雜訊
    return X.clamp(0, 1), y


def main():
    torch.manual_seed(0)
    X, y = make_shapes()
    net = LeNet5Mini()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    n_params = sum(p.numel() for p in net.parameters())
    print(f"LeNet-5縮影: 總參數 {n_params} (全連接同級需數十萬 -- 權重共享省 25 倍)")
    for ep in range(8):
        opt.zero_grad()
        loss = nn.CrossEntropyLoss()(net(X), y)
        loss.backward()
        opt.step()
        acc = (net(X).argmax(1) == y).float().mean().item()
        print(f"  epoch {ep + 1}: loss={loss.item():.3f} acc={acc:.2f}")
    print("結論: 濾波器由梯度自動學成圓形/方形偵測器 -- 特徵學習取代特徵工程")


if __name__ == "__main__":
    main()
