# 1943 - M-P 神經元 (McCulloch & Pitts)
# 對應本書: 1943-麥卡洛克皮茨邏輯神經元.md
# 公式: y = H(sum_i w_i x_i - theta), H 為階躍函數
# 展示: 單一 M-P 神經元可做 AND/OR/NOT, 但單層做不出 XOR
import numpy as np


def mp_neuron(x, w, theta):
    return 1 if np.dot(w, x) - theta > 0 else 0


def demo_gate(name, w, theta, cases):
    print(f"--- {name}: w={w}, theta={theta} ---")
    for x, expected in cases:
        y = mp_neuron(np.array(x), np.array(w), theta)
        ok = "OK" if y == expected else "FAIL"
        print(f"  in={x} -> {y} (expect {expected}) [{ok}]")


def main():
    demo_gate("AND", [1, 1], 1.5,
              [([0, 0], 0), ([0, 1], 0), ([1, 0], 0), ([1, 1], 1)])
    demo_gate("OR", [1, 1], 0.5,
              [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 1)])
    demo_gate("NOT", [-2], -1, [([0], 1), ([1], 0)])
    # XOR: 暴力搜尋證明單一 M-P 神經元無解 (權重/閾值網格)
    xor = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    found = False
    for w1 in np.arange(-2, 2.5, 0.5):
        for w2 in np.arange(-2, 2.5, 0.5):
            for th in np.arange(-2, 2.5, 0.5):
                if all(mp_neuron(np.array(x), np.array([w1, w2]), th) == t
                       for x, t in xor):
                    found = True
    print("單層 M-P 神經元能否表達 XOR:", "能 (意外!)" if found else "不能 (符合 Minsky-Papert 論證, 需多層/隱藏層)")


if __name__ == "__main__":
    main()
