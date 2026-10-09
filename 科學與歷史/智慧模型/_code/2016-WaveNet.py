# 2016 - WaveNet 語音合成: 擴張因果卷積的自回歸
# 對應本書: 2016-WaveNet語音合成.md
# 公式: p(x)=Π p(x_t|x_<t); 門控 z=tanh(W_f x)⊙σ(W_g x); 感受野 R=Σ dilation+1 (指數爆炸)
# 展示: 擴張卷積堆疊預測正弦波下一點 (μ-law 量化 256 類的縮影), 感受野計算 + 損失下降
import torch
import torch.nn as nn
import torch.nn.functional as F


class WaveNetMini(nn.Module):
    def __init__(self, layers=6, channels=32, n_bins=64):
        super().__init__()
        self.emb = nn.Embedding(n_bins, channels)
        self.dilations = [2 ** i for i in range(layers)]  # 1,2,4,...,32
        self.f = nn.ModuleList([nn.Conv1d(channels, channels, 2, dilation=d)
                                for d in self.dilations])
        self.g = nn.ModuleList([nn.Conv1d(channels, channels, 2, dilation=d)
                                for d in self.dilations])
        self.rf = sum(self.dilations) + 1                  # 感受野: 指數爆炸
        self.out = nn.Linear(channels, n_bins)

    def forward(self, q):
        x = self.emb(q).transpose(1, 2)                    # 因果: 左pad, 只看過去
        for f, g, d in zip(self.f, self.g, self.dilations):
            h = F.pad(x, (d, 0))                           # 左填充守住因果性
            z = torch.tanh(f(h)) * torch.sigmoid(g(h))     # 門控 (LSTM 的遺產)
            x = x + z[:, :, -x.size(2):]                   # 殘差 (2015 的遺產)
        return self.out(x.transpose(1, 2))


def main():
    torch.manual_seed(0)
    T, NB = 256, 64
    t = torch.linspace(0, 8 * 3.1416, 4000)
    wave = torch.sin(t) + 0.3 * torch.sin(3 * t)           # 雙頻正弦 (聲波縮影)
    q = ((wave + 1.3) / 2.6 * (NB - 1)).long().clamp(0, NB - 1)  # 量化 (μ-law 精神)
    net = WaveNetMini()
    print(f"6層擴張卷積感受野 R={net.rf} 點 (每加一層翻倍 -- RNN 的 O(T) 步變成 O(1) 並行)")
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(25):
        opt.zero_grad()
        idx = torch.randint(0, len(q) - T - 1, (32,))
        xb = torch.stack([q[i:i + T] for i in idx])
        yb = torch.stack([q[i + 1:i + T + 1] for i in idx])
        loss = F.cross_entropy(net(xb).reshape(-1, NB), yb.reshape(-1))
        loss.backward()
        opt.step()
    print(f"25輪後下一點預測 loss={loss.item():.3f} (隨機猜={-__import__('math').log(1 / NB):.3f})")
    net.eval()
    with torch.no_grad():
        seed = q[:T].unsqueeze(0)
        gen = seed[0].tolist()
        cur = seed
        for _ in range(60):                                # 自回歸生成 60 點
            nxt = net(cur)[:, -1].argmax(-1)
            gen.append(int(nxt))
            cur = torch.cat([cur[:, 1:], nxt.unsqueeze(0)], 1)
    err = (torch.tensor(gen[T:]).float() - q[T:T + 60].float()).abs().mean().item()
    print(f"自回歸續寫60點平均量化誤差={err:.2f} 格 (波形跟上 -- 生成即逐點採樣)")
    print("結論: 捨棄 RNN、用卷積並行生成 -- 條件化再加文本即 TTS, 換成像素即 PixelCNN")


if __name__ == "__main__":
    main()
