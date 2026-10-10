# 1999 TLA+：Lamport 的並行宇宙規格書

> 案件編號：1999-TLA。報案人：所有被並行 bug 咬過的工程師。案情：並行系統太難想清楚，測試測不出死結。破案者：Leslie Lamport。

## 案發現場

並行系統的 bug 最狡猾。它們不藏在單行程式裡，藏在交錯（interleaving）裡。兩個行程各自正確，合在一起就死結、活鎖、遺失更新。測試只能走過億萬交錯中的幾條，剩下的就是深夜當機的來源。

1977 年 Pnueli 把時序邏輯帶入程式驗證，1981 年模型檢測誕生，但工業界仍缺一支「能寫規格」的筆。工程師會寫虛擬碼，不會寫 $AG$ 與 $EU$ ；數學家會寫公式，不懂訊息佇列與容錯移轉。

Lamport 早已是並行演算法的傳奇（Bakery 演算法、Paxos、因果時鐘）。他在 1990 年代初提出 TLA（Temporal Logic of Actions），1999 年前後補上 PlusCal 與 TLC，形成完整工具鏈 TLA+ 。目標只有一個：讓工程師用數學寫出系統，再讓機器自動找反例。

## 偵查過程（含數學式/表格/理論）

### 線索一：TLA 的三段式宇宙

TLA 把系統寫成一個時序公式，標準形只有三段：

$$
Init \land \Box [Next]_{vars} \land Fairness
$$

其中 $Init$ 描述初態， $Next$ 描述下一步動作， $vars$ 為所有變數組成的元組， $Fairness$ 為公平性假設。

逐段解讀：

- $Init$ ：例如 $x = 0 \land queue = \langle \rangle$ 。
- $[Next]_{vars}$ 即 $Next \lor UNCHANGED \, vars$ ，允許「什麼都不變」的步（stuttering），使規格具備精化下的不變性。
- $\Box$ 為「永遠」， $Fairness$ 常用弱公平 $WF_{vars}(A)$ 或強公平 $SF_{vars}(A)$ 排除「某個該發生的動作永遠被忽略」的不合理反例。

動作（action）是含 primed 變數的公式，如 $x' = x + 1$ 表示 $x$ 加一。狀態謂詞不含 prime，時序公式描述無窮行為序列。

### 線索二：PlusCal 與 TLC 的雙人搭檔

TLA+ 本體是數學，工程師初見會卻步。Lamport 於是設計 PlusCal：一種長得像虛擬碼的前端，寫法如：

```
--algorithm Transfer {
  variables x = 0;
  process P = 0
  begin
    Inc: x := x + 1;
  end process
}
```

PlusCal 翻譯器把它轉成 TLA+ ，再交給 TLC 模型檢查器窮舉狀態。TLC 支援顯式列舉、對稱約簡、指紋雜湊，發現違反不變式或死結時，吐出最短反例軌跡。

表格：TLA+ 工具鏈。

| 層 | 工具 | 輸入 | 輸出 |
|---|---|---|---|
| 建模 | TLA+ / PlusCal | $Init$ 、 $Next$ 、性質 | 規格文件 |
| 檢查 | TLC | 規格＋有限模型 | 反例或通過 |
| 證明 | TLAPS | 歸納不變式 | 機械化證明 |

性質分兩類：安全性（safety，「壞事永不發生」）與活性（liveness，「好事終將發生」）。前者 TLC 最拿手，後者需公平性配合。

### 線索三：從硬體到 AWS 的破案實錄

TLA+ 的第一批戰果在硬體：Digital 的 Alpha 記憶體模型、快取一致性協定，皆用 TLA 抓到模擬沒抓到的角落。

真正的工業引爆是 Amazon AWS。Chris Newcombe 等人在 2011–2015 年報告：用 TLA+ 為 DynamoDB、S3、EBS 建模，在上線前抓到多個嚴重設計 bug。TLC 找到的反例長達數十步，人類審查根本走不到。

表格：代表案例。

| 案例 | 建模對象 | 抓到的問題 |
|---|---|---|
| Alpha 記憶體模型 | 多處理器讀寫序 | 規格歧義 |
| Disk Paxos | 容錯共識 | 活性違反 |
| DynamoDB | 複寫與容錯移轉 | 遺失確認 |
| S3 | 後台一致性流程 | 極端交錯死結 |

偵探筆記：TLA+ 的哲學是「先寫規格再寫程式」。規格只有數百行，卻能把設計者的模糊假設逼成 $Init$ 與 $Next$ ，模糊之處正是 bug 之家。

## 結案報告

案件告破。TLA+ 證明：並行正確性不是靠聰明，而是靠把交錯交給機器。一個公式、三段結構、一個檢查器，就讓 AWS 等級的系統在設計階段落網。

遺產有三：

1. 輕量形式方法（lightweight formal methods）典範：不必證明一切，先模型檢查關鍵規格。
2. stuttering 不變性與精化理論，成為後來 TLA 精化證明與分散式驗證的基礎。
3. 啟發 Alloy、Spin/Promela、Iris 等工具：規格語言與自動反例已成標配。

從因果鏈看，TLA+ 上承 Pnueli 時序邏輯與 1992 SMV 符號檢查，下啟分散式系統驗證與雲端可靠性工程。

## 證據與工具

證據 A：標準形再現，獨立成行。

$$
Init \land \Box [Next]_{vars} \land Fairness
$$

證據 B：弱公平定義。 $WF_{vars}(A)$ 意為：若動作 $A$ 持續被使能，則終將發生一步 $A$ 。它排除了排程器惡意餓死某行程的假反例。

證據 C：TLA+ 不變式示例。互斥： $Mutex \triangleq \neg (pc_0 = crit \land pc_1 = crit)$ ，以 $Inv \land [Next]_{vars} \Rightarrow Inv'$ 歸納證明，或直接交 TLC 檢查。

證據 D：延伸閱讀。Lamport 1994 年〈The Temporal Logic of Actions〉；Lamport 2002 年《Specifying Systems》免費公開；Newcombe 等 2015 年〈How Amazon Web Services Uses Formal Methods〉；TLC 與 TLAPS 官方手冊。
