# 2022 - ChatGPT 與 RLHF: 獎勵模型 + PPO-lite (裁剪目標 + KL 剎車)
# 對應本書: 2022-ChatGPT與RLHF.md
# 公式: L(φ)=-E[log σ(r(x,y_w)-r(x,y_l))]; PPO clip 目標; 獎勵'=r-β·KL(π||π_SFT)
# 展示: 三臂「回覆老虎機」-- 人類偏好 A>B>C; 獎勵模型學排序, 策略被推向 A 但 KL 剎車留住多樣性
import torch
import torch.nn as nn
import torch.nn.functional as F


def main():
    torch.manual_seed(0)
    # 真人類偏好 (不可見): A(有幫助) > B(敷衍) > C(有害), Bradley-Terry 強度
    true_r = torch.tensor([2.0, 0.0, -2.0])
    # 階段1 SFT: 均勻策略 (模仿分佈, 什麼都說一點)
    pi = torch.ones(3) / 3
    # 階段2 獎勵模型: 從成對偏好 (y_w 勝 y_l) 學 r_φ
    rm = nn.Embedding(3, 1)
    opt_r = torch.optim.Adam(rm.parameters(), lr=0.1)
    pairs = [(0, 1)] * 30 + [(1, 2)] * 30 + [(0, 2)] * 30  # A勝B, B勝C, A勝C
    for _ in range(200):
        opt_r.zero_grad()
        w = torch.tensor([p[0] for p in pairs])
        l = torch.tensor([p[1] for p in pairs])
        loss = -F.logsigmoid(rm(w).squeeze(1) - rm(l).squeeze(1)).mean()
        loss.backward()
        opt_r.step()
    with torch.no_grad():
        r_hat = rm.weight.squeeze(1)
    print("獎勵模型學到的排序:", [round(float(v), 2) for v in r_hat],
          "(A>B>C -- 與真偏好同序, 只從成對比較學來)")

    # 階段3 PPO: 舊策略採樣 + importance ratio + clip + KL(π||π_SFT) 剎車
    theta = torch.zeros(3, requires_grad=True)
    opt_p = torch.optim.Adam([theta], lr=0.05)
    pi_sft = pi.clone()
    beta, eps = 0.5, 0.2
    with torch.no_grad():
        pi_old = F.softmax(theta, 0).clone()
    for step in range(60):
        if step % 10 == 0:  # 定期同步行為策略
            with torch.no_grad():
                pi_old = F.softmax(theta, 0).clone()
        opt_p.zero_grad()
        logp = F.log_softmax(theta, 0)
        pi_new = logp.exp()
        with torch.no_grad():
            acts = torch.multinomial(pi_old.expand(32, 3), 1).squeeze(1)
            base = float((pi_old * r_hat).sum())
            adv = r_hat[acts] - base                        # 優勢
            old_logp = pi_old.log()[acts]
        ratio = (logp[acts] - old_logp).exp()               # importance ratio
        clip_obj = torch.min(ratio * adv, ratio.clamp(1 - eps, 1 + eps) * adv).mean()
        kl = (pi_new * (logp - pi_sft.log())).sum()         # KL 剎車: 別飄太遠
        (-(clip_obj - beta * kl)).backward()
        opt_p.step()
    with torch.no_grad():
        final = F.softmax(theta, 0)
    print("RLHF 後策略:", [round(float(v), 2) for v in final],
          "(偏向 A 但不斷臂 -- KL 剎車留住 B/C, 對齊稅的縮影)")
    print("結論: SFT學格式、RM學品味、PPO學分寸 -- 三階段即 ChatGPT 的配方")


if __name__ == "__main__":
    main()
