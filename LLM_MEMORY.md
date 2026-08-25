# LLM_MEMORY.md — 工作記憶(agent 讀寫;規則見 AGENTS.md,勿在此重複)

## A. 目前狀態(每次交接必更新)

- 目前階段: build
- 最後更新: 2026-07-26 / 當時階段: build（CI 打包、.gitignore、README 下載段落）
- 交接基準 commit: bb6d8ac [build] README 下載段落改為 H3 分段版式（使用者手改）
- 進行中任務: 等待新 session/新工具審閱 `package.yml` 與 `.gitignore` 異動（CI 實測已通過，見〈交接日誌〉最上方條目的檢查點 1-5）
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


### 2026-08-25 16:04 [maintain] 使用工具: Claude Code

- 完成了什麼: 依使用者指示，將 `AGENTS.md` 整份覆蓋升級至 Playbook v9（原版本 v2）。改動摘要：新增「交接基準 commit」欄位與其填寫規則、覆蓋前後順序規定（§2）；新增 §2.1 Review Loop 審閱提示機制；新增 §4「作用範圍僅限本檔所在目錄」巢狀邊界規則；新增語言與編碼規範明文（UTF-8／繁體中文）；新增 `Playbook-Variant: online` 標記。舊版 AGENTS.md（v2，commit `4eb13df`）已存於 git 歷史，可用 `git show 4eb13df:AGENTS.md` 找回，不再另外存檔。同時將 `scripts/hooks/pre-commit`／`commit-msg` 整份覆蓋至 v9 版本（中文檔名相容、管轄錨點收斂避免死鎖、大量檔案效能優化、commit-msg 白名單合併/還原訊息等修正），並確認 `.gitattributes` 已含 `scripts/hooks/* text eol=lf`。同步將〈A. 目前狀態〉的「最新 commit」欄改名為「交接基準 commit」（Playbook v3 起的欄位語意變更：只在接手時填一次、工作期間不再更動，不再是「做到哪」），並填入當下 HEAD。
- 下一個 agent 該做什麼: 本次改動需要審閱：確認 v9 新規則（尤其 §2.1 Review Loop 與 §4 巢狀邊界）是否符合本專案實際工作模式，並確認 hook 版本升級後 commit 仍正常通過。
- 地雷警告: 無

### 2026-07-26 [build] 使用工具: Claude Code

- 完成了什麼: 使用者要求「用 GitHub Action 自動編譯 Windows exe 與 Linux AppImage」。查證後發現此功能早已存在且實測成功——`.github/workflows/package.yml`（commit b2f6b5a 建立、fd405b3 修 YAML），Release v1.0.1（2026-06-17）由 github-actions[bot] 發佈，`PythonCPK.exe` 與 `PythonCPK-x86_64.AppImage` 兩個 asset 都在。故本次未重做，只補唯一缺口：原本僅 `push tag v*` 可觸發，無法在不發版的情況下試打包。改動三處：(1) 新增 `workflow_dispatch` 觸發器；(2) 兩個 job 各加 `actions/upload-artifact@v4`（`if-no-files-found: error`），讓手動觸發也能取得產物；(3) 兩個 `softprops/action-gh-release@v2` 步驟加上 `if: startsWith(github.ref, 'refs/tags/')`——因為手動觸發時 `github.ref_name` 是分支名而非 tag，不 guard 會建出以分支名為 tag 的錯誤 Release。驗證：以 pyyaml `safe_load` 解析成功，確認 triggers 為 `['push', 'workflow_dispatch']`、兩個 release 步驟都帶上 if 條件、upload-artifact 無 if 條件（永遠執行）。**已實跑 CI 驗證**：使用者明確指示直接 push（跳過 §2.1 先審後推），已 push `a4aeac2..34cccec`，並以 `gh workflow run` 手動觸發 run 30203433189。結果兩個 job 全綠——`build-windows` 4m22s、`build-linux` 2m6s；artifact 產出 `PythonCPK-windows-exe` 154MB、`PythonCPK-linux-appimage` 198MB（非空，確認是真實 binary）；兩個 `action-gh-release` 步驟均顯示 skipped，且 `gh release list` 仍只有 v1.0.1、未出現以 `main` 為 tag 的垃圾 Release，證實 `refs/tags/` guard 生效。唯一 annotation 是 Node.js 20 deprecation 警告（GitHub 已自動改用 Node 24 執行，不影響打包，屬 actions 上游版本問題）。

  **後續（同 session 追加）**：使用者詢問 154MB/198MB 執行檔是否適合放進 repo 的 `bin/`，回答不適合——GitHub 單檔硬上限 100MB 會直接拒絕 push，且 git 永久保存每版、二進位檔無法 delta 壓縮、Git LFS 免費額度 1GB 也撐不住；正解就是已在用的 GitHub Releases（單檔 2GB、不計入 repo 大小）。`bin/` 目前為空目錄且 git 不追蹤空目錄，無需處理。查證時發現兩個既有問題並依使用者指示修正：(1) 專案完全沒有 `.gitignore`，`.venv/` 只是僥倖未被追蹤，任何人跑 `git add -A` 就會把整個虛擬環境塞進版控；已新增 `.gitignore` 共 8 條規則（`__pycache__/`、`*.pyc`、`.venv/`、`build/`、`dist/`、`*.spec`、`*.AppImage`、`AppDir/`）。(2) `__pycache__/app.cpython-312.pyc` 自早期 commit 9c5ebf5 "new" 起就被追蹤（非本次異動造成），已用 `git rm --cached` 移除追蹤、保留磁碟檔案。驗證：`git check-ignore -v` 逐條確認 8 條規則全部命中（含用假路徑測試 `*.AppImage`、`*.spec`、巢狀 `sub/foo.pyc`），並反向確認 `app.py`、`DATA.csv`、`requirements.txt` 未被誤擋；`git status` 確認 .pyc 轉為 `D` 且不再以未追蹤檔案出現。

  **再追加**：潤飾 README「Bin Download」段落（純 README 異動，依 §2.1 不需審閱）。原段落問題：用 `#` H1 與專案標題同級、裸 URL 未做成 markdown 連結、未標示平台、與其他章節的 `## emoji 中文 (English)` 風格不一致、尾端多餘空行。改為 `## ⬇️ 下載執行檔 (Downloads)`，以表格列出 Windows/Linux 兩列，各自提供 GitHub Releases（指向 `/releases/latest`，永遠是最新版）與原有 Google Drive 兩個來源，並補上 AppImage 必要的 `chmod +x` 說明。保留原 Google Drive 連結未刪。驗證：`grep -n '^#'` 確認標題層級為單一 H1 + 全部章節 H2 + 一個巢狀 H3。

  **決策記錄**：使用者詢問「推新的上去會不會自動編譯」，說明現況為 tag-only 觸發後，**使用者明確決定維持現況，不加 `on.push.branches: [main]`**（理由：改 README 也會觸發 6 分鐘打包與 350MB artifact，無意義；公開 repo 雖然 Actions 分鐘數免費仍屬浪費）。相關實況已整理進 E 區〈發版流程〉〈二進位檔散佈〉〈README 下載連結〉三條，後續 agent 直接查 E 區即可，不必重新推導。使用者另指示直接 push，本次連同前兩筆未推的 commit（b943a93、f884fc5）一併推出。

  **使用者自行修改 README 下載段落**：使用者手動把該段從表格改為 H3 分段版式——`## ⬇️ 下載執行檔 (Downloads)` 下先放一條共用的 [GitHub Releases](https://github.com/lee18-in/PythonCPK/releases/latest) 連結，再以 `### Windows ： \`PythonCPK.exe\`` 與 `### Linux ： \`PythonCPK-x86_64.AppImage\`` 兩個 H3 各自掛 Google Drive 連結，`chmod +x` 提示區塊保留。此為使用者的版式偏好，agent 不得逕自改回表格。已依指示 commit 並 push（純 README 異動，依 §2.1 不需審閱）。核對結果：三個連結 URL 與改動前完全一致、無遺失，僅版式與 Releases 連結由重複兩次改為共用一條。
- 下一個 agent 該做什麼: 本次改動仍需審閱（已 push 且 CI 實測通過，但依 §2.1 撰寫者不得自審）：(1) `git diff a4aeac2 -- .github/workflows/package.yml` 確認只動了上述三處，沒碰到既有已驗證可用的 PyInstaller / AppImage 打包邏輯；(2) 核對 `startsWith(github.ref, 'refs/tags/')` guard 是否確實蓋住兩個 job 的 release 步驟，避免手動觸發污染 Releases；(3) 確認兩個 upload-artifact 的 `path` 與各自 job 實際產物路徑相符（Windows: `dist/PythonCPK.exe`；Linux: 工作目錄根的 `PythonCPK-x86_64.AppImage`）；(4) CI 已實測通過，審閱重點放在程式碼與規則正確性，不需再驗證「能不能跑」；(5) 新增的 `.gitignore` 8 條規則是否有誤擋必要檔案（用 `git ls-files` 對照 `git status --ignored --short` 確認追蹤清單未縮減），以及 `git rm --cached` 只移除了 `.pyc`、沒動到其他追蹤檔案。
- 地雷警告: AppImage 的 fallback 圖示依賴 PIL，目前是靠 matplotlib 間接帶進 Pillow，requirements.txt 未直接列出，若日後移除 matplotlib 會壞。

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
- CI 打包 (`.github/workflows/package.yml`): 產出 Windows `PythonCPK.exe`（PyInstaller `--onefile --windowed`）與 Linux `PythonCPK-x86_64.AppImage`（PyInstaller `--onedir` + appimagetool）。
- 發版流程: **只有 push tag `v*` 會觸發編譯並自動建 Release**；一般 `git push origin main` 不觸發任何編譯；`workflow_dispatch` 手動觸發只產生 Actions artifact（預設 90 天過期）且刻意不建 Release。發版順序必須先推 main 再推 tag，否則 tag 指向的 commit 在遠端會成孤兒。指令: `git tag v1.0.2 && git push origin v1.0.2`。耗時約 5 分鐘（Windows 4m22s / Linux 2m6s，兩 job 並行）。
- 二進位檔散佈: 執行檔約 154MB(exe) / 198MB(AppImage)，**不得放進 repo**（GitHub 單檔硬上限 100MB 會拒絕 push，且 git 永久保存每版、二進位無法 delta 壓縮）。一律走 GitHub Releases（單檔上限 2GB、不計入 repo 大小、asset 永不過期）。`bin/` 目錄保持空置。
- README 下載連結: 使用 `https://github.com/lee18-in/PythonCPK/releases/latest`，為 GitHub 官方轉址端點，發新版後自動指向最新，README 無需修改（已 curl 實測 302 正常）。另有直接下載形式 `/releases/latest/download/<檔名>` 亦實測可用，目前 README 未採用。
