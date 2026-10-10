# A.5 GitHub Actions：自動化 CI/CD 入門

## 什麼是 CI/CD

在團隊開發中，每次有人提交程式碼，我們都需要確認：程式碼能不能正常編譯？測試是否全部通過？是否符合風格規範？如果這些工作都靠人工執行，不僅耗時，還容易出錯。

**CI/CD** 是兩種自動化實踐的統稱：

- **CI（Continuous Integration，持續整合）**：每次提交或合併後，自動執行建構和測試，確保主線程式碼的品質。
- **CD（Continuous Delivery/Deployment，持續交付/部署）**：在 CI 通過後，自動將程式碼部署到測試或正式環境。

**GitHub Actions** 是 GitHub 內建的 CI/CD 服務。它允許你定義自動化的工作流程（workflow），在特定事件（如推送、Pull Request）觸發時自動執行。而且它對公開版倉免費，私有版倉也有一定的免費額度。

## 第一個 GitHub Actions 工作流程

GitHub Actions 的設定檔放在版倉的 `.github/workflows/` 目錄下，使用 YAML 格式。以下是一個最基本的範例：

```yaml
# .github/workflows/hello.yml
name: Hello World

on:
  push:
    branches: [main]

jobs:
  say-hello:
    runs-on: ubuntu-latest
    steps:
      - name: 列出目錄
        run: ls -la
      - name: 印出訊息
        run: echo "Hello from GitHub Actions!"
```

將這個檔案提交並推送到 GitHub，你就會在版倉的「Actions」分頁中看到工作流程被觸發了。

## 解讀 workflow 檔案

一個 workflow 檔案由幾個主要區塊組成：

**name**：工作流程的名稱，顯示在 GitHub Actions 介面上。

**on**：觸發條件。上面的例子設定為當有人推送到 `main` 分支時觸發。常見的觸發事件包括：

- `push`：推送提交時
- `pull_request`：建立或更新 Pull Request 時
- `schedule`：定時觸發（例如每天凌晨兩點）
- `workflow_dispatch`：手動觸發

**jobs**：定義要執行的工作。一個 workflow 可以包含多個 job，每個 job 在不同的執行環境（runner）中運行。

**runs-on**：指定執行環境。`ubuntu-latest` 是最常用的，也可以使用 `windows-latest` 或 `macos-latest`。

**steps**：job 中的每一個步驟。可以是執行 shell 指令（`run`），或是使用別人寫好的現成動作（`uses`）。

## 實作：自動執行 Python 測試

假設你的專案使用 Python 和 pytest，以下是自動執行測試的 workflow：

```yaml
# .github/workflows/test.yml
name: Run Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - name: Checkout 程式碼
        uses: actions/checkout@v4

      - name: 設定 Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: 安裝相依套件
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: 執行測試
        run: pytest --verbose
```

這個 workflow 做了以下事情：

1. 在 Python 3.10、3.11、3.12 三個版本上分別執行測試（**矩陣策略**）。
2. 使用 `actions/checkout` 動作將程式碼取出。
3. 使用 `actions/setup-python` 安裝指定版本的 Python。
4. 安裝專案的相依套件。
5. 執行 pytest。

`actions/checkout@v4` 和 `actions/setup-python@v5` 是社群維護的現成動作，`@v4` 和 `@v5` 是版本號，用來確保穩定性。

## 實作：程式碼風格檢查

除了測試，你還可以用 GitHub Actions 自動檢查程式碼風格。以下是一個使用 `flake8` 檢查 Python 程式碼的範例：

```yaml
# .github/workflows/lint.yml
name: Lint

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: 安裝 flake8
        run: pip install flake8

      - name: 執行程式碼風格檢查
        run: flake8 src/ --max-line-length=120
```

## 實作：自動部署到 GitHub Pages

如果你有一個靜態網站（例如用 Jekyll 或 MkDocs 製作），可以設定每次推送到 `main` 時自動部署到 GitHub Pages：

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 設定 GitHub Pages
        uses: actions/configure-pages@v4

      - name: 建構靜態網站
        run: |
          pip install mkdocs-material
          mkdocs build

      - name: 部署到 GitHub Pages
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/

      - name: 發布到 GitHub Pages
        uses: actions/deploy-pages@v4
```

## 自訂動作的 reusable 特性

GitHub Actions 最強大的地方在於它的**生態系**。GitHub Marketplace 上有數萬個現成的動作（action），涵蓋了幾乎所有常見的需求。例如：

- 上傳Coverage 報告到 Codecov
- 自動產生 Changelog
- 部署到 AWS、GCP、Azure 等雲端平台
- 自動發布 npm 或 PyPI 套件

你也可以將自己的 workflow 封裝成可重用的動作，讓多個專案共享。

## Workflow 的最佳實踐

- **命名清晰**：workflow 名稱應反映其用途，如 `Run Tests` 而非 `CI`。
- **善用快取**：使用 `actions/cache` 快取相依套件，加速後續執行。
- **分離環境**：測試、部署等不同階段應分開成不同的 workflow。
- **保密管理**：敏感資訊（如 API 金鑰）應使用 GitHub Secrets，絕對不要寫在程式碼中。

```yaml
# 使用 GitHub Secrets 中的環境變數
- name: 部署
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh
```

在版倉的「Settings > Secrets and variables > Actions」中可以新增 Secrets。

## 想一想

1. 如果你的 workflow 執行一次需要 20 分鐘，你會如何優化它來縮短等待時間？
2. 為什麼 GitHub Actions 的 Secrets 不能在 workflow 檔案中直接寫出來？如果洩露了會有什麼後果？
3. 除了程式碼測試和部署，你還能想到 GitHub Actions 可以用來自動化哪些工作？

## 本章小結

本章介紹了 CI/CD 的基本概念，以及如何使用 GitHub Actions 實作自動化工作流程。我們從最簡單的「Hello World」開始，逐步實作了自動測試（含矩陣策略）、程式碼風格檢查，以及靜態網站部署。GitHub Actions 讓你不用花時間在重複性的建構和部署工作上，而是專注在寫出更好的程式碼。下一章將回到 Git 本身，學習 rebase、cherry-pick、bisect 等進階操作。
