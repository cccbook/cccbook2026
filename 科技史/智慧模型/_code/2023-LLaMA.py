# 2023 - LLaMA 開源大模型: RMSNorm + SwiGLU + RoPE + GQA 的現代零件
# 對應本書: 2023-LLaMA開源大模型.md
# 公式: <R_m q, R_n k> = <q, R_{n-m} k> (相對位置內建); GQA: H_q=H, H_kv=H/g
# 展示: LLaMA block 前向 + RoPE 相對性驗證 + SwiGLU/RMSNorm/GQA 形狀
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def rmsnorm(x, w, eps=1e-6):
    return x / (x.pow(2).mean(-1, keepdim=True) + eps).sqrt() * w  # 無均值漂移, 比 LayerNorm 便宜


def swiglu(x, W, V):
    return F.silu(x @ W) * (x @ V)  # 門控前饋, 參數量產出比勝 ReLU-MLP


def rope(x, pos):
    d = x.size(-1)  # 旋轉一半維度對; 形狀補成 (1,T,1,d) 以廣播 (B,T,H,d)
    ang = pos.float().unsqueeze(-1) * torch.exp(
        torch.arange(0, d, 2).float() * -(math.log(10000.0) / d))
    c = ang.cos().repeat_interleave(2, -1).view(1, -1, 1, d)
    s = ang.sin().repeat_interleave(2, -1).view(1, -1, 1, d)
    x2 = torch.stack([-x[..., 1::2], x[..., 0::2]], -1).reshape_as(x)
    return x * c + x2 * s


class LLaMABlock(nn.Module):  # GQA: q 4頭, kv 2組 (g=2)
    def __init__(self, d=32, hq=4, hkv=2):
        super().__init__()
        self.hq, self.hkv, self.dk = hq, hkv, d // hq
        self.wq = nn.Linear(d, d, bias=False)
        self.wk = nn.Linear(d, hkv * self.dk, bias=False)
        self.wv = nn.Linear(d, hkv * self.dk, bias=False)
        self.wo = nn.Linear(d, d, bias=False)
        self.w1 = nn.Linear(d, 64, bias=False)
        self.w3 = nn.Linear(d, 64, bias=False)
        self.w2 = nn.Linear(64, d, bias=False)
        self.n1 = nn.Parameter(torch.ones(d))
        self.n2 = nn.Parameter(torch.ones(d))

    def forward(self, x):
        B, T, D = x.shape
        h = rmsnorm(x, self.n1)
        Q = self.wq(h).view(B, T, self.hq, self.dk)
        K = self.wk(h).view(B, T, self.hkv, self.dk)
        V = self.wv(h).view(B, T, self.hkv, self.dk)
        pos = torch.arange(T)
        Q, K = rope(Q, pos), rope(K, pos)          # RoPE: 位置轉進 Q/K
        K = K.repeat_interleave(self.hq // self.hkv, 2)  # GQA: kv 頭複用
        V = V.repeat_interleave(self.hq // self.hkv, 2)
        a = F.softmax(Q.transpose(1, 2) @ K.transpose(1, 2).transpose(-2, -1)
                      / math.sqrt(self.dk), -1)
        x = x + self.wo((a @ V.transpose(1, 2)).transpose(1, 2).reshape(B, T, D))
        h2 = rmsnorm(x, self.n2)
        return x + self.w2(swiglu(h2, self.w1.weight.T, self.w3.weight.T))


def main():
    torch.manual_seed(0)
    x = torch.randn(2, 8, 32)
    blk = LLaMABlock()
    y = blk(x)
    print(f"LLaMA block: {tuple(x.shape)} -> {tuple(y.shape)} "
          f"(RMSNorm+SwiGLU+RoPE+GQA 全在, 無 bias -- 零件現代化)")
    # RoPE 相對性: 內積只與距離 n-m 有關 (平移一格不變)
    torch.manual_seed(1)
    q = torch.randn(4, 8)
    k = torch.randn(4, 8)
    s1 = (rope(q[:2], torch.tensor([3, 5])) * rope(k[:2], torch.tensor([3, 5]))).sum(-1)
    s2 = (rope(q[:2], torch.tensor([7, 9])) * rope(k[:2], torch.tensor([7, 9]))).sum(-1)
    print(f"RoPE 平移不變性: 距離皆為2的兩對內積差={float((s1 - s2).abs().max()):.2e} (≈0 -- 相對位置內建)")
    n_params = sum(p.numel() for p in blk.parameters())
    print(f"單 block 參數 {n_params}; GQA kv頭減半≈省 1/4 注意力參數 (推論成本預留)")
    print("結論: 零件現代化 + 乾淨資料 + Chinchilla 配比 -- LLaMA-65B ≈ Chinchilla-70B > GPT-3-175B")


if __name__ == "__main__":
    main()
