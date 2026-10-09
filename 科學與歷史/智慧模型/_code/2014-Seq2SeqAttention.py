# 2014 - Seq2Seq 與 Bahdanau 注意力
# 對應本書: 2014-Seq2Seq與注意力.md
# 公式: e_ti = vᵀtanh(W s_{t-1} + U h_i); α=sotfmax(e); c_t = Σ α_ti h_i
# 展示: 數字串反轉任務 (源句倒序輸入, Sutskever 技巧), 注意力矩陣呈現對角對齊
import torch
import torch.nn as nn
import torch.nn.functional as F


class AttnSeq2Seq(nn.Module):
    def __init__(self, V=10, E=16, H=32):
        super().__init__()
        self.emb = nn.Embedding(V, E)
        self.enc = nn.GRU(E, H, batch_first=True)
        self.dec = nn.GRUCell(E + H, H)
        self.Wa = nn.Linear(H, H, bias=False)   # U_a h_i
        self.Ua = nn.Linear(H, H, bias=False)   # W_a s_{t-1}
        self.va = nn.Linear(H, 1, bias=False)   # v_a
        self.out = nn.Linear(H * 2, V)

    def forward(self, src, tgt):
        eh, h = self.enc(self.emb(src))          # eh: 全部編碼狀態 (回頭看的對象)
        s = h.squeeze(0)
        go = torch.zeros(len(src), 1, dtype=torch.long)
        prev = self.emb(go).squeeze(1)
        loss, alphas = 0, []
        for t in range(tgt.size(1)):
            e = self.va(torch.tanh(self.Ua(s).unsqueeze(1) + self.Wa(eh))).squeeze(-1)
            a = F.softmax(e, dim=1)              # α_{t,i}: 此步看哪裡
            alphas.append(a.detach())
            c = (a.unsqueeze(-1) * eh).sum(1)    # c_t: 動態上下文 (瓶頸解除)
            s = self.dec(torch.cat([prev, c], 1), s)
            logits = self.out(torch.cat([s, c], 1))
            loss = loss + F.cross_entropy(logits, tgt[:, t])
            prev = self.emb(tgt[:, t])
        return loss / tgt.size(1), torch.stack(alphas, 1)


def main():
    torch.manual_seed(0)
    T, N = 6, 2000
    src = torch.randint(0, 10, (N, T))
    tgt = src.flip(1)                            # 目標: 反轉 (倒序的極端版)
    net = AttnSeq2Seq()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(40):
        opt.zero_grad()
        loss, _ = net(src, tgt)
        loss.backward()
        opt.step()
    with torch.no_grad():
        loss, alphas = net(src[:5], tgt[:5])
        pred = []
        # 貪婪解碼
        eh, h = net.enc(net.emb(src[:5]))
        s = h.squeeze(0)
        prev = net.emb(torch.zeros(5, 1, dtype=torch.long)).squeeze(1)
        for _ in range(T):
            e = net.va(torch.tanh(net.Ua(s).unsqueeze(1) + net.Wa(eh))).squeeze(-1)
            a = F.softmax(e, dim=1)
            c = (a.unsqueeze(-1) * eh).sum(1)
            s = net.dec(torch.cat([prev, c], 1), s)
            tok = net.out(torch.cat([s, c], 1)).argmax(1)
            pred.append(tok)
            prev = net.emb(tok)
        pred = torch.stack(pred, 1)
        acc = (pred == tgt[:5]).float().mean().item()
    print(f"反轉任務準確率(抽5句逐token)={acc:.2f}")
    print("源句:", src[0].tolist(), "目標:", tgt[0].tolist(), "預測:", pred[0].tolist())
    print("注意力矩陣 α(行=解碼步, 列=源位置, 反對角線即正確對齊):")
    for row in alphas[0]:
        print("  " + " ".join(f"{v:.2f}" for v in row))


if __name__ == "__main__":
    main()
