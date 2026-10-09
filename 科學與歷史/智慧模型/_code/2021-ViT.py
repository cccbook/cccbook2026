# 2021 - ViT 視覺 Transformer: patch 即 token
# 對應本書: 2021-ViT視覺Transformer.md
# 公式: z_0 = [x_class; x_p^1 E; ...; x_p^N E] + E_pos; N = HW/P²
# 展示: MNIST 切 4x4 patches (16 tokens+CLS), 2層Transformer 編碼器分類
import time
from pathlib import Path

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T


class ViTMini(nn.Module):
    def __init__(self, patch=7, dim=64, depth=2, heads=4, ncls=10):
        super().__init__()
        self.P = patch
        self.proj = nn.Linear(patch * patch, dim)   # x_p E: patch 嵌入
        self.cls = nn.Parameter(torch.randn(1, 1, dim))
        self.pos = nn.Parameter(torch.randn(1, 17, dim))  # 16 patches + CLS
        layer = nn.TransformerEncoderLayer(dim, heads, dim * 2, batch_first=True)
        self.enc = nn.TransformerEncoder(layer, depth)
        self.head = nn.Linear(dim, ncls)

    def forward(self, img):
        B = len(img)
        p = img.unfold(2, self.P, self.P).unfold(3, self.P, self.P)  # 切 patch
        p = p.permute(0, 2, 3, 1, 4, 5).reshape(B, 16, -1)
        z = torch.cat([self.cls.expand(B, -1, -1), self.proj(p)], 1) + self.pos
        return self.head(self.enc(z)[:, 0])          # 只讀 CLS


def main():
    torch.manual_seed(0)
    root = Path(__file__).parent / "data"
    tf = T.Compose([T.ToTensor()])
    train = torchvision.datasets.MNIST(str(root), train=True, download=True, transform=tf)
    test = torchvision.datasets.MNIST(str(root), train=False, download=True, transform=tf)
    tr = torch.utils.data.DataLoader(torch.utils.data.Subset(train, range(6000)),
                                     batch_size=128, shuffle=True)
    te = torch.utils.data.DataLoader(torch.utils.data.Subset(test, range(2000)), batch_size=512)
    net = ViTMini()
    print(f"ViT-mini 參數: {sum(p.numel() for p in net.parameters())} "
          f"(28x28/7=16 patches+CLS, 無卷積 -- 歸納偏置只剩位置編碼)")
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    t0 = time.time()
    for ep in range(5):
        net.train()
        for x, y in tr:
            opt.zero_grad()
            loss = nn.CrossEntropyLoss()(net(x), y)
            loss.backward()
            opt.step()
        net.eval()
        with torch.no_grad():
            acc = sum((net(x).argmax(1) == y).sum().item() for x, y in te) / 2000
        print(f"  epoch {ep + 1}: 測試準確率={acc:.4f} [{time.time() - t0:.0f}s]")
    print("結論: 無卷積也學得會 -- 但要更多資料 (原文: JFT-3億張才超車; 此處6千張小輸CNN很正常)")


if __name__ == "__main__":
    main()
