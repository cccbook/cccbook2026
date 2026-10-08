# 1983：GCC 與 GNU 計畫誕生——自由軟體的工具鏈革命

## 事件
1983 年，Richard Stallman 宣布 GNU 計畫，目標是打造一個完全自由的類 UNIX 作業系統。1985 年 GNU C 編譯器（GCC）第一版發佈。GCC 讓任何人在任何機器上都能免費取得高品質的 C 編譯器，是自由軟體運動的第一塊基石。

## 為何重要
- **打破編譯器壟斷**：1980 年代 Unix 廠商的 C 編譯器要價數千美元且各自為政；GCC 免費、開源、可攜，直接促成 C 語言的民主化。
- **GCC 的技術傳統**：中間表示（RTL）、多前端多後端架構、最佳化選項（-O0～-O3）、跨平台交叉編譯，成為其後所有編譯器（LLVM/Clang 亦然）的參考對象。
- **GNU 工具鏈成型**：GCC + glibc + binutils + GNU Make + Emacs + Bash，構成 Linux 之後得以起飛的完整使用者空間。

## 理論與實用原因
- **理論原因**：Stallman 主張軟體應如數學公式般自由傳播（自由軟體四大自由）；GPL 授權以「copyleft」確保衍生作品同樣自由，是法律與軟體工程交叉的創新。
- **實用原因**：GNU 系統需要一個 C 編譯器，當時沒有自由選擇，只能自己寫。GCC 一開始就設計成多後端，讓「新硬體上第一個能跑的編譯器」往往是 GCC——這也讓 C 成為新平台的第一語言。

## 彌補了什麼缺陷
彌補了「高品質編譯器被商業壟斷、價格高昂、不可修改、平台綁定」的缺陷；也彌補了各廠商方言叢生、缺乏統一工具鏈的缺陷。GPL 與自由軟體文化更彌補了「軟體無法自由修改與分享」的制度性缺陷。

## 程式範例
GCC 的多最佳化等級與編譯流程——一個 C 程式如何變成執行檔：

```c
/* hello.c */
#include <stdio.h>

int main(void) {
    for (int i = 0; i < 3; i++)
        printf("hello, GNU\n");
    return 0;
}
```

```sh
$ gcc hello.c -o hello          # 最基本：一行編譯
$ gcc -O0 hello.c -o hello      # 無最佳化，方便除錯
$ gcc -O3 -march=native hello.c -o hello   # 全力最佳化
$ gcc -S hello.c                # 產生組合語言 hello.s（可看中間結果）
$ gcc -c hello.c                # 只編譯不連結，產生 hello.o
```

交叉編譯——GCC 讓「新硬體上第一個能跑的編譯器」成為現實：

```sh
# 在 x86 的機器上，替 ARM 開發板編譯程式
$ gcc -m32 hello.c -o hello32         # 不同位元
$ arm-linux-gnueabi-gcc hello.c -o hello-arm   # 交叉編譯給 ARM
```

```sh
$ ./hello
hello, GNU
hello, GNU
hello, GNU
```

## 相關條目
- [1989-ANSI-C標準C89](1989-ANSI-C標準C89.md)
- [1991-Linux誕生](1991-Linux誕生.md)
- [2005-LLVM與Clang問世](2005-LLVM與Clang問世.md)
