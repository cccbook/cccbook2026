# 2023 - RT-2 視覺語言動作模型: 動作 token 化, 其餘交給 Transformer
# 對應本書: 2023-RT-2視覺語言動作模型.md
# 公式: a_t ∈ R^7 -> 256-bin 離散化 -> token; L = -E[log p(action tokens|image, instruction)]
# 展示: 合成「影像+指令->7維動作」上, 端對端學出 reaching (位置誤差收斂), 語義泛化縮影
import torch
import torch.nn as nn
import torch.nn.functional as F


class RT2Mini(nn.Module):
    def __init__(self, d=48, bins=32):
        super().__init__()
        self.bins = bins
        self.venc = nn.Sequential(nn.Linear(16, 64), nn.ReLU(), nn.Linear(64, d))
        self.tenc = nn.Embedding(20, d)
        layer = nn.TransformerEncoderLayer(d, 4, d * 2, batch_first=True)
        self.tr = nn.TransformerEncoder(layer, 2)
        self.head = nn.Linear(d, 7 * bins)  # 7 維動作 × 離散 bins

    def forward(self, v, t):
        z = torch.cat([self.venc(v).unsqueeze(1), self.tenc(t)], 1)
        h = self.tr(z)[:, -1]
        return self.head(h).view(-1, 7, self.bins)


def main():
    torch.manual_seed(0)
    N, BINS = 1200, 32
    V = torch.randn(N, 16)                       # 影像特徵
    T = torch.randint(0, 20, (N, 4))             # 指令 token (如 "pick red cup")
    A = torch.zeros(N, 7, dtype=torch.long)
    A[:, :2] = ((V[:, :2] + 3) / 6 * (BINS - 1)).long().clamp(0, BINS - 1)  # reaching
    A[:, 2:4] = ((V[:, 2:4] + 3) / 6 * (BINS - 1)).long().clamp(0, BINS - 1)  # 姿態
    A[:, 4] = T.sum(1) % BINS                    # 夾爪 (由指令決定 -- 語義 grounding)
    A[:, 5] = ((V[:, 4] + T[:, 0].float() / 10 + 3) / 6.2 * (BINS - 1)).long().clamp(0, BINS - 1)
    A[:, 6] = ((V[:, 5] - T[:, 1].float() / 10 + 3) / 6.2 * (BINS - 1)).long().clamp(0, BINS - 1)
    net = RT2Mini(bins=BINS)
    opt = torch.optim.Adam(net.parameters(), lr=5e-3)
    for ep in range(200):
        opt.zero_grad()
        loss = sum(F.cross_entropy(net(V, T)[:, j], A[:, j]) for j in range(7)) / 7
        loss.backward()
        opt.step()
    with torch.no_grad():
        pred = net(V, T).argmax(-1)
        acc = (pred == A).float().mean().item()
        tol = ((pred - A).abs() <= 1).float().mean().item()  # 機器人只在乎誤差多小
        err = ((pred[:, :2].float() - A[:, :2].float()).abs().mean().item())
    print(f"動作 token 準確率={acc:.3f} (±1 bin 容忍={tol:.3f}) 位置維平均 bin 誤差={err:.2f}/{BINS}")
    print("結論: 動作即另一種語言 -- 誤差以 bin 計, 容忍內即抓得住 (VLM 語義泛化)")


if __name__ == "__main__":
    main()
