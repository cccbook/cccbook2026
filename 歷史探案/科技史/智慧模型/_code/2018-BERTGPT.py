# 2018 - BERT 與 GPT 預訓練典範: 自回歸 LM + 掩碼 LM, 同一具 Transformer
# 對應本書: 2018-BERT與GPT預訓練典範.md
# 公式: GPT: L=Σ log p(x_i|x_<i}); BERT: L=Σ_{i∈M} log p(x_i|x_{\M})
# 展示: 字元級 toy 語料上, 因果模型學接龍、掩碼模型學完形, [CLS] 句向量可分兩類
import torch
import torch.nn as nn
import torch.nn.functional as F


class MiniTransformer(nn.Module):
    def __init__(self, V, d=32, h=4):
        super().__init__()
        self.emb = nn.Embedding(V, d)
        self.pos = nn.Embedding(32, d)
        self.attn = nn.MultiheadAttention(d, h, batch_first=True)
        self.ffn = nn.Sequential(nn.Linear(d, 64), nn.ReLU(), nn.Linear(64, d))
        self.n1 = nn.LayerNorm(d)
        self.n2 = nn.LayerNorm(d)
        self.head = nn.Linear(d, V)

    def forward(self, ids, causal):
        T = ids.size(1)
        x = self.emb(ids) + self.pos(torch.arange(T))
        m = torch.triu(torch.ones(T, T, dtype=torch.bool), 1) if causal else None
        a, _ = self.attn(x, x, x, attn_mask=m, need_weights=False)
        x = self.n1(x + a)          # Add & Norm (殘差配方, 2015 的遺產)
        x = self.n2(x + self.ffn(x))
        return self.head(x)


def main():
    torch.manual_seed(0)
    sents = ["cats eat fish", "dogs eat meat", "birds eat seeds",
             "cats drink milk", "dogs drink water", "birds sing songs"]
    vocab = ["<m>", "[CLS]"] + sorted({c for s in sents for c in s})
    ci = {c: i for i, c in enumerate(vocab)}
    V = len(vocab)
    data = [[ci["[CLS]"]] + [ci[c] for c in s] for s in sents]
    T = max(map(len, data))
    X = torch.tensor([r + [ci["<m>"]] * (T - len(r)) for r in data])
    net = MiniTransformer(V)
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(300):
        opt.zero_grad()
        # GPT 分支: 因果掩碼, 預測下一字元
        logits = net(X, causal=True)
        lgpt = F.cross_entropy(logits[:, :-1].reshape(-1, V), X[:, 1:].reshape(-1))
        # BERT 分支: 隨機掩 2 位, 雙向預測
        mask = torch.rand_like(X.float()) < 0.15
        mask[:, 0] = False
        logits_b = net(torch.where(mask, ci["<m>"], X), causal=False)
        lbert = F.cross_entropy(logits_b[mask], X[mask]) if mask.any() else 0
        (lgpt + lbert).backward()
        opt.step()
    print(f"GPT自回歸損失={lgpt.item():.3f} BERT掩碼損失={float(lbert):.3f} (同一具Transformer, 兩種目標)")
    net.eval()
    with torch.no_grad():
        # 接龍: "cats " 之後最可能的三個字元
        seed = torch.tensor([[ci["[CLS]"], ci["c"], ci["a"], ci["t"], ci["s"], ci[" "]]])
        nxt = F.softmax(net(seed, causal=True)[0, -1], -1).topk(3)
        print("接龍 'cats '->", [(vocab[i], round(float(p), 2)) for p, i in zip(nxt.values, nxt.indices)])
        # 完形: "cats eat ____" (掩一位)
        q = torch.tensor([[ci["[CLS]"], ci["c"], ci["a"], ci["t"], ci["s"], ci[" "],
                           ci["e"], ci["a"], ci["t"], ci[" "], ci["<m>"]]])
        fill = net(q, causal=False)[0, -1].argmax().item()
        print(f"完形 'cats eat _' 填: '{vocab[fill]}' (雙向上下文 -- BERT 的看家本領)")
        # [CLS] 句向量: 貓狗(吃喝) vs 鳥(唱歌) 應分開 (整批雙向走完整網路)
        e = net.emb(X) + net.pos(torch.arange(X.size(1)))
        a, _ = net.attn(e, e, e, need_weights=False)
        h = net.n1(e + a)
        H = (net.n2(h + net.ffn(h)))[:, 0]
        d_bird = (H[5] - H[:2].mean(0)).norm().item()
        d_pet = (H[0] - H[1]).norm().item()
        print(f"[CLS]距離: 鳥句-貓狗句={d_bird:.2f} vs 貓句-狗句={d_pet:.2f} "
              f"({'語義分群' if d_bird > d_pet else '未分群'})")


if __name__ == "__main__":
    main()
