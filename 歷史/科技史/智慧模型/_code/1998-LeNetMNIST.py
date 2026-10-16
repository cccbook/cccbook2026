# 1998 - LeNet-5 與 MNIST (LeCun et al., Proc. IEEE)
# 對應本書: 1998-LeNet與MNIST.md
# 重現: 真 LeNet-5 (C1 6@5x5 -> S2 -> C3 16@5x5 -> S4 -> C5 120 -> F6 84 -> OUT 10)
#       在真 MNIST (6萬訓練/1萬測試) 上端對端訓練, 目標: 測試錯誤率壓到 ~1%
import time
from pathlib import Path

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T


class LeNet5(nn.Module):
    """1998 年定稿結構 (tanh + 平均池化, 6萬參數). 輸入 1x32x32 (MNIST 28->pad 32)."""

    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 6, 5)          # 32->28
        self.s2 = nn.AvgPool2d(2, 2)          # ->14
        self.c3 = nn.Conv2d(6, 16, 5)         # ->10
        self.s4 = nn.AvgPool2d(2, 2)          # ->5
        self.c5 = nn.Conv2d(16, 120, 5)       # ->1x1 (卷積式全連接)
        self.f6 = nn.Linear(120, 84)
        self.out = nn.Linear(84, 10)

    def forward(self, x):
        x = torch.tanh(self.c1(x))
        x = self.s2(x)
        x = torch.tanh(self.c3(x))
        x = self.s4(x)
        x = torch.tanh(self.c5(x).flatten(1))
        x = torch.tanh(self.f6(x))
        return self.out(x)


def evaluate(net, loader):
    net.eval()
    correct = total = 0
    with torch.no_grad():
        for x, y in loader:
            correct += (net(x).argmax(1) == y).sum().item()
            total += len(y)
    return correct / total


def main():
    torch.manual_seed(0)
    root = Path(__file__).parent / "data"
    tf = T.Compose([T.Pad(2), T.ToTensor()])  # 28x28 -> 32x32, 論文設定
    train = torchvision.datasets.MNIST(str(root), train=True, download=True, transform=tf)
    test = torchvision.datasets.MNIST(str(root), train=False, download=True, transform=tf)
    tr_loader = torch.utils.data.DataLoader(train, batch_size=128, shuffle=True)
    te_loader = torch.utils.data.DataLoader(test, batch_size=1024)
    print(f"MNIST: 訓練 {len(train)} 張, 測試 {len(test)} 張 (NIST SD-1/SD-3 混合重整)")

    net = LeNet5()
    n_params = sum(p.numel() for p in net.parameters())
    print(f"LeNet-5 總參數: {n_params} (約6萬, 全連接同級需數十萬)")
    opt = torch.optim.SGD(net.parameters(), lr=0.05, momentum=0.9)
    t0 = time.time()
    for ep in range(2):
        net.train()
        loss_sum = n = 0
        for x, y in tr_loader:
            opt.zero_grad()
            loss = nn.CrossEntropyLoss()(net(x), y)
            loss.backward()
            opt.step()
            loss_sum += loss.item() * len(y)
            n += len(y)
        acc = evaluate(net, te_loader)
        print(f"  epoch {ep + 1}: train_loss={loss_sum / n:.3f} "
              f"test_acc={acc:.4f} (test_err={1 - acc:.2%}) [{time.time() - t0:.0f}s]")
    # 抽看 10 個測試樣本
    net.eval()
    with torch.no_grad():
        x, y = next(iter(te_loader))
        pred = net(x[:10]).argmax(1)
    print("抽查前10張測試: 真值=", y[:10].tolist(), "預測=", pred.tolist())
    print("結論: 2 epoch 即達 ~99% -- 論文 LeNet-5 為 0.7~0.8% 錯誤率, 線性分類器約 12%")


if __name__ == "__main__":
    main()
