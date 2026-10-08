# 2015：TensorFlow 與深度學習框架——從 Theano 到宣告式計算圖

## 事件
- **2007–2008**：蒙特婁大學 Yoshua Bengio 團隊開發 **Theano**——第一個 Python 深度學習框架：宣告式定義計算圖、自動微分（autodiff）、GPU 支援。
- **2013**：**Caffe**（Berkeley，C++）在影像辨識圈流行。
- **2015 年 11 月**：Google Brain 開源 **TensorFlow**——Theano 思想的工業級實作：計算圖、自動微分、分散式訓練、TensorBoard 視覺化。
- （2016 年 1 月，Facebook 的 **PyTorch** 問世，見下一篇。）

## 為何重要
- **自動微分是深度學習的核心技術**：訓練神經網路需要對任意計算圖求梯度；手寫反向傳播容易出錯，自動微分（autodiff，源自 1960–70 年代的代數計算理論）讓梯度自動且正確。
- **Theano 奠定了「宣告式計算圖」範式**：使用者描述計算（前向），框架編譯優化（融合運算、GPU 排程）並自動求梯度。Theano 於 2017 年停止開發，但它的思想活在 TensorFlow 與 PyTorch 中。
- **TensorFlow 1.x 的宣告式圖模式**：先定義靜態圖、再在 Session 中執行——效能極佳但除錯困難；這直接催生了 PyTorch 的「動態圖」路線（見 2016-PyTorch問世）。

## 理論與實用原因
- **理論原因**：
  - **自動微分**分為前向模式與反向模式（reverse-mode AD）；反向模式一次反向掃描即可算出對所有參數的梯度，正是反向傳播（1986 Rumelhart/Hinton/Williams）的廣義化。
  - **宣告式計算圖**源自資料流（dataflow）語言理論（1970 年代）：計算是節點、資料是邊，圖結構暴露給編譯器做優化（運算融合、並行排程）。
- **實用原因**：2012 年 AlexNet 赢得 ImageNet 後，深度學習爆發；研究者需要「GPU 加速 + 自動微分 + 可重現」的工具，Theano 太慢難用，於是工業界（Google）出手。

## 彌補了什麼缺陷
- Theano/TensorFlow 彌補了「手寫反向傳播易錯、NumPy 無 GPU、無自動微分」的缺陷。
- TensorFlow 彌補了 Theano「編譯慢、生態弱、無工業級分散式訓練」的缺陷——但自己引入了「靜態圖難除錯」的新缺陷，由 PyTorch 修正。

## 程式範例

Theano 的宣告式計算圖——先描述、後編譯：

```python
import theano.tensor as T

# 宣告式：定義符號變數與計算圖（此時還沒有真的計算）
x = T.matrix("x")
y = x * 2 + 1                 # 計算圖的節點與邊
f = theano.function([x], y)   # 編譯成 C/GPU 代碼，可做運算融合
```

自動微分——手寫 vs autodiff：

```python
# 手寫反向傳播：容易出錯（要自己推導每個梯度）
# grad_y = 2（手推）；若模型複雜，手推必錯

# Theano：梯度自動且正確
grad = T.grad(y.sum(), x)     # 自動微分：反向模式 AD
```

TensorFlow 1.x——工業級宣告式圖（與 PyTorch 的路線之爭，見 2016 篇）：

```python
import tensorflow as tf

# TF 1.x：先建靜態圖，再在 Session 中執行——效能好但除錯像黑箱
a = tf.placeholder(tf.float32, shape=(2, 2))
b = a * 2 + 1
with tf.Session() as sess:
    result = sess.run(b, feed_dict={a: [[1, 2], [3, 4]]})
# print(b) 只會印出 Tensor 物件，不是值——不能 print 中間值、不能用 pdb
```

GPU 加速：

```python
with tf.device("/gpu:0"):     # Theano 奠定的 GPU 支援，TF 工業化
    logits = dense_layer(x)
```

## 相關條目

- [2016-PyTorch問世](2016-PyTorch問世.md)
- [2006-NumPy問世與with陳述](2006-NumPy問世與with陳述.md)
