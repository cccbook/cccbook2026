# 1989 - POSIX 標準與 BSD 授權（統一戰國的規格書）

## 案件摘要
1988–89 年，IEEE 發布 **POSIX.1（IEEE Std 1003.1-1988）**——第一個 Unix 系統呼叫介面的正式標準。
同年 Berkeley 發布 **BSD 授權（4.3BSD-Tahoe 附帶的授權條款，1989 年 6 月正式定案）**——與 GNU GPL 分庭抗禮的自由授權。
$$\text{POSIX（介面標準）} \;+\; \text{BSD/GPL（自由授權）} \;=\; \text{戰國 Unix 的統一基礎}.$$

## 前因 -- 為什麼會有這個案子
- **戰國 Unix 的混亂**：1980 年代末，System V、BSD、Xenix、SunOS、HP-UX……各廠商的 Unix 介面互不相容——同一支程式在 A 廠可編譯、B 廠失敗。**彌補的缺陷：介面碎片化**。
- **美國政府的採購需求**：1980 年代美國聯邦政府要求「NIST 認證的作業系統」——需要一個可驗證的標準，POSIX 因此而生。
- **BSD 授權的動機**：BSD 內含大量 AT&T 原始碼，授權糾纏不清；Berkeley 決心**重寫 AT&T 的部分、留下乾淨的授權**——1989 年 Networking Release 1（Net/1）幾乎全部是 Berkeley 自己的程式碼。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：POSIX——介面即合約
$$\text{POSIX} = \{\text{open, read, write, fork, exec, signal, ...}\} \quad \text{——形式化的介面集合}.$$
- **理論基礎**：Liskov 代換原則的實踐——任何「POSIX 相容系統」都必須能執行任何 POSIX 程式。**介面標準讓程式與系統解耦**。
- **彌補的缺陷**：1980 年代 Unix 之間的差異讓移植成本高漲；POSIX 把「可移植」從美德變成**合約義務**。

### 第二條線索：POSIX 的關鍵規格
1. **系統呼叫**：open/read/write/close、fork/exec/wait、signal。
2. **shell**：POSIX sh（以 Bourne shell 為基礎，標準化語法）。
3. **工作控制**：csh 發明的 job control（&、jobs、fg、bg）進入標準。
4. **termios**：終端機 I/O 的標準介面。

### 第三條線索：BSD 授權 vs GPL
$$\text{BSD 授權} = \text{保留版權聲明即可自由使用（含商業閉源）}.$$
$$\text{GPL} = \text{衍生品必須同樣自由（copyleft 傳染）}.$$
- **彌補的缺陷**：GPL 的「傳染性」讓商業公司卻步；BSD 授權讓企業（如 Sun、後來的 Apple）可以閉源使用——**兩種授權補足自由軟體光譜的兩端**。

### C 範例：POSIX 相容的移植性

```c
/* _POSIX_C_SOURCE：明確聲明只使用 POSIX 介面 */
#define _POSIX_C_SOURCE 200809L
#include <unistd.h>
#include <fcntl.h>

int main(void) {
    /* 這段程式碼可在任何 POSIX 系統上編譯執行：
       Linux, macOS, FreeBSD, Solaris, AIX ... */
    int fd = open("data.txt", O_RDONLY);
    char buf[64];
    ssize_t n = read(fd, buf, sizeof(buf));
    close(fd);
    return 0;
}
```

### Shell 範例：POSIX sh 的可移植腳本

```sh
#!/bin/sh
# POSIX sh：在 Linux/macOS/BSD 上都能執行
# 注意：不用 bash 專屬語法（如 [[ ]]、陣列）
for f in *.log; do
    case "$f" in
        *.gz) ;;
        *) [ -s "$f" ] && wc -l "$f" ;;
    esac
done
```

## 結案 -- 後果與影響
- **POSIX 成為事實標準**：所有 Unix（含 Linux、macOS）都宣稱 POSIX 相容；Windows 的 Cygwin（1995）、WSL（2016）都是為了補足 POSIX 相容性而生。
- **BSD 授權的勝利**：FreeBSD/NetBSD/OpenBSD（1993）、macOS（2001，見 `2001-MacOSX以BSD為基礎.md`）都採 BSD 授權；今天 Apple、Sony（PlayStation 的 FreeBSD 核心）都受益於 BSD 授權的寬容。
- **SVR4（1989）**：AT&T 與 Sun 合作，統合 System V 與 BSD——戰國 Unix 在介面層面開始統一。
- 歷史教訓：**標準化的勝利不在技術，而在「讓程式碼可以搬家」的承諾**。

## 關鍵人物與文獻
- **IEEE**：POSIX.1-1988（IEEE Std 1003.1）。
- **UC Berkeley**：Networking Release 1 (1989)、BSD 授權。
- 相關案件：`1983-BSD4.2TCP_IP與Sun.md`、`1991-Linux誕生.md`。
