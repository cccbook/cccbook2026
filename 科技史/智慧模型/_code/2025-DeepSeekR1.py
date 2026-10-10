# 2025 - DeepSeek-R1: GRPO (組內歸一優勢, 免 critic) + MoE 參數算術
# 對應本書: 2025-DeepSeek-R1.md
# 公式: Â_i = (r_i - mean(r)) / std(r); y = Σ_{top-k} g_i E_i (256專家取8)
# 展示: 四臂「推理老虎機」上 GRPO 從零學出最優臂 (R1-Zero 縮影: 純 RL 湧現)
import torch
import torch.nn as nn
import torch.nn.functional as F


def main():
    torch.manual_seed(0)
    true_p = torch.tensor([0.2, 0.35, 0.5, 0.9])  # 四臂真成功率 (不可見的驗證器)
    theta = torch.zeros(4, requires_grad=True)    # 策略 (R1-Zero: 從零開始, 無 SFT)
    opt = torch.optim.Adam([theta], lr=0.1)
    eps, G = 0.2, 16                              # clip 半徑, 每組樣本數
    hist = []
    for step in range(120):
        logits = theta.detach()
        with torch.no_grad():
            acts = torch.multinomial(F.softmax(logits, 0).expand(G, 4), 1).squeeze(1)
            r = (torch.rand(G) < true_p[acts]).float()  # 0/1 驗證獎勵 (結果監督)
            adv = (r - r.mean()) / (r.std() + 1e-6)     # GRPO: 組內歸一, 免 critic
            old_logp = F.log_softmax(logits, 0)[acts]
        opt.zero_grad()
        ratio = (F.log_softmax(theta, 0)[acts] - old_logp).exp()
        loss = -torch.min(ratio * adv, ratio.clamp(1 - eps, 1 + eps) * adv).mean()
        loss.backward()
        opt.step()
        hist.append(float(r.mean()))
    with torch.no_grad():
        final = F.softmax(theta, 0)
    print(f"GRPO 120輪: 獎勵 {hist[0]:.2f} -> {hist[-1]:.2f} "
          f"(純 RL, 無示範 -- R1-Zero 的『啊哈』是統計量的形狀)")
    print("終局策略:", [round(float(v), 2) for v in final], "(最優臂 0.9 被找出)")
    print("MoE 算術: 256專家取8 -> 每次只算 8/256 參數 (省 32x); 蒸餾把果實分給小模型")


if __name__ == "__main__":
    main()
