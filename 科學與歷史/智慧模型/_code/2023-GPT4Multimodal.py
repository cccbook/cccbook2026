# 2023 - GPT-4 多模態: 影像 tokens + 文字 tokens 進同一具 Transformer
# 對應本書: 2023-GPT-4多模態.md
# 公式: 輸入序列 = [v_1..v_m, t_1..t_n] -> Transformer -> 文字輸出
# 展示: 合成圖文問答上, 多模態 > 純文字 (影像補上文字沒有的資訊)
import torch
import torch.nn as nn
import torch.nn.functional as F


class MultimodalMini(nn.Module):
    def __init__(self, d=32):
        super().__init__()
        self.vproj = nn.Linear(8, d)     # 影像 patch -> token (ViT 的遺產)
        self.tproj = nn.Embedding(12, d)  # 文字 token
        layer = nn.TransformerEncoderLayer(d, 4, d * 2, batch_first=True)
        self.tr = nn.TransformerEncoder(layer, 2)
        self.head = nn.Linear(d, 2)      # 是非問答

    def forward(self, v, t, use_image=True):
        tv = self.vproj(v) if use_image else torch.zeros_like(self.vproj(v))
        z = torch.cat([tv, self.tproj(t)], 1)
        return self.head(self.tr(z)[:, -1])


def main():
    torch.manual_seed(0)
    N = 800
    # 世界: 影像含圓環與否; 問題問「有圓環嗎」-- 文字本身無答案, 必須看圖
    V = torch.randn(N, 4, 8)
    has = torch.randint(0, 2, (N,))
    V[has == 1, :, 0] += 3.0             # 有圓環: 第0維打亮 (視覺事實)
    T = torch.randint(0, 12, (N, 3))     # 問題 token (與答案無關的噪聲)
    y = has.long()
    net = MultimodalMini()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    ntr = 600  # 留 200 當測試 (文字路會背訓練集 -- 泛化看測試集)
    for ep in range(60):
        opt.zero_grad()
        loss = (F.cross_entropy(net(V[:ntr], T[:ntr], True), y[:ntr])
                + F.cross_entropy(net(V[:ntr], T[:ntr], False), y[:ntr])) / 2
        loss.backward()
        opt.step()
    with torch.no_grad():
        acc_mm = (net(V[ntr:], T[ntr:], True).argmax(1) == y[ntr:]).float().mean().item()
        acc_tx = (net(V[ntr:], T[ntr:], False).argmax(1) == y[ntr:]).float().mean().item()
    print(f"多模態準確率={acc_mm:.2f} 純文字準確率={acc_tx:.2f} (文字無答案時只能猜)")
    print("結論: 影像即 token -- 同一序列、同一注意力; MMLU 86.4% 的起點是『看得見』")


if __name__ == "__main__":
    main()
