# COMPONENT_MAP.md — PythonCPK 不衰減知識庫

> - **Language and Encoding Standards**: All system files, code annotations, memory files (`LLM_MEMORY.md`), and handover logs for this project are uniformly encoded in **UTF-8** and **Traditional Chinese** by default.

## 0. 六十秒進入狀況

- **專案定位**：PyQt6 桌面製程能力分析（CPK）工具，入口為 `app.py`。
- **執行／建置指令**：`python app.py`（啟動 PyQt6 GUI 分析工具）
- **測試指令**：無自動化測試套件（手動 GUI 測試）。
- **程式碼慣例**：Python 3.8+／PyQt6／NumPy／Pandas／SciPy／Matplotlib／Seaborn（PEP 8）。
- **發版核心紅線**：只有 push tag `v*` 會建置並發佈 Release；`bin/` 目錄保持空置，執行檔一律走 GitHub Releases。

---

## 1. 專案結構與發版契約

- **核心檔案**：`app.py`（GUI 與分析邏輯）、`DATA.csv`、`requirements.txt`、`.github/workflows/package.yml`、`.gitignore`、`.gitattributes`、`scripts/hooks/`（`pre-commit`、`commit-msg`）。
- **CI 打包（`.github/workflows/package.yml`）**：
  - Windows：`PythonCPK.exe`（PyInstaller `--onefile --windowed`，產物路徑 `dist/PythonCPK.exe`，約 154 MB）。
  - Linux：`PythonCPK-x86_64.AppImage`（PyInstaller `--onedir` + `appimagetool`，產物路徑根目錄 `PythonCPK-x86_64.AppImage`，約 198 MB）。
- **發版流程與權限邊界**：
  - 僅 push `v*` tag 觸發編譯與 `softprops/action-gh-release@v2` 發佈（須先推 `main` 再推 tag，例如 `git tag v1.0.2 && git push origin v1.0.2`，兩 job 並行約 5 分鐘）。
  - `workflow_dispatch` 手動觸發僅上傳 `actions/upload-artifact@v4`（`if-no-files-found: error`，保存 90 天），release 步驟具 `if: startsWith(github.ref, 'refs/tags/')` 防誤建假 Release。
- **二進位檔與下載規範**：
  - 禁止將 `.exe` / `.AppImage` 放進 repo（GitHub 單檔上限 100 MB），`bin/` 保持空置，統一放 GitHub Releases（單檔上限 2 GB）。
  - `README.md`〈⬇️ 下載執行檔 (Downloads)〉維持使用者偏好的 **H3 分段版式**（共用 `/releases/latest` 連結＋Windows／Linux 分段與 Google Drive 連結＋`chmod +x` 提示），禁止改回表格。

---

## 2. 決策理由、環境隱性條件與地雷

1. **維持 tag-only 自動打包（2026-07-26 使用者裁定）**：不新增 `on.push.branches: [main]`，避免改 `README.md` 觸發約 6 分鐘打包與 ~350 MB artifact 浪費。
2. **`.gitignore` 8 條防誤納規則（2026-07-26）**：涵蓋 `__pycache__/`、`*.pyc`、`.venv/`、`build/`、`dist/`、`*.spec`、`*.AppImage`、`AppDir/`；已將早期誤追蹤之 `__pycache__/app.cpython-312.pyc` 以 `git rm --cached` 移出索引。
3. **AppImage 圖示隱性依賴**：fallback 圖示依賴 PIL（由 `matplotlib` 間接帶入 Pillow，`requirements.txt` 未直接列出）；若日後移除 `matplotlib` 須補列 `Pillow`。
4. **Git Hooks 約束**：本倉啟用 `core.hooksPath=scripts/hooks`，`.gitattributes` 含 `scripts/hooks/* text eol=lf`；遵守 `AGENTS.md` §3 與 §0 自檢，不得以 `--no-verify` 略過。

---

## 3. 驗證台帳

| 日期 | 驗證項目 | 環境與方法 | 結果 |
|---|---|---|---|
| 2026-07-26 | `package.yml` 語法與手動 CI 打包 | `pyyaml` `safe_load` 解析＋`gh workflow run`（run `30203433189`） | 雙 job 綠燈（Windows 4m22s / 154 MB、Linux 2m6s / 198 MB）；`action-gh-release` 正確 skipped，未建假 tag Release |
| 2026-07-26 | `.gitignore` 8 條規則有效性與追蹤保護 | 逐條 `git check-ignore -v`（含假路徑）＋核對 `app.py`／`DATA.csv`／`requirements.txt` 未被擋 | 8 條全數命中，必要檔未受影響，`.pyc` 已自索引移除 |
