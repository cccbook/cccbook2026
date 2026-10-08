# 2016：PyTorch 問世——動態計算圖與 Python-first 的深度學習

## 事件
- **2016 年 10 月**：Facebook AI 研究院（Soumith Chintala、Adam Paszke 等）開源 **PyTorch 0.1**——以 Python 為第一語言的深度學習框架：**動態計算圖（define-by-run）**、`autograd` 自動微分、與 NumPy 無縫互通。
- **2018 年**：**PyTorch 1.0** 發佈，合併 Caffe2 與 ONNX 支援，加入 TorchScript（追蹤/腳本化把動態圖凍結為可部署的靜態圖）。
- **2022 年**：PyTorch 從 Meta 移交 **PyTorch Foundation**（隸屬 Linux 基金會），完成中立化。
- **2020 年代**：PyTorch 成為學術界壓倒性主流（論文採用率超過 80%），Hugging Face、Stable Diffusion、LLaMA 等生成式 AI 生態皆以 PyTorch 為基礎。

## 為何重要
- **動態圖 vs 靜態圖的路線之爭**：TensorFlow 1.x「先建圖、後執行」，效能好但**除錯像黑箱**——不能直接 print 中間值、不能用 pdb 逐步追蹤。PyTorch 選擇「執行即定義」（define-by-run）：每一行程式碼立即執行，計算圖在執行中動態建構——**用 Python 的直覺寫深度學習**。
- **Python-first 的勝利**：前身 Lua Torch（2002）效能好但 Lua 生態太小；PyTorch 以 Python 為原生介面，研究者的 NumPy 知識直接可用。
- **研究到部署的雙軌**：TorchScript/ONNX 補上「動態圖不便部署」的短板，證明兩種模式可以共存。

## 理論與實用原因
- **理論原因（動態圖）**：宣告式靜態圖（Theano/TensorFlow）把「定義」與「執行」分離，違反 Python 的互動式傳統；動態圖回到 **REPL 式計算**——每個張量操作立即執行，控制流（if/loop）就是 Python 原生控制流。理論上，條件與迴圈形狀依賴資料的模型（RNN、樹狀網路）在靜態圖中需要特殊算子，動態圖則自然表達。
- **理論原因（autograd）**：**反向模式自動微分**（見 2015-TensorFlow 篇）以「動態 tape 記錄」實作——每次操作記錄反向函式，`loss.backward()` 沿 tape 反向累積梯度。相比靜態圖的編譯期微分，動態 tape 犧牲一點效能換取完全的彈性。
- **實用原因**：研究者除錯時間遠大於訓練時間；「能 print、能 pdb、if/while 直接寫」的框架大幅提升研究迭代速度——這是 PyTorch 赢得學術界的根本原因。

## 彌補了什麼缺陷
- 彌補了 TensorFlow 1.x/Theano「靜態圖難除錯、控制流表達受限、學習曲線陡峭」的缺陷。
- 彌補了 Lua Torch「生態太小、與科學 Python 棧割裂」的缺陷。
- TorchScript 彌補了動態圖「不便生產部署與跨語言執行」的缺陷。

## 程式範例

動態圖 vs 靜態圖——「用 Python 的直覺寫深度學習」：

```python
import torch

# 執行即定義（define-by-run）：每行立即執行，控制流就是 Python 原生控制流
x = torch.randn(3, requires_grad=True)

# 可以 print 中間值、可以用 pdb 逐步追蹤——TensorFlow 1.x 做不到
y = x * 2
print(y)                      # 印出真正的值，不是 Tensor 物件

# if/while 直接寫：形狀依賴資料的模型（RNN、樹狀網路）自然表達
def rnn_step(h, x):
    if h.abs().sum() > 10:    # Python 原生 if——靜態圖需要特殊算子
        h = h * 0.1
    return h + x
```

autograd——動態 tape 記錄反向函式：

```python
w = torch.randn(2, 2, requires_grad=True)
loss = (w ** 2).sum()
loss.backward()               # 沿 tape 反向累積梯度——自動且正確
print(w.grad)                 # tensor 2w——不用手推反向傳播
```

與 NumPy 無縫互通：

```python
import numpy as np
a = np.random.rand(3, 3)
t = torch.from_numpy(a)       # NumPy 知識直接可用
t.numpy()                     # 互相轉換，零拷貝
```

TorchScript——補上部署短板：

```python
scripted = torch.jit.script(rnn_step)  # 凍結為可部署的靜態圖
scripted.save("model.pt")              # 跨語言執行（C++ runtime）
```

## 相關條目

- [2015-TensorFlow與深度學習框架](2015-TensorFlow與深度學習框架.md)
- [2006-NumPy問世與with陳述](2006-NumPy問世與with陳述.md)
- [2014-Jupyter問世](2014-Jupyter問世.md)
