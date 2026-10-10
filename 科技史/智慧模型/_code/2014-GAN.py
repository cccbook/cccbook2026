# 2014 - GAN 對抗式生成 (Goodfellow et al.)
# 對應本書: 2014-GAN對抗式生成.md
# 公式: V = E[log D(x)] + E[log(1-D(G(z)))]; 最優 D* = p_data/(p_data+p_g); 極小化 JS 散度
# 展示: 1D 雙峰真實分布上, G 從單點追到雙峰, D 準確率回落 0.5 (納許均衡縮影)
import torch
import torch.nn as nn


def main():
    torch.manual_seed(0)
    # 真實分布: N(-2,0.3) 與 N(+2,0.3) 等比混合 (模式崩潰的試金石: 只學一峰即失敗)
    def real(n):
        pick = torch.randint(0, 2, (n, 1)).float() * 4 - 2
        return pick + torch.randn(n, 1) * 0.3
    G = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
    D = nn.Sequential(nn.Linear(1, 16), nn.ReLU(), nn.Linear(16, 1))
    og = torch.optim.Adam(G.parameters(), lr=2e-2)
    od = torch.optim.Adam(D.parameters(), lr=2e-2)
    bce = nn.BCEWithLogitsLoss()
    for step in range(3000):
        xr = real(128)
        z = torch.randn(128, 2)
        # 1) D: 真假二分 (鑑識官升級眼力)
        od.zero_grad()
        ld = bce(D(xr), torch.ones(128, 1)) + bce(D(G(z).detach()), torch.zeros(128, 1))
        ld.backward()
        od.step()
        # 2) G: 非飽和損失 -E[log D(G(z))] (偽造者升級手藝)
        og.zero_grad()
        lg = bce(D(G(torch.randn(128, 2))), torch.ones(128, 1))
        lg.backward()
        og.step()
    with torch.no_grad():
        fake = G(torch.randn(2000, 2)).ravel()
        left = (fake < 0).float().mean().item()
        d_real = torch.sigmoid(D(real(500))).mean().item()
        d_fake = torch.sigmoid(D(fake.view(-1, 1))).mean().item()
    print(f"生成樣本左峰比例={left:.2f} (目標0.50 -- 遠離0/1 即未模式崩潰)")
    print(f"D(真)={d_real:.2f} D(偽)={d_fake:.2f} (均衡時皆≈0.5, 偽造者追平鑑識官)")
    print(f"生成均值±標準差={fake.mean():.2f}±{fake.std():.2f} (真實≈0.00±2.02)")


if __name__ == "__main__":
    main()
