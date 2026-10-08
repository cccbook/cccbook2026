# 1978：K&R 書與 UNIX 第七版——事實標準的確立

## 事件
1978 年，Brian Kernighan 與 Dennis Ritchie 出版《The C Programming Language》（俗稱 K&R），書中描述的語言版本（K&R C）加上 UNIX 第七版（V7）的編譯器，成為其後十年業界的事實標準。UNIX 也自此附帶 C 編譯器出售，「買 UNIX 就有 C」讓 C 迅速散布到大學與業界。

## 為何重要
- **K&R C 的語法定型**：函式宣告的舊式風格、前置處理器（`#define`、`#include`）的完整化、`union`、`enum`、`typedef` 等都在此時期成熟。
- UNIX 第七版被譽為「第一個真正可攜的 UNIX」，BSD 與 System V 皆源自 V7。

## 理論與實用原因（各語法為何加入）
- **前置處理器（`#define`、`#include`、條件編譯 `#if`）**：
  - *彌補的缺陷*：早期 C 缺乏常數與巨集抽象，跨機器的可攜性需要針對不同硬體條件編譯不同程式碼。
  - *實用原因*：UNIX 要移植到字長、位元組序不同的機器，`#if` 讓一份原始碼服務多種硬體；`#include` 讓標頭檔成為模組介面——這個設計影響至今（C++、Objective-C 全盤繼承，也帶來了「重複編譯」的效率缺陷）。
- **`union`**：讓 OS 核心能用同一塊記憶體表示多種資料（如行程訊息的多型表示），節省記憶體——PDP-11 記憶體極為昂貴。
- **`enum` 與 `typedef`**：讓程式碼可讀性提高，型別名稱可自訂，彌補「裸 int 滿天飛、意義不明」的缺陷。
- **K&R 舊式函式宣告**：
  - *彌補的缺陷*：早期編譯器記憶體有限，無法保留完整函式原型，於是參數型別不寫在括號內——這個妥協後來被 1989 年 ANSI C 的「函式原型」修正。

## 彌補了什麼缺陷
K&R 時期補齊了 C 在「常數抽象、條件編譯、資料描述能力」上的不足；但函式無完整原型、缺乏標準、各實作方言叢生的缺陷，則留給 1989 年的 ANSI C 解決。

## 程式範例
前置處理器——一份原始碼服務多種硬體（UNIX 移植的核心需求）：

```c
/* 條件編譯：字長與位元組序不同的機器共用同一份程式碼 */
#if vax || pdp11
#  define WORDSIZE 32
#else
#  define WORDSIZE 16
#endif
```

`#define` 常數與巨集（彌補缺乏常數抽象的缺陷）：

```c
#define BUFSIZE 512              /* 常數：取代滿天飛的裸數字 */
#define MAX(a, b) ((a) > (b) ? (a) : (b))   /* 巨集：注意括號陷阱！ */

int x = MAX(BUFSIZE, 1024);      /* 若忘記括號：MAX(a,b) a>b?a:b 會因優先序出錯 */
```

`#include` 讓標頭檔成為模組介面：

```c
/* file.h —— 介面 */
struct inode *iget(unsigned short num);   /* K&R 舊式宣告（型別不在括號內） */
/* 缺陷：iget(999999) 傳錯參數型別，編譯器不會警告！ */
```

`union`——同一塊記憶體表示多種資料（PDP-11 記憶體昂貴）：

```c
union value {            /* OS 核心用同一塊記憶體表示多種內容 */
    long   num;          /* 整數值 */
    char   name[8];      /* 名字字串 */
};
union value v;
v.num = 42;              /* 寫入整數 */
/* v.name 現在是垃圾——union 只能同時用一個成員，節省 8 bytes 記憶體 */
```

`enum` 與 `typedef`——彌補「裸 int 滿天飛、意義不明」：

```c
typedef enum { READ, WRITE, EXEC } perm_t;   /* 以前是 #define READ 01 */

typedef struct inode { int i_mode; int i_uid; } inode_t;
inode_t node;            /* 不用每次寫 struct inode */
```

## 相關條目
- [1972-C語言誕生](1972-C語言誕生.md)
- [1989-ANSI-C標準C89](1989-ANSI-C標準C89.md)
- [1983-GCC與GNU計畫誕生](1983-GCC與GNU計畫誕生.md)
