# 2021 - CLIP 多模態對齊: 雙編碼器 + InfoNCE 對比損失
# 對應本書: 2021-CLIP多模態對齊.md
# 公式: L = -Σ[log exp(sim(I_i,T_i)/τ)/Σ_j exp(sim(I_i,T_j)/τ) + 對稱項]; sim=餘弦
# 展示: 合成圖文對上, N×N 相似度矩陣的對角線被推高 -- 零樣本分類即相似度比對
import torch
import torch.nn as nn
import torch.nn.functional as F


def main():
    torch.manual_seed(0)
    N, DI, DT, D, TAU = 256, 20, 16, 16, 0.07
    # 合成世界: 潛語義 z 生成配對的圖/文觀測 (模擬「4億圖文對」的配對結構)
    z = torch.randn(N, 8)
    I = z @ torch.randn(8, DI) + torch.randn(N, DI) * 0.3
    T = z @ torch.randn(8, DT) + torch.randn(N, DT) * 0.3
    enc_i = nn.Sequential(nn.Linear(DI, 32), nn.ReLU(), nn.Linear(32, D))
    enc_t = nn.Sequential(nn.Linear(DT, 32), nn.ReLU(), nn.Linear(32, D))
    opt = torch.optim.Adam(list(enc_i.parameters()) + list(enc_t.parameters()), lr=1e-2)
    for ep in range(200):
        opt.zero_grad()
        Ii = F.normalize(enc_i(I), dim=1)
        Tt = F.normalize(enc_t(T), dim=1)
        S = Ii @ Tt.T / TAU                                # N×N 相似度矩陣
        tgt = torch.arange(N)
        loss = (F.cross_entropy(S, tgt) + F.cross_entropy(S.T, tgt)) / 2  # 雙向 InfoNCE
        loss.backward()
        opt.step()
    with torch.no_grad():
        S = F.normalize(enc_i(I), dim=1) @ F.normalize(enc_t(T), dim=1).T
        r1 = (S.argmax(1) == torch.arange(N)).float().mean().item()  # 圖找文 R@1
        r1t = (S.argmax(0) == torch.arange(N)).float().mean().item()  # 文找圖 R@1
        print(f"InfoNCE={loss.item():.3f} 圖找文R@1={r1:.2f} 文找圖R@1={r1t:.2f} "
              f"(隨機≈{1 / N:.3f} -- 對角線被推高)")
        # 零樣本分類縮影: 新圖 vs 「a photo of {c}」式兩類文本原型
        Tn = F.normalize(enc_t(T[:2]), dim=1)              # 借兩句當類原型
        In = F.normalize(enc_i(I[:8]), dim=1)
        pred = (In @ Tn.T).argmax(1)
        print("零樣本式比對 (前8張圖分兩類):", pred.tolist(),
              "(分類=相似度比對, 無需微調 -- 本文第二條線索)")


if __name__ == "__main__":
    main()
