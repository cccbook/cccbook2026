# -*- coding: utf-8 -*-
"""1999 HP 格點蛋白摺疊玩具 (對應 wiki：計算模擬學 / 蛋白質摺疊・HP lattice model)。

背景：Dill (1985) HP 模型把胺基酸簡化為疏水 H / 親水 P 兩類，
放在 2D 方格上做自避行走 (self-avoiding walk)，能量 = -1 × (非鍵結 H-H 接觸數)。
此處取課本式 8 珠鏈 HPPHPPHH，窮舉全部自避行走找最低能量 (ground state)。

只用 numpy；窮舉為純 Python DFS + numpy 驗算能量。固定種子 (此題為確定性窮舉)。
"""
import numpy as np

np.random.seed(1999)

SEQ = "HPPHPPHH"  # 8 珠
MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def energy_of(pos) -> int:
    """pos: list of (x, y)；回傳能量 = -H-H 接觸數。"""
    p = np.array(pos)
    n = len(pos)
    is_h = np.array([c == "H" for c in SEQ])
    contacts = 0
    for i in range(n):
        if not is_h[i]:
            continue
        for j in range(i + 2, n):  # 排除鏈上相鄰
            if not is_h[j]:
                continue
            if abs(p[i][0] - p[j][0]) + abs(p[i][1] - p[j][1]) == 1:
                contacts += 1
    return -contacts


def main():
    # 固定首兩珠以去除平移+旋轉對稱：(0,0) -> (1,0)
    best_e = 0
    best_conf = None
    total_saw = 0

    def dfs(path, visited):
        nonlocal best_e, best_conf, total_saw
        if len(path) == len(SEQ):
            total_saw += 1
            e = energy_of(path)
            if e < best_e:
                best_e = e
                best_conf = list(path)
            return
        x0, y0 = path[-1]
        for dx, dy in MOVES:
            nxt = (x0 + dx, y0 + dy)
            if nxt in visited:
                continue
            visited.add(nxt)
            path.append(nxt)
            dfs(path, visited)
            path.pop()
            visited.remove(nxt)

    dfs([(0, 0), (1, 0)], {(0, 0), (1, 0)})

    print(f"序列: {SEQ} (長度 {len(SEQ)})")
    print(f"窮舉自避行走總數 (固定首步去對稱後): {total_saw}")
    print(f"最佳能量 E* = {best_e}  (即 H-H 接觸數 = {-best_e})")
    print(f"一個最優構形 (x,y 序列): {best_conf}")
    # ASCII 視覺化
    xs = [c[0] for c in best_conf]
    ys = [c[1] for c in best_conf]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    grid = [["." for _ in range(xmax - xmin + 1)] for _ in range(ymax - ymin + 1)]
    for k, (x, y) in enumerate(best_conf):
        grid[y - ymin][x - xmin] = SEQ[k]
    print("最優構形圖 (y 由上而下):")
    for row in reversed(grid):
        print(" ".join(row))
    # 驗證：重算能量一致，且確實達到全域最優（窮舉保證）
    assert energy_of(best_conf) == best_e
    print(f"VERIFICATION: best_energy={best_e} contacts={-best_e} n_saw={total_saw} PASS")


if __name__ == "__main__":
    main()
