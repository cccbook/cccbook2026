# JavaScript 程式語言發展史年表

> JavaScript 是1995年由 Brendan Eich 在網景公司（Netscape）以十天時間創造的語言。
> 它融合了 Scheme（函數式）、Self（原型繼承）與 Java/C（語法外殼）三大傳統，
> 從瀏覽器腳本語言演化為橫跨前端、後端、行動裝置與物聯網的通用語言。
> 本書同時記錄**語言本身**與**開發者軟體**（瀏覽器、執行時、工具鏈）兩條主線——
> 它們互相推動：瀏覽器大戰催生標準化，Node 催生 ES6，框架催生不可變語法。

## 前史：理論根源

| 年份 | 事件 | 意義 |
|------|------|------|
| 1936 | 圖靈機與 Lambda 演算 | 一級函數（first-class function）的數學基礎 |
| 1958 | LISP 問世 | 函數作為值、動態型別、垃圾回收的先驅 |
| 1967 | SIMULA 67 | 類別（class）概念的起源 |
| 1972 | Parnas 資訊隱藏理論 | 封裝與私有欄位的理論基礎 |
| 1975 | Scheme 發表 | 詞法作用域與一級函數的簡潔實現 |
| 1976 | Promise 理論 | 非同步程式設計的理論基礎 |
| 1987 | Self 語言 | 原型繼承：物件不需類別，直接複製他人 |
| 1993 | Mosaic 瀏覽器 | 全球資訊網爆發，瀏覽器需要腳本語言 |

## 語言與開發者軟體年表

### 一、誕生與瀏覽器大戰（1994–2001）

| 年份 | 標題 | 事件 |
|------|------|------|
| 1994 | [Netscape Navigator 問世](1994-NetscapeNavigator問世.md) | 第一個商業成功的瀏覽器，促成 JS 誕生 |
| 1995 | [JavaScript 誕生](1995-JavaScript誕生.md) | 十天創造：原型繼承、一級函數、動態型別、var |
| 1995 | IE 1.0 隨 Windows 95 問世 | 瀏覽器大戰（1995–2001）開端 |
| 1996 | [JScript 大戰與瀏覽器相容性危機](1996-JScript大戰與瀏覽器相容性危機.md) | IE 3 逆向工程出 JScript，碎片化催生標準化 |
| 1996 | [VBScript 問世](1996-VBScript問世.md) | 微軟以 VB 語法對抗 JS，後因封閉消亡 |
| 1997 | [ECMAScript 1 標準化](1997-ECMAScript1標準化.md) | ECMA-262 第一版，統一語言規範 |
| 1998 | [ECMAScript 2](1998-ECMAScript2.md) | ISO/IEC 16262 對齊，純編輯性修訂 |
| 1998 | [Mozilla 開源](1998-Mozilla開源.md) | 網景開源瀏覽器，Firefox 的基礎 |
| 1999 | [ECMAScript 3：正則表達式與例外處理](1999-ECMAScript3正則表達式與例外處理.md) | RegExp、try/catch、switch、do-while |
| 1999 | [XMLHttpRequest 問世](1999-XMLHttpRequest問世.md) | IE 5 為 Outlook Web Access 首創非同步資料取回 |

### 二、IE 壟斷與蟄伏（2001–2008）

| 年份 | 標題 | 事件 |
|------|------|------|
| 2001 | [微軟反壟斷案與第一次瀏覽器大戰落幕](2001-微軟反壟斷案與第一次瀏覽器大戰落幕.md) | IE 6 市佔95%以上，五年零創新的雙重停滯 |
| 2001 | [JSON 的發明](2001-JSON的發明.md) | Crockford 以 JS 物件字面量發明資料交換格式 |
| 2002 | [Phoenix 專案——Firefox 的前身](2002-Mozilla與Firefox之路.md) | 輕量獨立瀏覽器，打破壟斷的起點 |
| 2004 | [Firefox 1.0 問世](2004-Firefox-1-0問世.md) | 第二次瀏覽器大戰開打，標準實作復興 |
| 2005 | [Ajax 革命](2005-Ajax革命.md) | Gmail/Google Maps 證明 Web 可做應用程式 |

### 三、重生與現代化（2008–2015）

| 年份 | 標題 | 事件 |
|------|------|------|
| 2008 | [Chrome 問世與 V8 引擎](2008-Chrome問世與V8引擎.md) | JIT 讓 JS 速度提升一個數量級，Node 的先決條件 |
| 2009 | [ECMAScript 5：嚴格模式與 JSON](2009-ES5嚴格模式與JSON.md) | "use strict"、getters/setters、map/filter/reduce、bind |
| 2009 | [Node.js 問世](2009-Nodejs問世.md) | V8 + 事件迴圈，JavaScript 走出瀏覽器 |
| 2010 | [npm 與套件管理生態](2010-npm套件管理生態.md) | 世界上最大的套件庫，生態爆發 |
| 2012 | [TypeScript 問世](2012-TypeScript問世.md) | 漸進式靜態型別，彌補動態型別的工程化缺陷 |
| 2013 | [React 與前端框架革命](2013-React與前端框架革命.md) | 宣告式 UI、虛擬 DOM、JSX、單向資料流 |
| 2014 | [Babel 與 webpack——轉譯時代](2014-Babel與webpack轉譯時代.md) | 新語法可立即使用，模組戰國統一 |
| 2015 | [ECMAScript 6（ES2015）：現代化的黎明](2015-ES6現代化的黎明.md) | let/const、箭頭函數、class、Promise、ESM、解構 |

### 四、年度小步快跑（2016–至今）

| 年份 | 標題 | 關鍵語法/事件 |
|------|------|---------------|
| 2016 | [ES2016：指數運算子](2016-ES2016指數運算子.md) | `**`、Array.includes |
| 2017 | [ES2017：async/await](2017-ES2017async-await.md) | async/await、共享記憶體與 Atomics、Object.values/entries |
| 2018 | [ES2018：非同步迭代](2018-ES2018非同步迭代.md) | for await...of、物件展開/其餘、Promise.finally、正則命名群組 |
| 2018 | [Deno 構想](2018-Deno構想.md) | Ryan Dahl 反思 Node 十大缺陷，宣布 Deno |
| 2019 | [ES2019：扁平化陣列](2019-ES2019扁平化陣列.md) | flat/flatMap、Object.fromEntries、可省略 catch 綁定 |
| 2020 | [ES2020：可選鏈與空值合併](2020-ES2020可選鏈與空值合併.md) | `?.`、`??`、BigInt、Promise.allSettled、動態 import |
| 2020 | [Deno 1.0 問世](2020-Deno-1-0問世.md) | 安全沙箱、TS 內建、URL 匯入 |
| 2020 | [Vite 與新一代建構工具](2020-Vite新一代建構工具.md) | 原生 ESM + esbuild，終結 webpack 漫長等待 |
| 2021 | [ES2021：邏輯賦值運算子](2021-ES2021邏輯賦值運算子.md) | `\|\|=`、`&&=`、`??=`、replaceAll、數字分隔符、Promise.any |
| 2022 | [ES2022：頂層 await 與類別欄位](2022-ES2022頂層await與類別欄位.md) | 頂層 await、私有欄位 `#x`、Array.at、error.cause |
| 2023 | [ES2023：不可變陣列方法](2023-ES2023不可變陣列方法.md) | toSorted/toReversed/with、findLast、Hashbang |
| 2023 | [Bun 問世](2023-Bun問世.md) | Zig + JavaScriptCore，全能一體的運行時 |
| 2024 | [ES2024：分組與迭代輔助器](2024-ES2024分組與迭代輔助器.md) | Object.groupBy、迭代器輔助器、Promise.withResolvers |
| 2025 | [ES2025 與未來展望](2025-ES2025與未來展望.md) | Import Attributes、Set 方法、Temporal 曆法提案 |

## 發展主軸

1. **1995–1999：誕生與標準化** —— 十天創造的語言，瀏覽器大戰的碎片化四年內催生 ECMAScript 標準。
2. **2000–2008：停滯與蟄伏** —— IE 6 壟斷與 ES4 內戰讓語言凍結十年，但 Ajax 讓生態暗中爆發。
3. **2009–2015：重生** —— V8、Node.js、ES5/ES6 讓 JavaScript 成為通用語言。
4. **2016–至今：每年小步快跑** —— TC39 年度發佈 + 「社群先試、標準後收」模式；執行時（Node/Deno/Bun）三雄競爭，工具鏈（Babel/webpack/Vite）不斷重寫效率極限。
