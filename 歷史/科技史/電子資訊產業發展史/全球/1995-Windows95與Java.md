# 1995：Windows 95 與 Java — 網際網路的前夜與跨平台烏托邦

## 案情
1995 年 8 月 24 日午夜，Windows 95 全球開賣，滾石樂團的〈Start Me Up〉成為廣告主題曲，首週銷售破 700 萬套。同年 5 月 23 日，Sun Microsystems 在 SunWorld 會議正式發表 Java 語言，James Gosling 團隊喊出「Write Once, Run Anywhere」。年底，Microsoft 授權 Mosaic 程式碼推出 Internet Explorer 1.0，綁進 Windows 95 Plus! 套件。

## 前因
- Windows 3.1 仍是 16 位元疊在 DOS 上的半吊子系統，Apple Macintosh 的易用性與 GUI 優勢步步進逼。
- Novell 的 NetWare、IBM OS/2 都在爭奪企業桌面，Microsoft 需要一次徹底翻新。
- Sun 以工作站與 SPARC 晶片為生，眼見 PC 侵蝕市場，急需新戰場；Oak 計畫（原為機頂盒開發）技術成熟卻無市場。
- 網際網路在 Mosaic 帶動下爆發性成長，但 Microsoft 一度輕忽，Bill Gates 直到 1995 年 5 月才發出「Internet Tidal Wave」備忘錄，全公司轉向。

## 線索與推理
Windows 95 的偵探視角：Microsoft 賣的不是作業系統，是「平台」。1995 年的關鍵決策是將 IE 免費綁進系統——短期放棄營收，長期壟斷入口。這是典型的兩階段賽局：先以零價格鞏固市占（此時微軟對瀏覽器的投入被形容為「我們要讓 Netscape 的空氣都買不到」），再利用平台地位收取生態稅。Netscape 的悲剧在於它以為瀏覽器是產品，Microsoft 知道它是通路。

Java 的決策邏輯同樣精彩。Sun 看見的敵人不是 Microsoft，而是「作業系統本身的壟斷」。Java 的策略是：在 OS 之上再架一層 JVM 虛擬機器，讓應用程式不再依賴特定 OS。若 JVM 普及，Windows 就只是硬體驅動層，商業價值被架空。Scott McNealy 說「We're not trying to be Microsoft; we're trying to make Microsoft irrelevant」——這句話點破整場棋局。

Microsoft 的反制：1996 年授權 Java 但做「Windows 專屬延伸」，造成 Java 程式在某平台跑不動——分裂標準是壟斷者最便宜的武器。這場糾紛最終以 2001 年 Sun 獲得約 12 億美元和解金落幕。

## 理論
跨平台承諾的經濟學：若有 $m$ 個平台、 $n$ 個應用程式，原生開發需 $m \times n$ 次移植；有了虛擬機器則只需 $m+n$ 次（每平台一個 JVM＋每程式一次編譯）。

$$\text{移植成本}: m \times n \longrightarrow m + n$$

Java 垃圾回收與位元碼驗證提供安全性，是讓下載式程式（Applet）成為可能的技術前提——這正是 1995 年「網路就是電腦」的實踐。

平台壟斷可用雙邊網路效應模型描述：使用者數 $u$ 與開發者數 $d$ 互相增強：

$$\frac{du}{dt} = a\,d, \qquad \frac{dd}{dt} = b\,u$$

其解 $u, d$ 呈指數成長且易引爆正回饋——Windows 95 一夜之間啟動此飛輪，而 Microsoft 綁 IE 正是把飛輪從「桌面」延伸到「網路」的動作，日後成為 1998 年 US v. Microsoft 反壟斷案的核心罪狀。

## 後果
1. Windows 95 確立 Microsoft 在 PC 桌面的絕對霸權，Wintel 聯盟進入全盛期。
2. 瀏覽器大戰開打：IE vs Navigator，Netscape 1998 年被 AOL 收購，並開源出 Mozilla。
3. Java 未能取代 Windows 桌面，卻在伺服器端（J2EE）、Android（Dalvik/ART 源自 Java 語系）與企業軟體長出第二生命。
4. 「網路是平台」的思想由 Netscape 傳給 Google 與 Web 2.0 世代。
5. Microsoft 綁架瀏覽器的策略招致反壟斷訴訟，重創其創新形象，為 2000 年代的 Google 崛起讓路。

## 冷案檔案
- 時間：1995 年 5 月 23 日（Java 發表）；1995 年 8 月 24 日（Windows 95 開賣）；1995 年 8 月（IE 1.0）
- 案由：PC 霸權加冕、跨平台烏托邦宣言、瀏覽器大戰的槍聲在同一年響起
- 歷史定位：1995 年是「桌面時代」的巔峰與「網路時代」的起跑線，兩個世代的權力在此交接
