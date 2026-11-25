# AI-Study-Cards

手機優先的隨身技術記憶卡合集，支援單卡主動回想、題庫全覽、流程總覽、深淺色切換與 `localStorage` 自動進度儲存（可部署至 GitHub Pages，於手機瀏覽器「加入主畫面」離線閱讀）。

## 主題列表

- [index.html](./index.html) — 多主題總目錄與整體熟練度儀表板
- [mcp_mobile_study.html](./mcp_mobile_study.html) — 🔌 MCP 架構與使用（10 題）
- [git_mobile_study.html](./git_mobile_study.html) — 🌿 Git 工作流程（10 題）
- [api_mobile_study.html](./api_mobile_study.html) — 🌐 API 請求與回應流程（10 題）
- [react_mobile_study.html](./react_mobile_study.html) — ⚛️ React 渲染與開發流程（10 題）

## 推送至 GitHub Pages

1. 在 GitHub 建立一個新 Repository（例如 `AI-Study-Cards`）。
2. 在本機終端機執行：
   ```zsh
   git remote add origin https://github.com/<你的帳號>/AI-Study-Cards.git
   git push -u origin main
   ```
3. 到 GitHub Repository 的 **Settings → Pages**，將 Source 設為 **Deploy from a branch**，Branch 選擇 **`main` / `/ (root)`** 並按下 **Save**。
4. 等待約 1 分鐘即可透過 `https://<你的帳號>.github.io/AI-Study-Cards/` 在手機上直接開啟閱讀。
