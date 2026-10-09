# 2013 - VAE 變分自編碼器 (Kingma & Welling)
# 對應本書: 2013-VAE變分自編碼器.md
# 公式: ELBO = E_q[log p(x|z)] - KL(q(z|x)||p(z)); z = μ + σ⊙ε (重參數化)
# 展示: 2D 雙團資料上, ELBO 上升 + 潛空間連續可採樣 (模糊但可生成 vs AE 的空洞)
import torch
import torch.nn as nn


class VAE(nn.Module):
    def __init__(self, latent=2):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(2, 32), nn.Tanh(), nn.Linear(32, 32), nn.Tanh())
        self.mu = nn.Linear(32, latent)
        self.lv = nn.Linear(32, latent)   # log σ²
        self.dec = nn.Sequential(nn.Linear(latent, 32), nn.Tanh(), nn.Linear(32, 2))

    def forward(self, x):
        h = self.enc(x)
        mu, lv = self.mu(h), self.lv(h)
        z = mu + (0.5 * lv).exp() * torch.randn_like(mu)  # 重參數化: 隨機性搬家到 ε
        xh = self.dec(z)
        recon = ((x - xh) ** 2).sum(1).mean()             # E_q[log p(x|z)] (高斯即MSE)
        kl = -0.5 * (1 + lv - mu ** 2 - lv.exp()).sum(1).mean()
        return recon + kl, recon, kl, z, xh


def main():
    torch.manual_seed(0)
    # 資料: 兩個高斯團 (模擬「兩個數字類別」)
    a = torch.randn(300, 2) * 0.4 + torch.tensor([2.0, 2.0])
    b = torch.randn(300, 2) * 0.4 + torch.tensor([-2.0, -2.0])
    X = torch.cat([a, b])
    net = VAE()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(300):
        opt.zero_grad()
        elbo, recon, kl, *_ = net(X)
        elbo.backward()
        opt.step()
    elbo, recon, kl, z, xh = net(X)
    print(f"ELBO={elbo.item():.3f} (重建項={recon.item():.3f} + KL項={kl.item():.3f})")
    # 連續性檢驗: 潛空間插值解碼應平滑橫跨兩團 (AE 會掉進空洞)
    with torch.no_grad():
        za = net.enc(a[:1])
        zb = net.enc(b[:1])
        ma, mb = net.mu(za), net.mu(zb)
        path = torch.stack([ma[0] * (1 - t) + mb[0] * t for t in torch.linspace(0, 1, 5)])
        decoded = net.dec(path)
    print("潛插值解碼路徑 (應從[2,2]平滑走到[-2,-2]):")
    for p in decoded:
        print(f"  [{p[0]:.2f}, {p[1]:.2f}]")
    # 可採樣性: 先驗採樣直接解碼
    with torch.no_grad():
        samp = net.dec(torch.randn(4, 2))
    print("先驗採樣解碼:", [[round(float(v), 2) for v in s] for s in samp])


if __name__ == "__main__":
    main()
