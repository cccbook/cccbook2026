# 2016 - AlphaGo: 策略直覺 + MCTS 搜尋 (井字棋縮影)
# 對應本書: 2016-AlphaGo.md
# 公式: UCT(s,a) = Q(s,a) + c·√(ln N(s)/N(s,a)); rollout 淺層模擬 + 價值評估混合
# 展示: 純隨機 rollout 的 MCTS 在井字棋上輾壓隨機走子 -- 「直覺引導下搜尋」的最小骨架
import numpy as np

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for a, c, d in LINES:
        if b[a] != 0 and b[a] == b[c] == b[d]:
            return b[a]
    return 0 if 0 in b else 3  # 3=和棋


def legal(b):
    return [i for i, v in enumerate(b) if v == 0]


def mcts_move(board, player, sims=300, c=1.4, seed=0):
    """以 player 視角做 MCTS: Q+UCT 選子, 隨機 rollout 評估."""
    rng = np.random.default_rng(seed)
    N = {a: 0 for a in legal(board)}
    W = {a: 0.0 for a in legal(board)}
    tot = 0
    for _ in range(sims):
        # UCT 選擇 (未試過的先各試一次)
        untried = [a for a in N if N[a] == 0]
        a = rng.choice(untried) if untried else max(
            N, key=lambda m: W[m] / N[m] + c * np.sqrt(np.log(tot) / N[m]))
        b2 = board.copy()
        b2[a] = player
        turn = 3 - player
        while winner(b2) == 0:  # rollout: 隨機下完 (淺層模擬的極簡版)
            b2[rng.choice(legal(b2))] = turn
            turn = 3 - turn
        w = winner(b2)
        r = 1.0 if w == player else (0.5 if w == 3 else 0.0)
        N[a] += 1
        W[a] += r
        tot += 1
    return max(N, key=lambda m: W[m] / N[m])


def play(mcts_first=True, seed=0):
    rng = np.random.default_rng(seed)
    b = np.zeros(9, dtype=int)
    turn, go_first = 1, mcts_first
    while winner(b) == 0:
        if go_first:
            b[mcts_move(b, turn, seed=rng.integers(1e9))] = turn
        else:
            b[rng.choice(legal(b))] = turn
        turn, go_first = 3 - turn, not go_first
    return winner(b)


def main():
    mcts_wins = draws = rand_wins = 0
    for i in range(40):  # MCTS 先後手各 20 局
        w = play(mcts_first=(i % 2 == 0), seed=i)
        mcts_side = 1 if i % 2 == 0 else 2
        if w == 3:
            draws += 1
        elif w == mcts_side:
            mcts_wins += 1
        else:
            rand_wins += 1
    print(f"MCTS(300次模擬) vs 隨機走子 40局: 勝={mcts_wins} 和={draws} 負={rand_wins}")
    print("結論: 搜尋即直覺的放大器 -- AlphaGo 把 rollout 換成策略/價值網路, 把井字棋換成圍棋")


if __name__ == "__main__":
    main()
