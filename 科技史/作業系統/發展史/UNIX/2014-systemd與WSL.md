# 2014 - systemd 與 WSL（init 之戰與 Unix 的全面相容）

## 案件摘要
2014 年，兩件大事代表 Unix 的現代演進：
1. **systemd** 成為主流 Linux 發行版的 init 系統（Debian 8、RHEL 7、Ubuntu 15.04）——init 系統 30 年來的最大革命。
2. Microsoft 發布 **WSL（Windows Subsystem for Linux）**——Windows 第一次內建**真正的 Linux 系統呼叫層**。
$$\text{systemd（init 革命）} \;+\; \text{WSL（Unix 全面相容）} = \text{Unix 思想的完全勝利}.$$

## 前因 -- 為什麼會有這個案子
- **SysV init 的缺陷**：1970 年代以來的 init（執行等級 + 序列啟動腳本）——**序列啟動慢**（大伺服器開機數分鐘）、**不監督服務**（服務當掉無人知）、**無依賴管理**（腳本編號硬编码 S01、S02）。
- **systemd 的動機**：Lennart Poettering（2010 年起開發）主張 init 應該：**並行啟動**、**socket 激活**（先建 socket 再啟服務，消除依賴順序）、**cgroups 監督**——把 2013 年的容器技術（cgroups）用於服務管理。
- **WSL 的動機**：開發者要在 Windows 上用 Unix 工具鏈（grep、ssh、gcc）——**彌補的缺陷：Windows 無 POSIX 層**。舊法是 Cygwin（1995，模擬層，慢）；WSL 1（2016 實際發布，系統呼叫轉譯）、WSL 2（2019，真 Linux 核心虛擬機）。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：並行啟動與依賴圖
$$\text{SysV init：} \; S_{01} \to S_{02} \to \cdots \to S_{99} \quad (\text{序列，} O(n))$$
$$\text{systemd：} \; \text{依賴圖 + 拓撲排序} \quad (\text{並行，無依賴者同時啟動})$$
- **彌補的缺陷**：序列啟動的 O(n) 等待；systemd 把啟動時間從分鐘級降到秒級。

### 第二條線索：socket 激活（socket activation）
$$\text{先建 socket（常駐）} \;\xrightarrow{\text{第一個連線}}\; \text{才啟動服務行程}.$$
- **理論基礎**：把「依賴」變成「排隊」——服務 A 不用等服務 B 起來，只要 B 的 socket 已在排隊——**依賴順序問題的數學消解**。
- **彌補的缺陷**：服務啟動順序的脆弱性（B 沒起來 A 就失敗）。

### 第三條線索：cgroups 監督
- **彌補的缺陷**：SysV init 無法追蹤服務的子行程（孤兒行程問題）——systemd 用 cgroups 把「服務 = 一群行程」的形式化，當掉就重啟。

### systemd 單元檔範例

```ini
# /etc/systemd/system/webapp.service
[Unit]
Description=My Web App
After=network.target

[Service]
ExecStart=/usr/bin/python3 /app/app.py
Restart=always              # 當掉自動重啟
MemoryMax=500M              # cgroups 資源限制

[Install]
WantedBy=multi-user.target
```

### Shell 範例：systemd vs SysV init

```bash
# 舊法（SysV init）：序列、脆弱
$ /etc/init.d/nginx start

# systemd：並行、監督、依賴管理
$ systemctl start nginx
$ systemctl status nginx
● nginx.service - A high performance web server
   Active: active (running) since ...
$ systemctl list-units --failed   # 找出當掉的服務
```

### Shell 範例：WSL——Windows 上的 Unix

```powershell
# WSL：Windows 內建 Linux（2016/2019）
PS> wsl --install -d Ubuntu
PS> wsl
$ grep -r "TODO" . | wc -l     # 真正的 Unix 工具鏈
$ sudo apt install gcc         # 完整的套件管理
```

## 結案 -- 後果與影響
- **systemd 的爭議**：Unix 哲學派批評 systemd「太龐大」（Do one thing well 的違背）——但並行啟動與 cgroups 監督的實用性贏得多數發行版。
- **WSL 的意義**：**Unix 工具鏈的完全勝利**——連微軟都要擁抱 Linux；2020 年代開發者環境的主流是「Windows + WSL + Docker」。
- **init 的歷史總結**：1969 年 Unix 的 init（一行 shell）→ SysV init（腳本）→ systemd（宣告式單元檔）——**從命令式到宣告式**的軟體工程大趨勢。
- 歷史教訓：**基礎服務（init）50 年不變，一旦改變就是革命**——systemd 證明「最老的元件」往往是最需要現代化的。

## 關鍵人物與文獻
- **L. Poettering**：systemd (2010–)、socket activation。
- **Microsoft**：WSL (2016/2019)。
- 相關案件：`1983-SystemV與GNU計畫.md`、`2013-Docker容器.md`。
