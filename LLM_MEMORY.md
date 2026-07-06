# LLM_MEMORY.md — 工作記憶(agent 讀寫;規則見 AGENTS.md,勿在此重複)

## A. 目前狀態(每次交接必更新)

- 目前階段: build
- 最後更新: 2026-07-06 / 當時階段: build
- 最新 commit: 87dcbb5 [takeover] WIP: 接手時發現未提交變更
- 進行中任務: 測試中
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
