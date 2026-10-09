# -*- coding: utf-8 -*-
# 05.1 CNN 與權重共享：numpy 手寫 2D 互相關卷積，驗證平移等變性
import numpy as np

def conv2d(I, K):
    # 互相關（cross-correlation）：核不翻轉，步距 1
    kh, kw = K.shape
    oh, ow = I.shape[0] - kh + 1, I.shape[1] - kw + 1
    O = np.zeros((oh, ow))
    for x in range(oh):
        for y in range(ow):
            O[x, y] = np.sum(I[x:x+kh, y:y+kw] * K)
    return O

# 邊緣濾片（垂直邊偵測）
K = np.array([[1.0, -1.0],
              [1.0, -1.0]])

# 影像：垂直邊在中央 col 2（避開邊界截斷）
I = np.zeros((6, 6))
I[:, 2] = 1.0

# 平移後影像：垂直邊右移 2 格到 col 4（平移算子 T_v，v = 2）
I_shifted = np.zeros((6, 6))
I_shifted[:, 4] = 1.0

O1 = conv2d(I, K)
O2 = conv2d(I_shifted, K)

# 驗證平移等變性：T_v(I*K) = (T_v I)*K（精確逐元素相等）
O1_shifted = np.zeros_like(O1)
O1_shifted[:, 2:] = O1[:, :-2]  # 特徵圖右移 2 格
print("原始影像的特徵圖：")
print(O1)
print("特徵圖右移 2 格（T_v(I*K)）：")
print(O1_shifted)
print("平移影像的特徵圖（(T_v I)*K）：")
print(O2)
print("平移等變性驗證 T_v(I*K) == (T_v I)*K：", np.allclose(O1_shifted, O2))
print("特徵圖隨輸入同樣平移——平移等變性成立")
