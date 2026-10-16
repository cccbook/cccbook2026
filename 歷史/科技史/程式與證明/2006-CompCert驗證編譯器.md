# 2006 CompCert 驗證編譯器：編譯器不再是嫌疑人

> 案件編號：2006-COMPCERT。報案人：Airbus 等高可靠產業。案情：源程式已驗證，編譯器卻可能誤譯。破案者：Xavier Leroy。

## 案發現場

形式驗證有個尷尬的盲點：你在 C 源碼層證明了程式正確，編譯器卻是未驗證的黑箱。它做優化、暫存器分配、指令排程，任何一處誤譯都讓源碼證明作廢。業界稱之為「驗證鴻溝」。

Airbus 的飛控軟體不敢賭。C 語言語意本就**枝微末節（ub、未定義行為），編譯器優化又越來越激進。測試只能說「測過的案例沒錯」，不能說「所有行為都保留」。誰來為編譯器作證？

2006 年起，INRIA 的 Leroy 交出 CompCert：一個用 Coq 寫成、用 Coq 證明的 C 編譯器，從 C 子集直達 PowerPC/ARM/x86 組合語言，附帶語意保持定理。這不是「測試充分的編譯器」，而是「攜帶證明的編譯器」。

## 偵查過程（含數學式/表格/理論）

### 線索一：語意保持即行為包含

Leroy 先把問題數學化。設源程式為 $C$ ，編譯結果為 $S$ ，其可觀察行為集合各記為 $Beh(C)$ 與 $Beh(S)$ 。行為含正常終止、發散、系統呼叫軌跡。正確編譯意味著目標行為不超出源行為允許範圍：

$$
Beh(S) \supseteq Beh(C)
$$

注意方向容易誤讀：此處 $Beh$ 以「改進」語意理解，或等價寫成「 $S$ 的每個可觀察行為都是 $C$ 允許的」。實務表述常為：若 $C$ 有定義行為 $B$ ，則 $S$ 亦產生 $B$ ；若 $C$ 有未定義行為，則 $S$ 可任意（但不憑空引入可觀察錯誤）。

表格：行為分類。

| 行為 | 例子 | 編譯要求 |
|---|---|---|
| 終止 $Terminates(n)$ | 回傳值 $n$ ＋ IO 軌跡 | 完全保留 |
| 發散 $Diverges$ | 無窮迴圈＋有限前綴軌跡 | 前綴保留 |
| 卡住 $GoesWrong$ | 未定義行為 | 不得由編譯引入 |

### 線索二：小步語意＋模擬關係圖

要證明上述包含，Leroy 為每層中間語言定義小步操作語意（small-step）： $s \rightarrow s'$ 。編譯器由約 20 遍（pass）組成：Clight → Cminor → RTL → LTL → Mach → Asm，每遍獨立證明。

每遍的核心是一條模擬（simulation）圖。設源狀態 $s$ 對應目標狀態 $t$ ，記為 $s \sim t$ 。前向模擬要求：

$$
s \sim t \land s \rightarrow s' \Rightarrow \exists t' : t \rightarrow^* t' \land s' \sim t'
$$

畫成圖即：源走一步，目標走零步或多步跟上，模擬關係保持。二十張小圖拼成大定理，任一優化（如常數傳播、死碼刪除）只需局部證明其模擬圖。

偵查筆記：CompCert 使用「星形模擬」與「測度」處理發散與口吃步（stuttering），確保無窮行為亦被保留。記憶體模型 CompCert memory 以塊＋偏移建模，支撐指標推理。

### 線索三：四萬行 Coq 與 Airbus 採用

CompCert 證明約 4 萬行 Coq（今已逾 10 萬行），程式與證明混寫：中間語言語法是歸納定義，優化是 Gallina 函數，正確性是定理。Coq 抽取（extraction）產生可執行的 OCaml 編譯器，信任基僅 Coq 核心＋抽取＋組合語言語意。

Airbus 與 AbsInt 等公司隨後在關鍵飛控與靜態分析鏈中採用 CompCert：源碼層用 Astrée 證無執行期錯誤，編譯層用 CompCert 保行為，兩端合攏。這是 PCC 理想的另一實現：編譯器自帶證明。

| 編譯器 | 保證 | 手段 |
|---|---|---|
| GCC/Clang | 測試＋經驗 | 回歸測試 |
| CompCert | 語意保持 $Beh(S) \supseteq Beh(C)$ | Coq 模擬證明 |

## 結案報告

案件告破。編譯器從最大嫌疑人變成證人：每遍優化皆有模擬圖作證，端到端定理一次封印。驗證鴻溝被填上，源碼證明終於能活到晶片上。

遺產有三：

1. 驗證編譯器路線確立，後有 CakeML、Velvet、JSCert 跟進。
2. 中間語言語意與記憶體模型成為後續並行、分離邏輯研究的基石。
3. 工業採納證明「證明有市場」：Airbus 願為確定性付費。

從因果鏈看，CompCert 上承 Hoare 邏輯、PCC、Coq，下啟 seL4 與高可靠工具鏈：證明從程式走向系統棧每一層。

## 證據與工具

證據 A：語意保持再現，獨立成行。

$$
Beh(S) \supseteq Beh(C)
$$

其中 $S$ 為組合語言目標， $C$ 為 C 源碼， $Beh$ 為可觀察行為集。

證據 B：前向模擬圖（文字版）。

```
s  ----->  s'
|          |
~          ~
|          |
v          v
t  --*-->  t'
```

證據 C：Coq 定理骨架。 `Theorem transf_correct : forall s t, transf s = OK t -> fsim s t.` 每遍如 `CminorSel` 、 `RTLgen` 、 `Regalloc` 皆有各自實例。

證據 D：延伸閱讀。Leroy 2009 年〈Formal Verification of a Realistic Compiler〉（CACM）；CompCert 官方文件與 Coq 原始碼；Airbus/AbsInt 導入報告。
