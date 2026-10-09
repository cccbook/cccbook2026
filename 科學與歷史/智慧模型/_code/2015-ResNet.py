# 2015 - ResNet 殘差網路 (He et al.)
# 對應本書: 2015-ResNet殘差網路.md
# 公式: H(x) = F(x) + x; ∂L/∂x_l = ∂L/∂x_{l+1}·(1 + ∂F/∂x) (「1+」直通梯度)
# 展示: 30 層 plain MLP vs 殘差 MLP 學 sin 曲線 -- 退化 (越深越差) vs 殘差解除
import torch
import torch.nn as nn


class Plain(nn.Module):
    def __init__(self, depth=30, w=32):
        super().__init__()
        self.layers = nn.ModuleList([nn.Sequential(nn.Linear(1 if i == 0 else w, w), nn.ReLU())
                                     for i in range(depth)])
        self.head = nn.Linear(w, 1)

    def forward(self, x):
        for l in self.layers:
            x = l(x)
        return self.head(x)


class ResNet(nn.Module):
    def __init__(self, blocks=15, w=32):
        super().__init__()
        self.inp = nn.Linear(1, w)
        self.blocks = nn.ModuleList([nn.Sequential(nn.Linear(w, w), nn.ReLU(),
                                                   nn.Linear(w, w)) for _ in range(blocks)])
        self.head = nn.Linear(w, 1)

    def forward(self, x):
        x = self.inp(x)
        for b in self.blocks:
            x = torch.relu(x + b(x))   # H(x) = F(x) + x: 恆等寫進架構
        return self.head(x)


def run(net, X, y, steps=1500):
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for _ in range(steps):
        opt.zero_grad()
        loss = ((net(X) - y) ** 2).mean()
        loss.backward()
        opt.step()
    with torch.no_grad():
        loss = ((net(X) - y) ** 2).mean().item()
    grads = [p.grad.norm().item() for p in net.parameters() if p.grad is not None]
    return loss, min(grads), max(grads)


def main():
    torch.manual_seed(0)
    X = torch.linspace(-3, 3, 400).view(-1, 1)
    y = torch.sin(X)
    for name, net in [("Plain-30層", Plain()), ("ResNet-15塊(≈30層)", ResNet())]:
        loss, gmin, gmax = run(net, X, y)
        print(f"{name}: 訓練MSE={loss:.4f} 梯度範數區間=[{gmin:.2e}, {gmax:.2e}]")
    print("結論: 同深度下 plain 退化 (MSE 高、底層梯度枯竭), 殘差以「1+」直通解除 -- "
          "ResNet-152 top-5 3.57% 壓過人類 5.1%")


if __name__ == "__main__":
    main()
