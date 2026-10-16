# 1992：POSIX.2 Shell 標準化

## 事件
1992 年，IEEE 發佈 **POSIX.2**（IEEE Std 1003.2）——以 **Bourne Shell（sh）為藍本**的 shell 與工具標準，正式把 shell 腳本語言規範化。這是 shell script 首次成為「標準語言」而非「某個 UNIX 版本的方言」。

## 標準化內容與其理論、實用原因

### 1. 以 Bourne Shell 為藍本的 shell 命令語言（sh）
- **理論原因**：Bourne Shell 是部署最廣、語法最穩定的 shell；ksh（1983）證明其可擴充性。
- **實用原因**：企業腳本投資必須保護——標準語法讓腳本可以在任何 POSIX 系統執行。
- **彌補缺陷**：csh/tcsh 與 sh 語法不相容、各 UNIX 版本 shell 方言叢生的可移植性災難。
- **標準化範圍**：變數、`if/for/while/case`、函數、here-doc、重導向、`test`/`[`、萬用字元。

### 2. 排除 csh 語法
- **理論原因**：csh 的運算式解析與重導向缺陷已被社群公認（*csh Programming Considered Harmful*）。
- **實用原因**：單一標準勝過兩個標準。

### 3. `command`、`getopts` 等標準內建
- **實用原因**：`getopts` 提供標準的選項解析（取代各家自行手寫的 `while case` 解析）；`command` 呼叫「真正的命令」而非同名函數/別名。
- **彌補缺陷**：選項解析程式碼在各腳本中重複且易錯。

### 4. 行程模型與信號標準化（`trap`、`kill` 語意）
- **實用原因**：腳本的清理與中斷處理跨平台一致。

## 程式範例：POSIX 標準腳本

```sh
#!/bin/sh
# POSIX.2 標準語法：跨平台可移植
# 變數、條件、迴圈、函數、case、getopts
```

```sh
# getopts：標準的選項解析（取代各家手寫的 while case）
while getopts "ab:f:" opt; do
  case "$opt" in
    a) all=1 ;;
    b) backup="$OPTARG" ;;
    f) file="$OPTARG" ;;
    *) echo "用法: $0 [-a] [-b 備份目錄] [-f 檔案]"; exit 1 ;;
  esac
done
shift $((OPTIND - 1))
```

```sh
# command：呼叫「真正的命令」而非同名函數/別名
ls() { echo "我的 ls"; }
command ls        # 執行真正的 ls，不是上面的函數
```

```sh
# trap：信號處理標準化（清理與中斷處理跨平台一致）
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT INT TERM
```

```sh
# 可移植性對比：POSIX vs bash 方言
# 這行是 POSIX（處處可跑）：
[ -f "$1" ] && echo ok
# 這行是 bash（4.0+ 關聯陣列，dash 會報錯）：
# declare -A map; map[k]=v
```

## 歷史意義
POSIX.2 直接決定了之後 30 年的 shell 生態格局：
- **bash**（1988）誕生時就以 POSIX 相容為目標，之後 `--posix` 模式更嚴格遵循。
- **dash**（Debian ash，1997）追求「最小 POSIX 實作」，成為 Debian/Ubuntu 的 `/bin/sh`（2006 年起），啟動腳本因此大幅加速。
- **busybox ash** 讓嵌入式 Linux 有微小的 POSIX shell。

「寫 POSIX 腳本還是 bash 腳本」成為至今仍在的工程決策：POSIX 換取可移植性，bash 換取語法表達力。

## 彌補了什麼缺陷
彌補了「各 UNIX 版本 shell 方言叢生、腳本不可移植」的核心缺陷，讓 shell script 正式成為標準化的腳本語言。

## 相關條目
- [1977-BourneShell-sh問世](1977-BourneShell-sh問世.md)
- [1988-Bash誕生](1988-Bash誕生.md)
- [1991-Linux問世](1991-Linux問世.md)
