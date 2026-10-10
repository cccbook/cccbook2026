# -*- coding: utf-8 -*-
"""1970 Game of Life 滑翔機 (glider)：Conway 1970
對應 wiki：Conway's Game of Life，滑翔機每 4 步平移一格 (1,1) 且活細胞恆為 5。
10x10 零邊界，跑 4 步做座標比對驗證。只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

N = 10
STEPS = 4
# 經典 glider（相對座標），放在 offset 處以避開邊界
PATTERN = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
OFF = (2, 2)


def make_grid():
    g = np.zeros((N, N), dtype=int)
    for dr, dc in PATTERN:
        g[OFF[0] + dr, OFF[1] + dc] = 1
    return g


def step(g):
    # 零邊界鄰居計數（切片法，不用 wrap）
    nb = np.zeros_like(g)
    nb[1:, 1:] += g[:-1, :-1]
    nb[1:, :] += g[:-1, :]
    nb[1:, :-1] += g[:-1, 1:]
    nb[:, 1:] += g[:, :-1]
    nb[:, :-1] += g[:, 1:]
    nb[:-1, 1:] += g[1:, :-1]
    nb[:-1, :] += g[1:, :]
    nb[:-1, :-1] += g[1:, 1:]
    nxt = ((nb == 3) | ((g == 1) & (nb == 2))).astype(int)
    return nxt


def coords(g):
    return sorted(map(tuple, np.argwhere(g == 1).tolist()))


g = make_grid()
init_c = coords(g)
print(f"init live={len(init_c)} coords={init_c}")
counts = [len(init_c)]
for s in range(1, STEPS + 1):
    g = step(g)
    c = coords(g)
    counts.append(len(c))
    print(f"step {s}: live={len(c)} coords={c}")

expected = sorted([(r + 1, c + 1) for r, c in init_c])
final_c = coords(g)
print(f"expected after 4 steps (shift +1,+1): {expected}")
print(f"VERIFY live_counts={counts} (all==5? {all(v == 5 for v in counts)})")
print(f"VERIFY shift_ok={final_c == expected}")
assert all(v == 5 for v in counts), f"live count changed: {counts}"
assert final_c == expected, f"glider did not translate: {final_c} vs {expected}"
print("PASS")
