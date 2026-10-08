# 1998：Erlang 開源

## 事件
Erlang 由 Joe Armstrong、Robert Virding 與 Mike Williams 於 1986 年在瑞典 Ericsson 計算機科學實驗室創造，最初是為了開發電信交換系統而設計的內部語言。1998 年，Ericsson 決定將 Erlang 開源（採 EPL 授權），同時一度宣布停止內部 Erlang 產品線、改用外部方案——隨後又在該年反轉決定，繼續以 Erlang 開發 AXD301 交換機。這台交換機之後達到了著名的 99.9999999%（九個九）可用性，成為分散式容錯系統的教科書案例。

## 語法/特性加入的理論與實用原因

### 1. Actor 行程：輕量、隔離、訊息傳遞
- **理論原因**：Erlang 的併發模型源自 actor 模型（Hewitt 1973）：行程（process）之間不共用記憶體，只透過非同步訊息傳遞溝通，理論上可免除鎖與競態條件。
- **實用原因**：Erlang 行程極輕量（KB 級、數百萬個可並存），每個行程有獨立 GC，行程崩潰不影響他者；電信系統正是「大量小型對話並存」的天然 actor 問題。
- **彌補缺陷**：用 C/C++ 寫容錯系統時，指標錯誤與記憶體共用會讓一個 bug 拖垮整個系統；行程隔離使錯誤可以局部化。

```erlang
%% 行程建立與訊息傳遞
Pid = spawn(fun loop/0),
Pid ! {hello, self()},
receive
  {reply, Msg} -> io:format("~p~n", [Msg])
end.
```

完整的收發迴路：行程以尾遞迴接收訊息，模式匹配決定行為——這就是 Erlang 行程的「狀態機」本質：

```erlang
-module(counter).
-export([start/0, loop/1]).

start() -> spawn(counter, loop, [0]).

%% 每則訊息用模式匹配分派；狀態以函數參數（單一賦值）攜帶
loop(N) ->
    receive
        {incr}        -> loop(N + 1);                %% 尾遞迴：常數堆疊
        {get, From}   -> From ! {count, N}, loop(N);
        stop          -> io:format("共 ~p 次~n", [N])  %% 不再遞迴，行程結束
    end.

%% 使用端：
%% Pid = counter:start(),
%% Pid ! {incr}, Pid ! {get, self()},
%% receive {count, N} -> io:format("~p~n", [N]) end.
```

對照組——用鎖保護共享計數器（Java/C++ 風格）與 Erlang 訊息傳遞的差異：

```java
// Java：共用記憶體，必須加鎖，忘記加鎖就是競態條件
class Counter {
    private int n = 0;
    synchronized void incr() { n = n + 1; }  // 鎖住整個物件
    synchronized int get()   { return n; }
}
```

Erlang 沒有鎖：狀態只存在於一個行程內，其他行程只能發訊息請求，天然免除競態條件。

### 2. 監督樹與「let it crash」哲學、OTP 框架
- **理論原因**：與其預防所有錯誤（防禦式程式設計），不如讓行程在出錯時立即崩潰，由監督者（supervisor）行程偵測並重啟它——錯誤處理回歸到「重啟到已知良好狀態」的簡單策略。
- **實用原因**：1998 年前後 Ericsson 將這些模式標準化為 OTP（Open Telecom Platform）框架：supervisor、gen_server、application 等行為模組，成為工業級容錯的標準配方。
- **彌補缺陷**：傳統例外處理程式碼往往比業務邏輯還多且不可靠；監督樹把容錯從「程式碼層」提升到「行程結構層」。

「let it crash」的概念碼——用 link/exit/monitor 串起監督關係，子行程崩潰由監督者重啟，而不是在業務邏輯裡包滿 try/catch：

```erlang
%% 監督者：linked 子行程，崩潰時收到 {'EXIT', Pid, Reason}
supervisor(Child) ->
    process_flag(trap_exit, true),      %% 攔截 EXIT 訊號
    receive
        {'EXIT', Child, Reason} ->
            io:format("子行程崩潰：~p，重啟~n", [Reason]),
            NewChild = spawn_link(fun risky/0),   %% 直接重啟到已知良好狀態
            supervisor(NewChild)
    end.

%% 子行程：不防禦，出錯就直接崩潰（let it crash）
risky() ->
    receive
        {div, A, B} -> A / B              %% B=0 時整個行程立即崩潰
    end,
    risky().

%% monitor：單向觀察，監督者不隨之崩潰
%% Ref = erlang:monitor(process, Pid),
%% receive {'DOWN', Ref, process, Pid, Reason} -> ... end.
```

OTP supervisor 的實際樣式（宣告式定義重啟策略）：

```erlang
%% OTP：以 child 規格宣告監督樹，框架代管啟動與重啟
init([]) ->
    SupFlags = #{strategy => one_for_one, intensity => 5, period => 10},
    Children = [#{id => counter,
                  start => {counter, start_link, []},
                  restart => permanent}],
    {ok, {SupFlags, Children}}.
```

### 3. 熱程式碼替換（hot code swapping）
- **理論原因**：Erlang 的函數版本機制（兩個版本共存、行程自主切換）在理論上支援不停機更新，根源於電信交換機不能停機的需求。
- **實用原因**：升級交換機軟體不需要斷線；這也使 Erlang 系統可以連續運行數年不重啟。
- **彌補缺陷**：傳統系統每次更新都要停機維護，對電信等高可用性領域不可接受。

熱替換的概念碼：模組載入新版本後，新呼叫用新版、仍在遞迴中的舊行程在進入下一次遞迴時切換：

```erlang
%% 載入新版模組；既有行程在下次 loop 進入時自動使用新版
code:load_file(counter).                 %% 編譯並載入新版本的 beam 檔

loop(N) ->
    receive
        {incr} -> loop(N + 1)
    end.
%% 兩個版本的 loop 共存：fully-qualified 呼叫 counter:loop/1 用「新版」，
%% 尾遞迴 loop(N + 1) 用「當前版」；行程在回到頂層遞迴時切換版本
```

函數式核心：函數頭模式匹配 + 尾遞迴，一行一個分支，邏輯一目瞭然：

```erlang
%% 以模式匹配在函數頭分支：處理串列的 map
double([])     -> [];                   %% 空串列：基礎情況
double([H|T])  -> [H * 2 | double(T)].  %% 尾遞迴式建構：常數堆疊
```

### 4. 函數式核心
- **理論原因**：單一賦值變數（single assignment）、模式匹配、尾遞迴，使行程邏輯易於驗證與除錯；輕量行程本身就是「狀態機」的封裝。
- **實用原因**：Armstrong 在 2003 年的博士論文中論證：Erlang 原始碼的錯誤密度顯著低於對照語言，函數式核心是主因之一。
- **彌補缺陷**：電信程式的並行狀態管理在命令式語言中極易出錯。

單一賦值的保證：變數一旦綁定就不可改，重複綁定直接編譯錯誤，消除一大類「狀態被意外竄改」的 bug：

```erlang
X = 10,
X = X + 1   %% 編譯錯誤：X 已綁定為 10，無法重新賦值
```

## 彌補了什麼缺陷
Erlang 彌補了用 C/C++ 建構分散式容錯系統的困難：行程隔離、監督樹、熱替換共同支撐了 AXD301 的九個九可用性。開源之後，Erlang 的影響力擴散：2009 年 WhatsApp 以少數工程師用 Erlang 撐起數億用戶的巨大併發量，成為著名案例；Elixir（2012）也建立在 Erlang VM（BEAM）之上。

## 相關條目
- [2007-Clojure誕生](2007-Clojure誕生.md)
- [1996-OCaml誕生](1996-OCaml誕生.md)
- [2004-Scala誕生](2004-Scala誕生.md)
