# 2025 - Genie3 互動世界模型: 動作條件的下一幀預測 (離散 token 版, Genie 路線)
# 對應本書: 2025-Genie3互動世界模型.md
# 公式: P(x_{t+1} | x_t, ..., a_t, text); 世界模型 = 下一幀預測 + 動作條件 + 記憶
# 展示: 8x8 格亮點走位 token 化 (64 詞) + 動作條件 -> 64 類分類預測下一 token;
#       有動作 vs 無動作 (平均動作) 的 rollout 位置跟隨率 -- 可控即世界
import torch
import torch.nn as nn
import torch.nn.functional as F

ACTS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 左右上下


def build_world(N=600, T=12, seed=0):
    torch.manual_seed(seed)
    S = torch.zeros(N, T + 1, 2, dtype=torch.long)
    A = torch.randint(0, 4, (N, T))
    S[:, 0] = torch.randint(0, 8, (N, 2))
    for t in range(T):
        S[:, t + 1, 0] = (S[:, t, 0] + torch.tensor([a[0] for a in ACTS])[A[:, t]]).clamp(0, 7)
        S[:, t + 1, 1] = (S[:, t, 1] + torch.tensor([a[1] for a in ACTS])[A[:, t]]).clamp(0, 7)
    tok = S[:, :, 0] * 8 + S[:, :, 1]  # 幀 -> token (VQ 的精神縮影: 64 詞)
    return tok, A


class World(nn.Module):  # 世界模型: 下一 token = f(當前 token, 動作)
    def __init__(self):
        super().__init__()
        self.pos = nn.Embedding(64, 16)
        self.act = nn.Embedding(4, 8)
        self.m = nn.Sequential(nn.Linear(24, 64), nn.ReLU(), nn.Linear(64, 64))

    def forward(self, tok, a):
        return self.m(torch.cat([self.pos(tok), self.act(a)], 1))


def main():
    torch.manual_seed(0)
    N, T = 600, 12
    tok, A = build_world(N, T)
    net = World()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(200):
        idx = torch.randint(0, N, (256,))
        t = torch.randint(0, T, (256,))
        opt.zero_grad()
        loss = F.cross_entropy(net(tok[idx, t], A[idx, t]), tok[idx, t + 1])
        loss.backward()
        opt.step()
    with torch.no_grad():
        idx = torch.arange(300)
        t = torch.randint(0, T, (300,))
        one = (net(tok[idx, t], A[idx, t]).argmax(1) == tok[idx, t + 1]).float().mean().item()
    print(f"單步下一 token 準確率={one:.2f} (64 選 1, 隨機≈0.02 -- 動作條件學會)")
    # rollout: 從真實首 token 出發, 同一動作序列推 12 步; 對手: 無動作 (平均嵌入)
    with torch.no_grad():
        M = 100
        cur = tok[:M, 0].clone()
        hit_c = hit_u = 0
        mean_a = net.act.weight.mean(0).expand(M, -1)  # 無動作基線: 平均動作嵌入
        for t in range(T):
            logits_c = net.m(torch.cat([net.pos(cur), net.act(A[:M, t])], 1))
            logits_u = net.m(torch.cat([net.pos(cur), mean_a], 1))
            hit_c += (logits_c.argmax(1) == tok[:M, t + 1]).sum().item()
            hit_u += (logits_u.argmax(1) == tok[:M, t + 1]).sum().item()
            cur = logits_c.argmax(1)  # 有條件 rollout (記憶一致性: 上一步輸出即下一步輸入)
    print(f"12步 rollout 位置跟隨率: 有動作={hit_c / (M * T):.2f} 無動作={hit_u / (M * T):.2f}")
    print("結論: 下一幀+動作+記憶 = 可互動的世界; 無動作即普通影片模型 (只能猜最可能的走位)")


if __name__ == "__main__":
    main()
