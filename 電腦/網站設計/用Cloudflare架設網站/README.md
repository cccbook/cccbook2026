# 用 Cloudflare 架設網站：從零開發到全球上線

本書以「邊做邊學」的方式，帶領讀者使用 **Cloudflare 的全套服務**（Pages、Workers、D1、R2、KV、Durable Objects、Tunnel 等）建構、部署並上線一個現代化的網站。從購買網域、撰寫程式，一直到安全防護、效能最佳化與監控，完成一條完整的「開發 → 部署 → 上線 → 營運」流程。

本書延續本 series「理論驅動實務」的風格：每項服務都會先說明它背後的問題與原理（例如 CDN 快取、邊緣運算、Edge Worker 的隔離模型），再進入實際操作，讓讀者知其然也知其所以然。

## 本書特色

- **免費入門**：Cloudflare 免費方案即可完成書中絕大多數實作，不必先花錢
- **全棧單平台**：前端靜態頁 + 後端 API + 資料庫 + 檔案儲存 + 安全防護，全部在同一平台完成
- **真實專案貫穿**：以一個「部落格 + 留言板 + 檔案下載」網站貫穿全書，逐步演化
- **涵蓋上線全流程**：網域、DNS、HTTPS、CI/CD、自訂網域、監控、防駭，一章章疊上去

## 目錄

* 第1章-導論：網站為何要放上邊緣
    * [1.1-從自有伺服器到邊緣運算：網站託管的六十年演進](01.1-從自有伺服器到邊緣運算：網站託管的六十年演進.md)
    * [1.2-Cloudflare 是什麼：CDN、DNS 與全球網路的原理](01.2-Cloudflare是什麼：CDN、DNS與全球網路的原理.md)
    * [1.3-Cloudflare 服務全景：Pages、Workers、D1、R2 對比傳統 LAMP / VPS](01.3-Cloudflare服務全景.md)
    * [1.4-註冊帳號與第一個網站：三分鐘上線 Hello World](01.4-註冊帳號與第一個網站：三分鐘上線HelloWorld.md)

* 第2章-網域與 DNS：網站的門牌與地址簿
    * [2.1-DNS 原理：遞迴查詢、TTL 與全球分散式資料庫](02.1-DNS原理：遞迴查詢、TTL與全球分散式資料庫.md)
    * [2.2-購買與託管網域：Cloudflare Registrar 與 DNS 設定實務](02.2-購買與託管網域：CloudflareRegistrar與DNS設定實務.md)
    * [2.3-DDNS 與內網穿透：多線路動態 IP 與 NAT 環境下的解法](02.3-DDNS與內網穿透：多線路動態IP與NAT環境下的解法.md)
    * [2.4-HTTPS 與邊緣憑證：從 ACME 到 Cloudflare 的一鍵加密](02.4-HTTPS與邊緣憑證：從ACME到Cloudflare的一鍵加密.md)

* 第3章-Pages：靜態網站的正確起點
    * [3.1-Jamstack 與靜態優先架構：為什麼快取是最好的後端](03.1-Jamstack與靜態優先架構.md)
    * [3.2-建立前端專案：HTML/CSS/JavaScript 到 Astro / React / Vue 首選框架](03.2-建立前端專案.md)
    * [3.3-部署 Pages：Git 整合、自動 CI 與自訂網域上線](03.3-部署Pages：Git整合、自動CI與自訂網域上線.md)
    * [3.4-快取與版本管理：丟棄部署、Headers 設定與預覽環境](03.4-快取與版本管理.md)

* 第4章-Workers：把後端寫在邊緣
    * [4.1-從客戶請求到邊緣節點：V8 Isolate 與冷啟動歸零的原理](04.1-V8Isolate與冷啟動歸零的原理.md)
    * [4.2-第一支 Worker：路由、Fetch Handler 與環境變數](04.2-第一支Worker：路由、FetchHandler與環境變數.md)
    * [4.3-Wrangler CLI：本地開發、測試與部署流程](04.3-WranglerCLI：本地開發、測試與部署流程.md)
    * [4.4-Pages Functions：檔案式路由與全棧（Full-Stack）頁面](04.4-PagesFunctions：檔案式路由與全棧頁面.md)

* 第5章-資料儲存：D1、KV、R2 與 Durable Objects
    * [5.1-邊緣資料儲存的取捨：一致性、延遲與複製](05.1-邊緣資料儲存的取捨.md)
    * [5.2-D1：SQLite 在邊緣上跑 SQL，部落格文章的儲存](05.2-D1：SQLite在邊緣上跑SQL.md)
    * [5.3-KV 與 R2：鍵值快取與物件儲存，留言板與檔案下載](05.3-KV與R2：鍵值快取與物件儲存.md)
    * [5.4-Durable Objects：強一致性的有狀態邊緣，線上人數計數器](05.4-DurableObjects：強一致性的有狀態邊緣.md)

* 第6章-實戰專案：打造部落格 + 留言板 + 檔案下載網站
    * [6.1-專案規劃：架構圖、資料模型與 API 設計](06.1-專案規劃：架構圖、資料模型與API設計.md)
    * [6.2-前端實作：Astro/React 頁面、版型與互動](06.2-前端實作.md)
    * [6.3-後端實作：Functions API、D1 資料存取與 R2 檔案](06.3-後端實作.md)
    * [6.4-上線：自訂域名、HTTPS、CI/CD 與回滾策略](06.4-上線：自訂域名、HTTPS、CI-CD與回滾策略.md)

* 第7章-進階後端：認證、排程與 WebSocket
    * [7.1-使用者的註冊與登入：Session、Cookie 與 Turnstile 驗證](07.1-使用者的註冊與登入.md)
    * [7.2-排程任務：Cron Triggers 與定時抓取](07.2-排程任務：CronTriggers與定時抓取.md)
    * [7.3-WebSocket 與 Durable Objects：即時通知與協作](07.3-WebSocket與DurableObjects：即時通知與協作.md)
    * [7.4-Worker 相互呼叫、Service Bindings 與 Queue](07.4-ServiceBindings與Queue.md)

* 第8章-上線之後：監控、效能與安全防護
    * [8.1-Workers Observability 與 Logpush：看見你的邊緣流量](08.1-WorkersObservability與Logpush.md)
    * [8.2-快取策略精修：Cache Rules、stale-while-revalidate 與開發者預覽](08.2-快取策略精修.md)
    * [8.3-安全防護：WAF、Rate Limiting、Turnstile、Bot 對抗實務](08.3-安全防護：WAF、RateLimiting、Turnstile.md)
    * [8.4-成本模型分析：免費方案能撐多久？何時該升級？](08.4-成本模型分析.md)

* 第9章-自架伺服器的混合架構：Tunnel 與 Zero Trust
    * [9.1-為什麼還要自架：資料庫、GPU 與把他雲服務塞進 Cloudflare 後面](09.1-為什麼還要自架.md)
    * [9.2-Cloudflare Tunnel：不需要公開 IP 與開 Port 的反向連線原理](09.2-CloudflareTunnel：不需要公開IP與開Port的架設.md)
    * [9.3-Zero Trust Access：把內部服務藏在身分驗證之後](09.3-ZeroTrustAccess：把內部服務藏在身分驗證之後.md)
    * [9.4-Load Balancing 與多線路出海：多來源、健康檢查與地理路由](09.4-LoadBalancing與多線路出海.md)

* 第10章-結語：從入門到生產級的檢查清單
    * [10.1-上線前檢查清單：安全、監控、備份與災難復原](10.1-上線前檢查清單.md)
    * [10.2-治理與擴展：IaC、多環境與團隊協作](10.2-治理與擴展：IaC、多環境與團隊協作.md)
    * [10.3-Cloudflare 之外：對比其他邊緣平台與未來展望](10.3-Cloudflare之外：對比其他邊緣平台與未來展望.md)

## 閱讀方式

- 章節有前後依賴，建議按順序閱讀；第 6 章是全書高潮（實戰上線一個真實網站）
- 每章開頭有「本章目標」、結尾有「小結與練習」
- 所有程式碼以 TypeScript 為主（教材在 `code/` 資料夾，逐步建立）
- 若只想快速上線一個靜態網站：讀第 1、3、2.4 節即可

## 需要的背景知識

- 基本的 HTML / CSS / JavaScript 概念
- 使用過命令列與 Git
- 不需要任何雲端或後端經驗

---

如需調整章節內容、增刪主題（例如加 3D、AI Workers、影像最佳化 Cloudflare Images、Stream 等），請告訴我。
