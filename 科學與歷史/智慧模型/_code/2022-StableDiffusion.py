# 2022 - Stable Diffusion 開源擴散: 潛空間擴散 + 文字條件 + CFG
# 對應本書: 2022-StableDiffusion開源擴散.md
# 公式: L_LDM = E||ε-ε_θ(z_t,t,c)||²; CFG: ε̃=ε_∅+w(ε_c-ε_∅)
# 展示: 8x8 圓/方圖 -> PCA 潛碼(8維) -> 潛空間擴散 (文字條件) -> 解碼, CFG 加強聽話度
import torch
import torch.nn as nn
from sklearn.decomposition import PCA


def make_images(n=600):
    X = torch.zeros(n, 64)
    y = torch.zeros(n, dtype=torch.long)
    yy, xx = torch.meshgrid(torch.arange(8), torch.arange(8), indexing="ij")
    d2 = (xx - 3.5) ** 2 + (yy - 3.5) ** 2
    for i in range(n):
        c = i % 2
        y[i] = c
        img = torch.zeros(8, 8)
        if c == 0:
            img[(d2 > 3) & (d2 < 14)] = 1.0   # 圓環 (潛空間與方框分得開)
        else:
            img[1:7, 1:7] = 1.0
            img[2:6, 2:6] = 0.0               # 方框
        X[i] = img.reshape(-1) + torch.randn(64) * 0.05
    return X.clamp(0, 1), y


NULL = 2  # 第3個 id = 無條件 (CFG 的 ∅)


def main():
    torch.manual_seed(0)
    X, y = make_images()
    pca = PCA(n_components=8).fit(X.numpy())  # E(x): 第一性原理的壓縮器 (VAE 的精神縮影)
    Z = torch.tensor(pca.transform(X.numpy()), dtype=torch.float32)
    print("像素 64 維 -> 潛碼 8 維 (壓縮 8x -- 先壓縮再去噪, 省計算)")

    T = 50
    beta = torch.linspace(1e-3, 0.05, T)
    abar = torch.cumprod(1 - beta, 0)
    txt = nn.Embedding(3, 4)  # τ(c): 圓/方/null 各一向量 (CLIP text embedding 縮影)

    class Eps(nn.Module):
        def __init__(self):
            super().__init__()
            self.te = nn.Embedding(T, 4)
            self.m = nn.Sequential(nn.Linear(8 + 4 + 4, 64), nn.ReLU(),
                                   nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 8))

        def forward(self, zt, t, c):  # 條件concat = 交叉注意力的最小骨架
            return self.m(torch.cat([zt, self.te(t), txt(c)], 1))

    net = Eps()
    opt = torch.optim.Adam(list(net.parameters()) + list(txt.parameters()), lr=1e-2)
    for ep in range(400):
        t = torch.randint(0, T, (256,))
        idx = torch.randint(0, len(Z), (256,))
        z0, c = Z[idx], y[idx]
        eps = torch.randn(256, 8)
        zt = abar[t].sqrt().unsqueeze(1) * z0 + (1 - abar[t]).sqrt().unsqueeze(1) * eps
        c_in = torch.where(torch.rand(256) < 0.1, torch.full_like(c, NULL), c)  # 10% 練無條件分支
        opt.zero_grad()
        ((net(zt, t, c_in) - eps) ** 2).mean().backward()  # L_LDM: 普通 MSE
        opt.step()
    # CFG 採樣: ε̃ = ε_∅ + w(ε_c - ε_∅); 圓/方各生 200 個, 比較 w=0(無條件) vs 3(強引導)
    print("CFG 效果 (生成落到『要求類別』的比例):")
    with torch.no_grad():
        center = {c: Z[y == c].mean(0) for c in (0, 1)}
        for w in [0.0, 3.0]:
            ok = tot = 0
            for c in (0, 1):
                z = torch.randn(200, 8)
                cc = torch.full((200,), c, dtype=torch.long)
                nu = torch.full((200,), NULL, dtype=torch.long)
                for t in range(T - 1, -1, -1):
                    tt = torch.full((200,), t, dtype=torch.long)
                    e = net(z, tt, nu) + w * (net(z, tt, cc) - net(z, tt, nu))
                    mu = (z - beta[t] / (1 - abar[t]).sqrt() * e) / (1 - beta[t]).sqrt()
                    z = mu + (beta[t].sqrt() * torch.randn_like(z) if t > 0 else 0)
                d0 = ((z - center[0]) ** 2).sum(1)
                d1 = ((z - center[1]) ** 2).sum(1)
                pred = torch.where(d0 < d1, torch.zeros_like(d0).long(),
                                   torch.ones_like(d0).long())  # 離誰近即哪類
                ok += (pred == c).sum().item()
                tot += 200
            print(f"  w={w}: 指派準確率={ok / tot:.2f} "
                  f"({'聽從文字條件' if ok / tot > 0.8 else '不分條件亂生'})")
    print("結論: 潛擴散(CPU秒級) + 交叉注意力(文字開口) + CFG(聽話旋鈕) = 開源擴散三件套")


if __name__ == "__main__":
    main()
