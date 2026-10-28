# 2024 - o1 推理模型: 測試時計算 (best-of-N + 驗證器), 準確率隨 k 爬升
# 對應本書: 2024-o1推理模型.md
# 公式: accuracy ∝ compute at inference; max_θ E[r(τ)], τ=(s_1..s_T) (想即動作)
# 展示: 迷宮尋路 -- 單次直覺 vs 多次採樣+驗證器選最優, 推理算力換準確率 (草莓藏在第二步)
import numpy as np

MAZE = np.array([
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
])
START, GOAL = (0, 0), (6, 6)
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
SIZE = 7


def rollout(policy_bias, rng):
    """隨機策略走迷宮 (直覺): bias 越大越往目標偏, 但仍會撞牆繞路 (限50步)."""
    p, path = list(START), [tuple(START)]
    for _ in range(50):
        if tuple(p) == GOAL:
            break
        moves = []
        for d in DIRS:
            q = (p[0] + d[0], p[1] + d[1])
            if 0 <= q[0] < SIZE and 0 <= q[1] < SIZE and MAZE[q] == 0:
                dist = abs(q[0] - GOAL[0]) + abs(q[1] - GOAL[1])
                moves.append((policy_bias ** -dist if policy_bias > 0 else 1.0, q))
        w = np.array([m[0] for m in moves])
        p = list(moves[rng.choice(len(moves), p=w / w.sum())][1])
        path.append(tuple(p))
    ok = tuple(p) == GOAL
    return ok, len(path) if ok else 999  # 驗證器: 到終點否 + 步數 (結果監督)


def best_of_n(n, seed=0):
    rng = np.random.default_rng(seed)
    cands = [rollout(1.2, rng) for _ in range(n)]  # 弱直覺: 單次成功率僅約三成
    oks = [c for c in cands if c[0]]
    return (True, min(c[1] for c in oks)) if oks else (False, 999)


def main():
    print("迷宮 best-of-N (測試時算力換準確率):")
    for n in [1, 4, 16, 64]:
        ok, steps, tot = 0, [], 200
        for i in range(tot):
            s, st = best_of_n(n, seed=i)
            ok += s
            steps.append(st)
        steps = [s for s in steps if s < 999]
        print(f"  N={n:3d}: 成功率={ok / tot:.2f} 平均步數={np.mean(steps):.1f} "
              f"(算力×{n} -- 推理革命的形狀)")
    print("結論: 不加大模型、只加思考次數+驗證器, 成功率照 log 律爬 -- o1 的第二條曲線")


if __name__ == "__main__":
    main()
