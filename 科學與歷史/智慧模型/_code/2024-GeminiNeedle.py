# 2024 - Gemini 原生多模態: 一切皆 token + 百萬級上下文的大海撈针
# 對應本書: 2024-Gemini原生多模態.md
# 公式: P(下一token | 文字,影像,音訊,視訊全離散化); L = Σ λ_m L_m
# 展示: 長序列大海撈针 -- 注意力從 2048 個位置撈出唯一鑰匙 (原生 vs 外掛的縮影)
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def main():
    torch.manual_seed(0)
    D, H = 32, 4
    wq = nn.Linear(D, D, bias=False)
    wk = nn.Linear(D, D, bias=False)
    wv = nn.Linear(D, D, bias=False)
    opt = torch.optim.Adam(list(wq.parameters()) + list(wk.parameters())
                           + list(wv.parameters()), lr=1e-2)
    # 世界: 2048 個「多模態 tokens」(隨機向量), 其中 1 個是鑰匙 (與 query 同分布)
    for ep in range(250):
        opt.zero_grad()
        B, L = 8, 2048
        mem = torch.randn(B, L, D)               # 大海 (百萬級上下文的縮影)
        key = torch.randn(B, 1, D)
        pos = torch.randint(0, L, (B,))
        for b in range(B):
            mem[b, pos[b]] = key[b, 0] + torch.randn(D) * 0.05  # 藏针
        q = key + torch.randn(B, 1, D) * 0.05    # 查詢 (另一模態的同一語義)
        s = (wq(q) @ wk(mem).transpose(-2, -1)) / math.sqrt(D // H)
        a = F.softmax(s, -1)
        out = a @ wv(mem)
        loss = ((out - wv(key)) ** 2).mean()     # 撈出的值應等於鑰匙的值
        loss.backward()
        opt.step()
    with torch.no_grad():
        B, L = 4, 2048
        mem = torch.randn(B, L, D)
        key = torch.randn(B, 1, D)
        pos = torch.randint(0, L, (B,))
        for b in range(B):
            mem[b, pos[b]] = key[b, 0] + torch.randn(D) * 0.1
        q = key + torch.randn(B, 1, D) * 0.1
        s = (wq(q) @ wk(mem).transpose(-2, -1)) / math.sqrt(D // H)
        a = F.softmax(s, -1)
        hit = sum(int(a[b, 0].argmax()) == int(pos[b]) for b in range(B))
        mass = sum(float(a[b, 0, pos[b]]) for b in range(B)) / B
    print(f"2048 選 1 撈针命中={hit}/{B} 針上注意力質量={mass:.2f} (隨機≈{1 / L:.4f})")
    print("結論: 原生多模態 = 同一注意力撈所有模態 -- 外掛管線做不到跨模態直連")


if __name__ == "__main__":
    main()
