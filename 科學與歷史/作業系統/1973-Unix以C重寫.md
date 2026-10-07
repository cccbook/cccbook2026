# 1973 - Unix 以 C 語言重寫（作業系統第一次可移植）

## 案件摘要
1973 年，Dennis Ritchie 把 Unix 從 PDP-11 組合語言**重寫為 C 語言**——
作業系統史上第一次，核心程式碼與特定機器**解耦**：
$$\text{原始碼} + \text{編譯器} \quad\Longrightarrow\quad \text{任何機器上的 Unix}.$$
Unix 從「一台機器的系統」變成「一族機器的系統」——**可移植性**的誕生，
C 語言從此成為系統軟體的通用語言。

## 前因 -- 為什麼會有這個案子
- **組合語言的牢籠**：1969 年的 Unix 用 PDP-7 組合語言寫成——換機器（如新到的 PDP-11）就要**全部重寫**。Thompson 已被迫重寫一次。
- **BCPL/B 的先驅線索**：Ritchie 從 BCPL（Richards, 1966）發展出 B 語言（無型別），再演化為 **NB（New B）→ C（1972）**——加入型別（int、char、指標）與結構，使它夠強大又能編譯成高效程式碼。
- **PDP-11 的契機**：1970 年 Bell 實驗室買入 PDP-11——Thompson 先用組合語言移植，但深知不可持續。
- **Ritchie 的偵探直覺**：與其每次重寫，不如**把核心寫在高階語言**——「作業系統必須用組合語言」的教條當場陣亡。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：可移植性的數學
設移植成本：組合語言版 = $c_{\text{asm}}$（幾乎等於重寫），C 版 = $c_{\text{port}}$（只改機器相依部分）：
$$c_{\text{port}} = c_{\text{machine-dependent}} \ll c_{\text{asm}}.$$
核心的機器相依部分被隔離到極少數檔案（組合語言起動碼、MMU 設定）——**其餘 95% 不用動**：
$$N \text{ 台機器: } c_{\text{asm}} \times N \quad \text{vs} \quad c_{\text{port}} \times N + c_{\text{port}}.$$

### 第二條線索：C 語言的設計抉擇
Ritchie 的關鍵取捨——**「可移植的組合語言」**：
1. **低階控制**：指標、位元運算——能寫驅動程式與 MMU。
2. **高階抽象**：函式、結構、型別——能寫大型系統。
3. **極小核心**：C 只有 32 個關鍵字——編譯器容易移植到新機器。
$$\text{C 編譯器可移植} \;\Longrightarrow\; \text{Unix 可移植} \;\Longrightarrow\; \text{生態系自我擴張}.$$
**語言與系統互相成就**——C 為 Unix 而生，Unix 為 C 而擴散。

### 第三條線索：1973 年的驗證——C 版 Unix 性能不輸組合語言
Ritchie 與 Thompson 重寫的 C 版核心，性能與組合語言版相當——
「高階語言太慢」的教條被正式謀殺。1974 年論文發表於 CACM：
$$\text{C 版 Unix 性能} \approx \text{組合語言版} \quad \text{（差距 < 20–30%）}.$$

### C 語言重寫核心的縮影

```c
#include <unistd.h>
#include <fcntl.h>

/* Unix 核心系統呼叫的 C 介面 —— 機器無關 */
int copy_file(const char *src, const char *dst) {
    char buf[512];
    int in  = open(src, O_RDONLY);          /* 一切皆檔案 */
    int out = open(dst, O_WRONLY | O_CREAT, 0644);
    int n;
    while ((n = read(in, buf, sizeof buf)) > 0)
        write(out, buf, n);
    close(in); close(out);
    return 0;
}
```
（1973 年的 C 版核心正是這種風格——**同一份程式碼，任何 Unix 機器都能編譯執行**。）

```python
# 驗證：同一份 C 原始碼在多平台編譯（macOS / Linux）
import subprocess
open("/tmp/copy_demo.c","w").write(r'''
#include <unistd.h>
#include <fcntl.h>
int main(){char b[8];int i=open("/etc/hostname",O_RDONLY);
int o=open("/tmp/h.out",O_WRONLY|O_CREAT,0644);
int n;while((n=read(i,b,8))>0)write(o,b,n);return 0;}
''')
r = subprocess.run(["cc","/tmp/copy_demo.c","-o","/tmp/copy_demo"])
print("編譯成功" if r.returncode == 0 else "編譯失敗")
```

## 結案 -- 後果與影響
- **Unix 的全面擴散**：可移植性使 Unix 跑上 DEC、HP、Sun、SGI 等數十種機器——**工作站時代的統一系統**。
- **C 語言統治系統軟體**：Linux 核心（1991）、Windows NT 核心、Git（2005）、SQLite——**50 年後 C 仍是系統語言之王**。
- **「高階語言寫系統」的範式**：之後每一代都重演——C++、Objective-C、Go（Thompson 参与）、Rust——**1973 年的破案是所有後繼者的祖先**。
- **軟體資產的保值**：架構/實作分離（1964，見「1964-System360與OS360.md」）+ 源碼可移植——軟體第一次成為**可攜帶的資產**。
- 歷史教訓：**把系統從「機器的財產」變成「語言的財產」，是可移植性的本質**——Ritchie 的 C 是這場解耦的兇器，1983 年圖靈獎實至名歸。

## 關鍵人物與文獻
- **D. M. Ritchie**：〈The Development of the C Language〉(1993)；C 語言 (1972)。
- **D. M. Ritchie & K. Thompson**：〈The UNIX Time-Sharing System〉, CACM 17, 365 (1974)。
- 相關案件：`1969-Unix誕生.md`、`1964-System360與OS360.md`、`1991-Linux誕生.md`。
