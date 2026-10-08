# 1983 - System V 與 GNU 計畫（商業化與自由化的分岔）

## 案件摘要
1983 年，兩件看似無關的大事同年發生：
1. **AT&T 發布 System V**——Unix 商業化的旗艦版本（1982 年 System III 後的正式版）。
2. **Richard Stallman 發起 GNU 計畫**——「GNU's Not Unix」：一個完全自由的 Unix 相容系統。
$$\text{System V（封閉商業）} \quad \text{vs} \quad \text{GNU（自由開放）}.$$
**Unix 史上的大分岔：商業授權 vs 自由軟體**——這條裂縫延續至今 40 年。

## 前因 -- 為什麼會有這個案子
- **AT&T 解禁**：1982 年反壟斷判決（AT&T 拆分）解除，AT&T 終於**可以賣 Unix**——System V 是第一個正式商業產品線（System III 為試金石）。
- **Stallman 的動機**：MIT AI 實驗室的印表機驅動程式不給原始碼事件，讓 Stallman 決心對抗「封閉軟體」——**Unix 的商業化（不能改、不能傳）正是他要對抗的敵人**。
- **彌補的缺陷**：封閉 Unix 的使用者被綁死在廠商身上；GNU 要提供一個「使用者永遠擁有自由」的替代品。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：System V 的商業化特徵
- **SVID（System V Interface Definition）**：把 Unix 介面寫成正式規格——**商業客戶要的是穩定承諾**。
- **新功能**：TERMINFO（終端機能力資料庫，取代混亂的 termcap）、行程會計、系統 V 行程間通訊（IPC：訊息佇列、共享記憶體、號誌）。
- **彌補的缺陷**：termcap 的字串式描述易錯難維護；早期 Unix 無標準 IPC，行程間通訊只能靠 pipe/檔案。

### 第二條線索：GNU 的三大武器
1. **GPL 授權（1989 定型）**：copyleft——衍生作品必須同樣自由。
   $$\text{GPL} = \text{自由} \;\xrightarrow{\text{傳染}}\; \text{所有衍生品都自由}.$$
2. **Emacs（1985）**：可程式化的編輯器，用 Lisp 擴充一切。
3. **GCC（1987）**：自由 C 編譯器——**取代 Unix 廠商的專用編譯器**，是自由系統的關鍵拼圖。
- **理論基礎**：Stallman 1985 年發表《GNU 宣言》——軟體自由是使用者權利，不是商業策略問題。

### 第三條線索：GNU 工具的「Unix 複刻戰略」
Stallman 的策略不是發明新系統，而是**逐一複刻 Unix 工具**（ls、grep、awk、bash……全部自由版）——
$$\text{GNU 工具} \;\approx\; \text{Unix 工具（介面相容）} + \text{自由（實作全新）}.$$
- **彌補的缺陷**：介面相容讓使用者無痛遷移；全新實作讓授權乾淨無爭議。

### Shell 範例：System V IPC 的號誌

```c
/* System V 號誌 (1983)：行程間同步的標準 API */
#include <sys/sem.h>
#include <sys/ipc.h>

int semid = semget(IPC_PRIVATE, 1, IPC_CREAT | 0666);
struct sembuf op = { .sem_num = 0, .sem_op = -1, .sem_flg = 0 };
semop(semid, &op, 1);      /* P 操作：取得資源 */
/* ... 關鍵區段 ... */
op.sem_op = 1;
semop(semid, &op, 1);      /* V 操作：釋放資源 */
```

### Shell 範例：GNU 工具與 Unix 工具的對照

```bash
$ ls --help        # GNU ls（1985，自由版，功能擴充）
$ grep --color     # GNU grep（彩色高亮，Unix 原版沒有）
$ bash --version   # GNU bash（1989，Bourne shell 的自由後裔）
```

### 編輯器範例：Emacs 的 Lisp 擴充

```elisp
;; Emacs (1985)：用 Lisp 擴充編輯器——編輯器即作業系統
(defun hello-unix ()
  (interactive)
  (insert "GNU's Not Unix, 1983"))
```

## 結案 -- 後果與影響
- **System V 線**：SunOS→Solaris、HP-UX、AIX——1980–90 年代商業 Unix 的主流；SVR4 (1989) 統合 System V 與 BSD。
- **GNU 線**：GCC、Emacs、bash、glibc——1991 年 Linus 用這些工具把 Linux 核心（見 `1991-Linux誕生.md`）組成完整系統。
- **授權之戰**：GPL vs BSD vs 商業授權——今日開源世界的授權光譜就是 1983 年的分岔所留下的。
- 歷史教訓：**介面相容（複刻）+ 授權自由（copyleft）= 平民對抗帝國的兩大武器**。

## 關鍵人物與文獻
- **AT&T**：System V, SVID (1983)。
- **R. M. Stallman**：《GNU Manifesto》(1985)；GCC (1987)；Emacs。
- 相關案件：`1983-BSD4.2TCP_IP與Sun.md`、`1991-Linux誕生.md`。
