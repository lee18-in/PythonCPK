# LLM_MEMORY.md — 工作記憶(agent 讀寫;規則見 AGENTS.md,勿在此重複)

## A. 目前狀態(每次交接必更新)

- 目前階段: build
- 最後更新: 2026-07-26 / 當時階段: build（CI 打包流程補手動觸發）
- 最新 commit: a4aeac2 [build] 記錄 auto push 操作
- 進行中任務: 等待新 session/新工具審閱本次 package.yml 異動
- 阻塞點: 目前無

## B. 規劃(規劃階段 [plan] 專屬區;狀態: 草稿 | 已定案)

### B1. 架構決策(已定案後鎖定,建置/維運階段不得改)

| # | 決策 | 理由 | 狀態 |
|---|------|------|------|

### B2. 短期目標(本週)

- [ 測試是否正常 ]

### B3. 中期目標(本月)

- [ ]

### B4. 長期目標

- [ ]

## C. 交接日誌(只追加,不刪改;最新在最上,每筆一個小節)

### 2026-07-26 [build] 使用工具: Claude Code

- 完成了什麼: 使用者要求「用 GitHub Action 自動編譯 Windows exe 與 Linux AppImage」。查證後發現此功能早已存在且實測成功——`.github/workflows/package.yml`（commit b2f6b5a 建立、fd405b3 修 YAML），Release v1.0.1（2026-06-17）由 github-actions[bot] 發佈，`PythonCPK.exe` 與 `PythonCPK-x86_64.AppImage` 兩個 asset 都在。故本次未重做，只補唯一缺口：原本僅 `push tag v*` 可觸發，無法在不發版的情況下試打包。改動三處：(1) 新增 `workflow_dispatch` 觸發器；(2) 兩個 job 各加 `actions/upload-artifact@v4`（`if-no-files-found: error`），讓手動觸發也能取得產物；(3) 兩個 `softprops/action-gh-release@v2` 步驟加上 `if: startsWith(github.ref, 'refs/tags/')`——因為手動觸發時 `github.ref_name` 是分支名而非 tag，不 guard 會建出以分支名為 tag 的錯誤 Release。驗證：以 pyyaml `safe_load` 解析成功，確認 triggers 為 `['push', 'workflow_dispatch']`、兩個 release 步驟都帶上 if 條件、upload-artifact 無 if 條件（永遠執行）。未實際跑過 CI（需 push 才能驗證）。
- 下一個 agent 該做什麼: 本次改動需要審閱：(1) `git diff a4aeac2 -- .github/workflows/package.yml` 確認只動了上述三處，沒碰到既有已驗證可用的 PyInstaller / AppImage 打包邏輯；(2) 核對 `startsWith(github.ref, 'refs/tags/')` guard 是否確實蓋住兩個 job 的 release 步驟，避免手動觸發污染 Releases；(3) 確認兩個 upload-artifact 的 `path` 與各自 job 實際產物路徑相符（Windows: `dist/PythonCPK.exe`；Linux: 工作目錄根的 `PythonCPK-x86_64.AppImage`）；(4) 審閱通過後，若使用者同意 push，可在 GitHub Actions 頁面手動 Run workflow 做一次真實驗證。
- 地雷警告: 尚未 push，遠端仍是舊版 workflow；手動觸發功能要 push 到 main 後才會出現在 Actions UI。AppImage 的 fallback 圖示依賴 PIL，目前是靠 matplotlib 間接帶進 Pillow，requirements.txt 未直接列出，若日後移除 matplotlib 會壞。

### 2026-07-06 auto push [build] 使用工具: Claude Code

- 完成了什麼: 推送 4 個已提交的 commit 至 origin/main (7ca4b86..7b6d112)
- 下一個 agent 該做什麼: 無
- 地雷警告: 無

### 2026-07-06 [plan] 使用工具: Claude Code

- 完成了什麼: 執行 Playbook v2 分支 B（現有專案防禦導入），覆蓋 AGENTS.md 為模板版本（含 Playbook-Version: 2 標記），LLM_MEMORY.md E 區確認完整（建置指令、測試指令、程式碼慣例已填）。
- 下一個 agent 該做什麼: 無
- 地雷警告: 無

### 2026-07-06 接手時發現未提交變更 [build] 使用工具: Claude Code

- 完成了什麼: 接手時工作樹不乾淨，LLM_MEMORY.md E 區已補充，但未 commit
- 下一個 agent 該做什麼: 無
- 地雷警告: ⚠️ 前一個 agent 未遵守 AGENTS.md §2 的交接協定（應在切換前 commit）

<!-- 範例格式,新條目複製此結構插入在本註解下方:

### 2026-07-05 21:07 [build] 使用工具: Antigravity

- 完成了什麼: 導入 AI agent 工作流初始檔案 (AGENTS.md, LLM_MEMORY.md, CLAUDE.md, GEMINI.md)
- 下一個 agent 該做什麼: 請使用者補充「進行中任務」與「阻塞點」
- 地雷警告: 無
-->

## D. 已封存結論(自〈總結封存〉搬入,唯讀)

## E. 專案技術脈絡(依專案填寫,agent 得隨專案實況更新,保持精簡)

- 建置指令: `python app.py` (啟動 PyQt6 GUI 分析工具)
- 測試指令: 無特定自動化測試指令（手動 GUI 測試）
- 程式碼慣例: Python 3.8+ / PyQt6 / Numpy / Pandas / Scipy / Matplotlib / Seaborn (PEP8)
