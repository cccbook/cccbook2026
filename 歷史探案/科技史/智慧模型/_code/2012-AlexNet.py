# 2012 - AlexNet 影像革命 (Krizhevsky-Sutskever-Hinton)
# 對應本書: 2012-AlexNet影像革命.md
# 公式: ReLU f(x)=max(0,x); Dropout h̃=m⊙h, m~Bernoulli(0.5)
# 展示: 迷你 AlexNet (5卷積+3全連接+ReLU+Dropout) 在 MNIST(放大32x32) 上 1 epoch 即超越線性基線
import time
from pathlib import Path

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T
from sklearn.linear_model import LogisticRegression


class MiniAlexNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 48, 5, padding=2), nn.ReLU(), nn.MaxPool2d(2),   # 32->16
            nn.Conv2d(48, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 16->8
            nn.Conv2d(128, 192, 3, padding=1), nn.ReLU(),                  # 8
            nn.Conv2d(192, 192, 3, padding=1), nn.ReLU(),
            nn.Conv2d(192, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 8->4
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.5), nn.Linear(128 * 4 * 4, 512), nn.ReLU(),
            nn.Dropout(0.5), nn.Linear(512, 512), nn.ReLU(),
            nn.Linear(512, 10))

    def forward(self, x):
        return self.classifier(self.features(x).flatten(1))


def main():
    torch.manual_seed(0)
    root = Path(__file__).parent / "data"
    tf = T.Compose([T.Resize(32), T.ToTensor()])
    train = torchvision.datasets.MNIST(str(root), train=True, download=True, transform=tf)
    test = torchvision.datasets.MNIST(str(root), train=False, download=True, transform=tf)
    # 為快: 取 12000/3000 子集 (完整集同理, 只是更久)
    tr = torch.utils.data.Subset(train, range(12000))
    te = torch.utils.data.Subset(test, range(3000))
    tr_l = torch.utils.data.DataLoader(tr, batch_size=128, shuffle=True)
    te_l = torch.utils.data.DataLoader(te, batch_size=1024)

    # 基線: 線性分類器 (sklearn 邏輯回歸; 只看3000張會過擬合 -- 正是小資料+大模型的困境)
    Xb = train.data[:3000].float().div(255).reshape(3000, -1).numpy()
    yb = train.targets[:3000].numpy()
    Xt = test.data[:3000].float().div(255).reshape(3000, -1).numpy()
    yt = test.targets[:3000].numpy()
    clf = LogisticRegression(max_iter=300).fit(Xb, yb)
    print(f"線性基線: 訓練準確率={clf.score(Xb, yb):.3f}, 測試準確率={clf.score(Xt, yt):.3f} "
          f"(過擬合 -- 呼應書中_dropout_要解決的問題)")

    net = MiniAlexNet()
    print(f"MiniAlexNet 參數: {sum(p.numel() for p in net.parameters())} "
          f"(原版6千萬, 此處縮小以便CPU演示; 三兇器 ReLU+Dropout+增廣全在)")
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    # 增廣: 小幅平移 (數字不能水平翻轉 -- 7 會變成別的字, 這是增廣需尊重資料的教訓)
    aug = T.RandomAffine(degrees=0, translate=(0.08, 0.08))
    t0 = time.time()
    for ep in range(4):
        net.train()
        for x, y in tr_l:
            opt.zero_grad()
            loss = nn.CrossEntropyLoss()(net(aug(x)), y)
            loss.backward()
            opt.step()
        net.eval()
        with torch.no_grad():
            acc = sum((net(x).argmax(1) == y).sum().item() for x, y in te_l) / len(te)
        print(f"  epoch {ep + 1}: 測試準確率={acc:.4f} (錯誤率={1 - acc:.2%}) [{time.time() - t0:.0f}s]")
    print("結論: ReLU(導數恆1)+Dropout(子網集成)+增廣 -- 論文 top-5 15.3% vs 次名 26.2%")


if __name__ == "__main__":
    main()
