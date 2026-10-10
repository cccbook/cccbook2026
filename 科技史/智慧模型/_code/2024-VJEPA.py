# 2024 - V-JEPA 世界模型: 預測表徵, 不生成像素 (JEPA 在影片上)
# 對應本書: 2024-VJEPA世界模型.md
# 公式: L = ||enc_y(y) - pred(enc_x(x))||²; θ_y <- m·θ_y + (1-m)·θ_x (EMA, 防坍縮)
# 展示: 遮住後半影片, 用前半潛表徵預測後半潛表徵 -- 方差不塌 (無坍縮) 即學到動態
import torch
import torch.nn as nn
import torch.nn.functional as F


def main():
    torch.manual_seed(0)
    T, N = 8, 400
    # 影片: 1D 亮點等速移動 (位置即全部物理)
    V = torch.zeros(N, T, 16)
    for i in range(N):
        x0 = torch.randint(0, 10, (1,)).item()
        v = 1 if i % 2 == 0 else -1
        for t in range(T):
            V[i, t, min(max(x0 + v * t, 0), 15)] = 1.0
    V = V + torch.randn_like(V) * 0.03
    D = 32
    enc_x = nn.Sequential(nn.Linear(16, 64), nn.ReLU(), nn.Linear(64, D))  # 上下文編碼器
    enc_y = nn.Sequential(nn.Linear(16, 64), nn.ReLU(), nn.Linear(64, D))  # 目標編碼器 (EMA)
    enc_y.load_state_dict(enc_x.state_dict())
    pred = nn.Sequential(nn.Linear(D, 64), nn.ReLU(), nn.Linear(64, D))    # 預測器
    opt = torch.optim.Adam(list(enc_x.parameters()) + list(pred.parameters()), lr=5e-3)
    m = 0.996
    for ep in range(200):
        opt.zero_grad()
        hx = enc_x(V[:, :4].mean(1))   # 前半的時間平均 -> 上下文表徵
        with torch.no_grad():
            hy = enc_y(V[:, 4:].mean(1))  # 後半的時間平均 -> 目標表徵
        loss = ((pred(hx) - hy) ** 2).mean() + 0.5 * max(0.0, 1.0 - pred(hx).std())  # 預測+方差防塌
        loss.backward()
        opt.step()
        with torch.no_grad():  # 目標編碼器慢動量跟隨
            for py, px in zip(enc_y.parameters(), enc_x.parameters()):
                py.mul_(m).add_(px, alpha=1 - m)
    with torch.no_grad():
        hx = enc_x(V[:, :4].mean(1))
        hy = enc_y(V[:, 4:].mean(1))
        err = ((pred(hx) - hy) ** 2).mean().item()
        var = pred(hx).std().item()
    print(f"掩碼潛預測 MSE={err:.4f} 表徵標準差={var:.2f} ({'無坍縮' if var > 0.3 else '坍縮警告'})")
    print("結論: Sora 生成像素、V-JEPA 預測表徵 -- 不重建即不浪費容量在葉紋上; EMA 是防塌的錨")


if __name__ == "__main__":
    main()
