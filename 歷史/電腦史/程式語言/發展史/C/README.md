# C 程式語言發展史年表

> C 是 1972 年由 Dennis Ritchie 在 Bell Labs 為了改寫 UNIX 而誕生的語言，
> 目標是「組合語言的速度與貼近硬體，加上高階語言的可攜性與結構化」。
> 它以指標、struct、小型核心與「信任程式設計師」的哲學，
> 成為半世紀以來系統程式設計的事實標準，也是 UNIX、Linux、Windows、
> 以及所有現代語言（C++、Java、C#、Go、Rust、JavaScript 語法外觀）的共同祖先。

## 前史：理論根源

| 年份 | 事件 | 意義 |
|------|------|------|
| 1958 | ALGOL 58 / FORTRAN | 區塊結構、型別宣告、函式與遞迴傳統的源頭（C 的函式語法沿自 ALGOL） |
| 1960 | BCPL 語言 | 無型別的系統語言，`*p` 解參考語法的祖先 |
| 1967 | BCPL 影響下的 B 語言 | Ken Thompson 將 BCPL 簡化成 B，只有 machine word 一種型別 |
| 1968 | Dijkstra「結構化程式設計」 | goto 有害論；C 的 struct、函式分解呼應此思潮 |

## 正式年表

| 年份 | 標題 | 關鍵語法/特性 |
|------|------|---------------|
| 1969 | [UNIX 誕生](1969-UNIX誕生.md) | C 的搖籃：為寫作業系統而造語言，可攜性成為第一目標 |
| 1972 | [C 語言誕生](1972-C語言誕生.md) | 語言誕生：型別、指標、struct、函式——從 B 的無型別到有型別 |
| 1978 | [K&R 書與 UNIX 第七版](1978-KR書與UNIX第七版.md) | 事實標準：前置處理器、union、enum、typedef；附帶 UNIX 出售 |
| 1983 | [GCC 與 GNU 計畫誕生](1983-GCC與GNU計畫誕生.md) | 自由工具鏈：GCC 打破編譯器壟斷，GNU 生態成型 |
| 1989 | [ANSI C 標準（C89）](1989-ANSI-C標準C89.md) | 函式原型、void、const、volatile、標準函式庫定型 |
| 1991 | [Linux 誕生](1991-Linux誕生.md) | 史上最大 C 專案：證明自由工具鏈（gcc+glibc）的成熟 |
| 1995 | [C95 寬字元與國際化補丁](1995-C95寬字元與國際化補丁.md) | wchar_t、wchar.h、digraphs——國際化的第一波補課 |
| 1999 | [C99 重大修訂](1999-C99重大修訂.md) | `//`、long long、stdint.h、指定初始化、inline、VLA、宣告混排 |
| 2005 | [LLVM 與 Clang 問世](2005-LLVM與Clang問世.md) | 第二編譯器勢力：SSA IR、人性化錯誤訊息、ASan/UBSan |
| 2011 | [C11 執行緒與泛型](2011-C11執行緒與泛型.md) | C 記憶體模型、_Atomic、threads.h、_Generic、_Static_assert |
| 2018 | [C17 小修訂](2018-C17小修訂.md) | 不加特性、只修缺陷——「穩定優先」時代的態度轉變 |
| 2024 | [C23 最新標準](2024-C23最新標準.md) | bool/nullptr 關鍵字化、typeof、constexpr、#embed、移除 K&R 函式 |
| 2025 | [C 的未來與 C2y](2025-C的未來與C2y.md) | 記憶體安全攻防戰：profile、工具化安全、C ABI 作為通用介面 |

## 語法演進主軸

1. **1972–1978：從無型別到有型別** —— B 只有一種 word 型別；C 加入 int/char/float、指標、struct，型別直接映射 PDP-11 硬體指令，「型別即硬體」。
2. **1978–1989：從方言到標準** —— 前置處理器成熟、union/enum/typedef 定型；函式原型、const、volatile、void 補上型別檢查與介面契約，彌補「不檢查參數」的最大錯誤源。
3. **1989–1999：停滯十年後的大躍進** —— 吸收 C++ 經驗（`//`、inline、宣告混排），加入 long long、stdint.h、指定初始化，回應 64 位元時代。
4. **1999–2011：並發理論的補課** —— C 記憶體模型與 _Atomic 讓「data race」第一次有數學定義；_Generic、_Static_assert 以最小機制補上泛型與編譯期驗證。
5. **2011–2024：從加特性到還債與安全** —— C17 不加特性；C23 移除 K&R 函式、關鍵字化 bool/nullptr、加入 typeof/constexpr/#embed，並以 stdckdint.h 回應整數溢位與記憶體安全壓力。
6. **2025–：工具化安全時代** —— 安全不再靠語言特性堆疊，而靠 ASan、-fbounds-safety、靜態分析與 profile 子集；C 成為所有語言的通用底層介面（C ABI）。

## 工具鏈與軟體生態發展主軸

1. **1969 UNIX → 1991 Linux** —— C 的搖籃與最大舞台：UNIX 為了可攜性造出 C，Linux 以 gcc+glibc 證明自由工具鏈成熟，成為三千萬行 C 的工程實驗場。
2. **1983 GCC** —— 打破商業編譯器壟斷，多前端多後端架構讓 C 成為每個新平台的第一語言；GPL 自由軟體文化隨之擴散。
3. **1999 glibc/GLibc 時代** —— 標準函式庫（stdio、stdlib、string）成為跨平台契約，POSIX 讓 UNIX 系 API 標準化。
4. **2005 LLVM/Clang** —— 「編譯器即函式庫」的革命：ASan/UBSan/clang-tidy/clangd 重新定義 C 的品質保證，也催生 rustc、Swift、Zig。
5. **2020s 記憶體安全運動** —— NSA/CISA 報告與 Rust 進入 Linux/Windows/Android 核心，迫使 C 生態轉向工具化安全與漸進改造。

## 發展主軸

1. **1969–1978：為 OS 而生** —— 一門語言的誕生是為了解決「組合語言無法移植」的實務問題，K&R 讓它成為大學與業界的事實標準。
2. **1978–1999：標準化與大躍進** —— C89 定型契約，C99 吸收 C++ 經驗，確保 C 在系統程式設計的統治地位。
3. **1999–2011：並發時代** —— 多核心普及逼出 C 記憶體模型，C 語意理論完成最大一次補課。
4. **2011–至今：安全化與還債** —— C17 穩定、C23 還債與吸收既有實踐，在 Rust 與政府資安政策的壓力下，C 的未來靠工具、profile 與數十億行既有程式碼的漸進安全化。
