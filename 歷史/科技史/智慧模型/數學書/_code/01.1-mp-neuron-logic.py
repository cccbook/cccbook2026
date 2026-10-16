# 01.1 M-P 神經元與邏輯閘驗證
# 用 numpy 實現線性閾值單元（LTU），驗證 AND/OR/NOT 邏輯閘
# 以及 XOR 需要兩層網路才能實現
import numpy as np

def mtp(x, w, theta):
    """McCulloch-Pitts 神經元：加權求和過門檻"""
    return 1 if x @ w >= theta else 0

# 定義四種邏輘閘的參數
inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
gates = {
    "AND": (np.array([1, 1]), 2),
    "OR":  (np.array([1, 1]), 1),
}

print("=== 單層 M-P 神經元實現 AND 與 OR ===")
for name, (w, th) in gates.items():
    outs = [mtp(np.array(x), w, th) for x in inputs]
    print(f"{name}: {list(zip(inputs, outs))}")

print("\n=== 單輸入 NOT 閘 ===")
for x in [0, 1]:
    print(f"NOT({x}) = {mtp(np.array([x]), np.array([-1]), 0)}")

print("\n=== 兩層 M-P 網路實現 XOR ===")
# y = XOR(x1,x2) = (x1 OR x2) AND NOT(x1 AND x2)
def xor_network(x):
    x = np.array(x)
    h_or  = mtp(x, np.array([1, 1]), 1)   # 第一層：OR
    h_and = mtp(x, np.array([1, 1]), 2)   # 第一層：AND
    h_not = mtp(np.array([h_and]), np.array([-1]), 0)  # NOT(AND)
    return mtp(np.array([h_or, h_not]), np.array([1, 1]), 2)  # 第二層：AND

outs = [xor_network(x) for x in inputs]
for x, y in zip(inputs, outs):
    print(f"XOR{x} = {y}")
assert outs == [0, 1, 1, 0], "XOR 真值表錯誤"
print("\n驗證成功：兩層 M-P 網路正確實現 XOR，單一 LTU 則不可（對角對無法被一直線分開）。")

# 附註：單一 LTU 不能做 XOR——程式以窮舉說明
print("\n=== 窮舉驗證：不存在單一 LTU 實現 XOR ===")
found = False
for w1 in np.arange(-3, 3.01, 0.5):
    for w2 in np.arange(-3, 3.01, 0.5):
        for th in np.arange(-3, 3.01, 0.5):
            outs2 = [mtp(np.array(x), np.array([w1, w2]), th) for x in inputs]
            if outs2 == [0, 1, 1, 0]:
                found = True
print(f"窮舉權重空間找到解：{found}（理論證明應為 False）")
