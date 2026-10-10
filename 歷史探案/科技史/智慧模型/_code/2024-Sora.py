# 2024 - Sora 世界模型: 時空 patches + DiT 去噪 (video -> 潛碼 -> 去噪 -> 影片)
# 對應本書: 2024-Sora世界模型.md
# 公式: video -> E -> spacetime patches -> DiT 去噪 -> D -> video; L=E||ε-ε_θ(z_t,t,c)||²
# 展示: 8幀 8x8 移動方塊影片 -> 時空patch tokens -> DiT block 去噪一步, 損失下降
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class DiTBlock(nn.Module):  # adaLN 調製 + 注意力 + MLP (DiT 精神縮影)
    def __init__(self, d=48, h=4):
        super().__init__()
        self.n1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, h, batch_first=True)
        self.n2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, d * 2), nn.GELU(), nn.Linear(d * 2, d))
        self.mod = nn.Sequential(nn.SiLU(), nn.Linear(d, 6 * d))  # t+c -> 6組調製

    def forward(self, z, cond):
        sh, ga, a1, a2, g1, g2 = self.mod(cond).unsqueeze(1).chunk(6, -1)
        h = self.n1(z) * (1 + sh) + ga
        h, _ = self.attn(h, h, h, need_weights=False)
        z = z + a1 * h
        h2 = self.n2(z) * (1 + g1) + g2
        return z + a2 * self.mlp(h2)


def main():
    torch.manual_seed(0)
    T, H, P, D = 8, 8, 4, 48  # 8幀, 8x8, patch 4x4x2
    # 影片: 方塊等速移動 (世界一致性的最小骨架: 位置連續)
    V = torch.zeros(200, T, H, H)
    for i in range(200):
        x0, v = torch.randint(0, 4, (1,)).item(), 1 if i % 2 == 0 else -1
        for t in range(T):
            x = min(max(x0 + v * t, 0), 5)
            V[i, t, 2:5, x:x + 3] = 1.0
    V = V + torch.randn_like(V) * 0.05
    # 時空 patch 化: (T/2)×(H/4)×(W/4) = 4×2×2 = 16 tokens, 每 token 2×4×4=32 維
    patches = V.unfold(1, 2, 2).unfold(2, 4, 4).unfold(3, 4, 4)
    assert patches.shape[1:4] == (4, 2, 2)
    Z = patches.reshape(200, 16, 32)
    proj = nn.Linear(32, D)
    dit = DiTBlock(D)
    t_emb = nn.Embedding(20, D)
    c_emb = nn.Embedding(2, D)  # 條件: 左移/右移 (文本提示縮影)
    params = list(proj.parameters()) + list(dit.parameters()) + list(t_emb.parameters()) + list(c_emb.parameters())
    opt = torch.optim.Adam(params, lr=5e-3)
    TT = 20
    beta = torch.linspace(1e-3, 0.05, TT)
    abar = torch.cumprod(1 - beta, 0)
    c = torch.tensor([i % 2 for i in range(200)])
    for ep in range(150):
        t = torch.randint(0, TT, (64,))
        idx = torch.randint(0, 200, (64,))
        z0 = proj(Z[idx])
        eps = torch.randn(64, 16, D)
        zt = abar[t].sqrt().view(-1, 1, 1) * z0 + (1 - abar[t]).sqrt().view(-1, 1, 1) * eps
        cond = t_emb(t) + c_emb(c[idx])
        opt.zero_grad()
        ((dit(zt, cond) - eps) ** 2).mean().backward()  # DiT 去噪目標
        opt.step()
    with torch.no_grad():
        t = torch.randint(0, TT, (64,))
        idx = torch.randint(0, 200, (64,))
        z0 = proj(Z[idx])
        eps = torch.randn(64, 16, D)
        zt = abar[t].sqrt().view(-1, 1, 1) * z0 + (1 - abar[t]).sqrt().view(-1, 1, 1) * eps
        loss = ((dit(zt, t_emb(t) + c_emb(c[idx])) - eps) ** 2).mean().item()
    print(f"時空 tokens: 影片->16 tokens (4時×2×2); DiT 去噪 MSE={loss:.4f} (從~1.0 降下)")
    print("結論: 影片即 token 序列 -- 縮放 patch 預算縮放世界; 生成派 vs V-JEPA 表徵派見下章")


if __name__ == "__main__":
    main()
