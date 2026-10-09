# 2017 - Transformer 注意力機制 (Vaswani et al., Attention Is All You Need)
# 對應本書: 2017-Transformer注意力機制.md
# 公式: Attention(Q,K,V)=softmax(QKᵀ/√d_k)V; MultiHead=Concat(head_i)W^O
#       PE(pos,2i)=sin(pos/10000^{2i/d})
# 展示: (1) 縮放點積+多頭+位置編碼的前向與注意力權重
#       (2) toy 複述任務: 自注意力一步直連任意距離 (LSTM 的 O(T) 步 vs 注意力的 O(1))
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def sinusoid_pos(T, d):
    pe = torch.zeros(T, d)
    pos = torch.arange(T).float().unsqueeze(1)
    div = torch.exp(torch.arange(0, d, 2).float() * -(math.log(10000.0) / d))
    pe[:, 0::2] = torch.sin(pos * div)
    pe[:, 1::2] = torch.cos(pos * div)
    return pe  # 相對位置是線性變換 -- 天生知道序


class MultiHeadSelfAttn(nn.Module):
    def __init__(self, d=32, h=4):
        super().__init__()
        self.h, self.dk = h, d // h
        self.wq = nn.Linear(d, d, bias=False)
        self.wk = nn.Linear(d, d, bias=False)
        self.wv = nn.Linear(d, d, bias=False)
        self.wo = nn.Linear(d, d, bias=False)

    def forward(self, x, mask=None):
        B, T, D = x.shape
        Q = self.wq(x).view(B, T, self.h, self.dk).transpose(1, 2)
        K = self.wk(x).view(B, T, self.h, self.dk).transpose(1, 2)
        V = self.wv(x).view(B, T, self.h, self.dk).transpose(1, 2)
        s = Q @ K.transpose(-2, -1) / math.sqrt(self.dk)  # √d_k: 方差歸一防飽和
        if mask is not None:
            s = s.masked_fill(mask, float("-inf"))
        a = F.softmax(s, dim=-1)                          # 任意兩位置一步直連
        return (self.wo((a @ V).transpose(1, 2).reshape(B, T, D)), a)


def main():
    torch.manual_seed(0)
    B, T, D = 2, 8, 32
    x = torch.randn(B, T, D) + sinusoid_pos(T, D)          # 內容 + 位置
    mha = MultiHeadSelfAttn(D, 4)
    out, a = mha(x)
    print(f"輸入 {tuple(x.shape)} -> 輸出 {tuple(out.shape)} "
          f"(置換等變+位置編碼=序列模型; 注意力權重形狀 {tuple(a.shape)} [B,頭,T,T])")
    print("第0頭第0行注意力 (第0個token看誰):", [round(float(v), 2) for v in a[0, 0, 0]])
    # toy 複述: 首符號經 7 步雜訊後複述 -- 注意力一步直連, 路徑 O(1)
    N = 600
    X = torch.randint(2, 6, (N, T))
    X[:, 0] = torch.randint(0, 2, (N,))
    y = X[:, 0].long()
    enc = nn.Sequential(nn.Embedding(6, D), )
    clf = nn.Linear(D, 2)
    opt = torch.optim.Adam(list(mha.parameters()) + list(enc.parameters())
                           + list(clf.parameters()), lr=5e-3)
    E = enc[0]
    for ep in range(60):
        opt.zero_grad()
        h = E(X) + sinusoid_pos(T, D)
        o, _ = mha(h)
        loss = F.cross_entropy(clf(o[:, -1]), y)          # 只讀末位: 須從首位取資訊
        loss.backward()
        opt.step()
    with torch.no_grad():
        h = E(X) + sinusoid_pos(T, D)
        o, a2 = mha(h)
        acc = (clf(o[:, -1]).argmax(1) == y).float().mean().item()
        focus = a2[:, :, -1, 0].mean().item()             # 末位對首位的平均注意力
    print(f"距離7步的複述準確率={acc:.2f} (LSTM 需穿越7個閘門, 注意力一步直連)")
    print(f"末位token對首位token平均注意力={focus:.2f} (模型學會回頭看 -- Bahdanau 的泛化)")


if __name__ == "__main__":
    main()
