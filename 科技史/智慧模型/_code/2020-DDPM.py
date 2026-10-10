# 2020 - DDPM 擴散模型 (Ho et al.): 加噪可一步直達, 去噪學預測雜訊
# 對應本書: 2020-DDPM擴散模型.md
# 公式: x_t = √ᾱ_t x_0 + √(1-ᾱ_t) ε; L_simple = E||ε - ε_θ(x_t,t)||²
# 展示: 1D 雙峰資料上, MLP 噪聲預測器 + 100 步反向鏈, 從純雜訊鑿回雙峰
import torch
import torch.nn as nn


def main():
    torch.manual_seed(0)
    # 資料: N(-2,0.2) 與 N(+2,0.2) -- GAN 章的老朋友, 換擴散再解一次
    def real(n):
        pick = torch.randint(0, 2, (n, 1)).float() * 4 - 2
        return pick + torch.randn(n, 1) * 0.2
    T, NB = 100, 16
    beta = torch.linspace(1e-3, 0.05, T)          # 雜訊排程
    alpha = 1 - beta
    abar = torch.cumprod(alpha, 0)

    class Eps(nn.Module):  # ε_θ(x_t, t): 時間嵌入 + MLP (U-Net 的精神縮影)
        def __init__(self):
            super().__init__()
            self.te = nn.Embedding(T, 8)
            self.m = nn.Sequential(nn.Linear(9, 64), nn.ReLU(),
                                   nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 1))

        def forward(self, xt, t):
            return self.m(torch.cat([xt, self.te(t)], 1))

    net = Eps()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(800):
        x0 = real(256)
        t = torch.randint(0, T, (256,))
        eps = torch.randn(256, 1)
        xt = abar[t].sqrt().unsqueeze(1) * x0 + (1 - abar[t]).sqrt().unsqueeze(1) * eps
        opt.zero_grad()
        ((net(xt, t) - eps) ** 2).mean().backward()  # L_simple: 普通 MSE
        opt.step()
    with torch.no_grad():
        loss = ((net(xt, t) - eps) ** 2).mean().item()
    print(f"噪聲預測 MSE={loss:.4f} (訓練像回歸一樣穩定 -- vs GAN 的賽局)")
    # 反向採樣: 從純雜訊出發去噪 100 步
    with torch.no_grad():
        x = torch.randn(2000, 1)
        for t in range(T - 1, -1, -1):
            tt = torch.full((len(x),), t, dtype=torch.long)
            mu = (x - beta[t] / (1 - abar[t]).sqrt() * net(x, tt)) / alpha[t].sqrt()
            x = mu + (beta[t].sqrt() * torch.randn_like(x) if t > 0 else 0)
    left = (x < 0).float().mean().item()
    print(f"生成左峰比例={left:.2f} (目標0.50 -- 雙峰皆鑿出, 無模式崩潰)")
    print(f"生成均值±標準差={x.mean():.2f}±{x.std():.2f} (真實≈0.00±2.01)")
    print("結論: GAN 學真不真、VAE 學像不像、DDPM 學雜訊在哪 -- 第三條路最穩")


if __name__ == "__main__":
    main()
