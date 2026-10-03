# 2013-React函數式UI

## 案件摘要

2013 年 5 月，JSConf US 的舞台上，Facebook 工程師 Jordan Walke 公開了一個內部孕育兩年的專案——React。它的前身是 Walke 於 2011 年開發的 FaxJS，一款用 PHP（XHP）與 JavaScript 實驗「UI 是狀態的函數」的雛形。React 拋棄了 jQuery 時代直接操作 DOM 的命令式寫法，改以宣告式的純函數模型重建整個前端世界觀。這起案件的謎題是：為什麼一個看似違反常識（每次都「重新渲染整個頁面」）的方案，反而解開了億級使用者產品的状态同步噩夢？破案關鍵，藏在數學式的純度與虛擬 DOM 的 O(n) diff 演算法裡。

## 前因 -- 為什麼會有這個案子

- jQuery 時代（2006–2013）的主流寫法是命令式：`$('.btn').on('click', function() { ... })`，程式碼一步步「指示」瀏覽器改哪個節點、改什麼文字。
- UI 狀態散落各處：DOM 本身、JavaScript 變數、閉包、伺服器回傳值，四處各有一份真相，同步全靠人工維護。
- Facebook 的廣告與通知系統是重災區：一則通知的已讀狀態要同步到角標、列表、紅點、彈窗等多個地方，任何一處漏改就是 bug。工程師戲稱這是「兩年才敢動一次的程式碼」。
- 命令式更新無法放心重試：同一行程式碼跑兩次，結果可能不同（狀態被改兩次），於是無法用「重新執行」來修復錯誤。
- 函數式思想在 FB 內部已有共識：pure function（相同輸入必得相同輸出、無副作用）、immutability（資料建好就不再改）、one-way data flow（資料只往一個方向流）。Walke 的 FaxJS 正是把這些原則搬到 UI 上的實驗。
- 更早的先聲：Evan Czaplicki 於 2012 年的 Elm 語言與 The Elm Architecture，已經示範了 `view : Model -> Html` 的純函數模型與單向資料流。

## 線索與推理 -- 數學式、程式、理論

### 線索一：UI = f(state) 的純函數模型

React 的核心假設可以用一條數學式寫下：

$$
\text{UI} = f(\text{state})
$$

其中 $f$ 是純函數：只要 state 相同，渲染出的 UI 必定相同。這意味著「UI 的歷史」不再重要——任何時刻的畫面都可以由當下的 state 完全重建。命令式時代的「狀態散落各處」被收斂成單一真相來源。

### 線索二：虛擬 DOM 與 O(n) diff

若每次 state 改變都真的重建整個 DOM，效能會崩潰。React 的解法是虛擬 DOM：先在記憶體中建一棵輕量的 JS 物件樹，與上一次的樹做 diff，只把差異套用到真實 DOM。兩樹 diff 的樸素演算法是 $O(n^3)$，React 的 reconciliation 演算法靠兩條啟發式假設壓到 $O(n)$：

1. 不同型別的元素會產生不同的樹（直接整棵替換，不再往下比）。
2. 開發者提供 key，暗示哪些子元素在同一列表中是穩定的。

用 Python 模擬這個 diff 思想：

```python
def diff(old, new, path="root", patches=[]):
    if old is None:
        patches.append(("ADD", path, new))
    elif new is None:
        patches.append(("REMOVE", path))
    elif old["type"] != new["type"]:
        patches.append(("REPLACE", path, new))
    elif old["type"] == "text":
        if old["text"] != new["text"]:
            patches.append(("TEXT", path, new["text"]))
    else:
        for i in range(max(len(old["children"]), len(new["children"]))):
            o = old["children"][i] if i < len(old["children"]) else None
            n = new["children"][i] if i < len(new["children"]) else None
            diff(o, n, f"{path}/{i}", patches)
    return patches

old = {"type": "div", "children": [
    {"type": "text", "text": "通知 3 則"},
    {"type": "text", "text": "廣告"},
]}
new = {"type": "div", "children": [
    {"type": "text", "text": "通知 4 則"},
    {"type": "text", "text": "廣告"},
]}

print(diff(old, new))
# [('TEXT', 'root/0', '通知 4 則')]  -- 只偵測到一處差異，其餘不動
```

### 線索三：單向資料流與 Flux

2014 年 Facebook 再發表 Flux 架構，把資料流固定成一個單向環：

$$
\text{Action} \rightarrow \text{Dispatcher} \rightarrow \text{Store} \rightarrow \text{View} \rightarrow \text{Action} \rightarrow \cdots
$$

View 只能「派發 Action」，不能直接改 Store。這是 Elm Architecture 的工業化版本：資料只往一個方向流，任何狀態變化都有明確的因果鏈，可追蹤、可重播。

### 線索四：純元件與 memoization

因為元件是純函數，相同 props 必得相同輸出——這正是 memoization 的數學前提。`React.memo` 記住上一次的 props，若這次 props 相同（淺比較），直接跳過重渲染：

$$
f(\text{props}) = \text{cache}[\text{props}] \quad \text{若 } \text{props} \in \text{cache}
$$

沒有純度，這個快取在數學上不成立；有了純度，效能優化只是查表。

### 線索五：Hooks——把副作用裝進容器

2019 年 React 16.8 發表 Hooks。函數元件原本不能有狀態與副作用，`useState` 與 `useEffect` 改變了這件事：

```jsx
function NotificationBadge() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    // 副作用（訂閱、請求）被「裝進」effect 容器，
    // 由 React 統一在渲染後執行與清理
    const unsubscribe = subscribeNotifications(setCount);
    return () => unsubscribe();
  }, []);

  return <span className="badge">{count}</span>;
}
```

`useEffect` 的本質，是把副作用從純函數本體抽離，放進一個由框架管理的容器。這與 Haskell 的 IO monad 同構：純函數不「執行」副作用，而是「描述」一個 `IO a` 型別的動作，由 runtime（React 或 GHC）在正確的時機執行。

$$
\text{render} :: \text{State} \rightarrow \text{UI}, \qquad \text{effects} :: \text{State} \rightarrow \text{IO}()
$$

純渲染與副作用分離——這正是 monad「分離純與不純」的核心思想，只是換了一身 JavaScript 的衣服。

## 結案 -- 後果與影響

- React 成為全球最流行的前端框架，支撐 Facebook、Instagram、Netflix、Airbnb 等億級使用者產品。
- 函數式思想（pure function、immutability、宣告式 UI）從學院冷門變成前端工業主流。
- Redux（2015，受 Flux 與 Elm 啟發）確立單向資料流與「reducer 是純函數」的準則；MobX、Elm 各自延續這條路。
- Hooks 影響了 Vue 3 的 Composition API 與 SwiftUI 的宣告式模型——宣告式 UI 成為跨平台共識。
- 「狀態散落各處」的問題以 state 容器與單一真相來源收案，command-imperative 的 jQuery 模式退出主流。

## 關鍵人物與文獻（條列）

- Jordan Walke——FaxJS（2011）與 React（2013）的原作者，Facebook 工程師。
- Evan Czaplicki——Elm 語言作者；Evan Czaplicki, "Elm: Concurrent FRP for Functional GUIs", Princeton Senior Thesis, 2012.
- Tom Occhino 與 Jordan Walke 在 JSConf US 2013 首次公開發表 React。
- Facebook 開源團隊, "React: A JavaScript library for building user interfaces", https://react.dev, 2013.
- Facebook, "Flux Application Architecture", 2014, https://facebook.github.io/flux.
- Andrew Clark et al., "React Hooks", React 16.8 官方文件, 2019, https://react.dev/reference/react.
- Philip Wadler, "Monads for functional programming", in Advanced Functional Programming, Springer, 1995——Hooks 與 IO monad 同構的理論源頭。
