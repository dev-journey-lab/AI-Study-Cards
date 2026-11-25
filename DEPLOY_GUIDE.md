# AI-Study-Cards 私密同步與 Git 操作說明

本文件記錄 `/Users/dev/AI-Study-Cards` 的實際建置狀態、iCloud 雲碟私密同步方式、Git SSH（`github-personal`）推送流程，以及未來若要部署至私密網頁（Cloudflare Pages + Access）的完整步驟。

---

## 一、目前已完成項目總覽

1. **四套手機版隨身記憶卡 + 多主題總目錄**（共 40 題，進度自動存於瀏覽器 `localStorage`）：
   - `index.html`：多主題總目錄與整體熟練度儀表板
   - `mcp_mobile_study.html`：🔌 MCP 架構與使用（10 題）
   - `git_mobile_study.html`：🌿 Git 工作流程（10 題）
   - `api_mobile_study.html`：🌐 API 請求與回應流程（10 題）
   - `react_mobile_study.html`：⚛️ React 渲染與開發流程（10 題）
2. **已同步至 iCloud 雲碟（100% 個人私密）**：
   - 目標路徑：`/Users/dev/Library/Mobile Documents/com~apple~CloudDocs/AI-Study-Cards/`
   - 僅複製 `.html` 檔（不含 `.git`），不會佔用多餘空間或造成版本衝突。
3. **本機 Git 初始化與 SSH 遠端綁定**：
   - 分支：`main`
   - 遠端 `origin`：`git@github-personal:dev-journey-lab/AI-Study-Cards.git`
   - 使用本機 `~/.ssh/config` 中已設定好的 `github-personal`（金鑰 `~/.ssh/id_ed25519_github_personal`），推送時不需輸入帳密。

---

## 二、如何在手機私密閱讀（iCloud 雲碟）

1. 在 iPhone 打開內建 **「檔案（Files）」App**。
2. 點進 **iCloud 雲碟 → `AI-Study-Cards`**。
3. 直接點擊想複習的主題檔案（例如 `git_mobile_study.html`、`api_mobile_study.html`、`react_mobile_study.html`、`mcp_mobile_study.html`）即可開始閱讀。
4. 在 Mac 上則可直接雙擊 `index.html` 用 Safari / Chrome 打開完整總目錄。

### 未來新增或修改學習卡後，如何再次同步到 iCloud？
在 Mac 終端機執行這一行即可覆蓋更新 iCloud 雲碟中的最新版本：

```zsh
cp /Users/dev/AI-Study-Cards/*.html "$HOME/Library/Mobile Documents/com~apple~CloudDocs/AI-Study-Cards/"
```

---

## 三、如何推送到 GitHub Private（私密）儲存庫

因為本機沒有安裝 `gh` CLI，首次需先在 GitHub 網頁建立空的私密儲存庫（只需做一次）：

1. 打開 [https://github.com/new](https://github.com/new)
2. **Repository name** 輸入：`AI-Study-Cards`
3. 權限選擇：**Private（私密）**（確保只有你自己看得到）
4. 下方 README / `.gitignore` / License 皆**不要勾選**，按 **Create repository**。
5. 回到 Mac 終端機執行推送（`origin` 已幫你綁好 SSH `github-personal`）：

```zsh
cd /Users/dev/AI-Study-Cards
git push -u origin main
```

### 日常修改後的標準 Git 更新流程
每次新增題目或主題後，照這 3 步備份到 GitHub Private Repo：

```zsh
cd /Users/dev/AI-Study-Cards
git add .
git commit -m "feat: add new study cards"
git push
```

---

## 四、進階選配：想要「手機 Safari 私密網址 + 加入主畫面」

如果未來除了 iCloud 雲碟外，也想用「專屬網址」在手機 Safari 打開並保留跨頁進度，但依然維持 **100% 私密**：

1. 確認 GitHub 的 `dev-journey-lab/AI-Study-Cards` 為 **Private** 且已完成 `git push`。
2. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Workers & Pages → Create → Pages → Connect to Git**。
3. 選擇 `dev-journey-lab/AI-Study-Cards`（Build command 留空、Output directory 填 `/`）完成部署。
4. 在該 Pages 專案開啟 **Cloudflare Zero Trust → Access**，新增規則「僅允許你自己的 Email 收取一次性驗證碼登入」，即可擁有 100% 私密且支援 Safari 加入主畫面的學習卡網站。
