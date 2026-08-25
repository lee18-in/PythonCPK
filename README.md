<!-- AI AGENTS: Read ./AGENTS.md first, then ./LLM_MEMORY.md.
     Do NOT write planning content into this file. -->

> - **Language and Encoding Standards**: All system files, code annotations, memory files (`LLM_MEMORY.md`), and handover logs for this project are uniformly encoded in **UTF-8** and **Traditional Chinese** by default.

# Process Capability Analysis Pro (PythonCPK)

Process Capability Analysis Pro 是一個基於 Python 與 PyQt6 打造的製程能力分析工具。它提供直覺的圖形化介面 (GUI)，協助工程師、品管人員快速計算與視覺化製程能力指標 (CPK, PPK)。

## ⬇️ 下載執行檔 (Downloads)

免安裝 Python 環境，下載對應平台的檔案即可直接執行。

[GitHub Releases](https://github.com/lee18-in/PythonCPK/releases/latest)

### Windows ： `PythonCPK.exe`
[Google Drive](https://drive.google.com/file/d/1lfFs8Xbb8VX1WigY-_AlcZCcGL_BDAGq/view?usp=drive_link)

### Linux ： `PythonCPK-x86_64.AppImage`
[Google Drive](https://drive.google.com/file/d/1WaoFvXiQzaU33atc9k4lI-HHQNf5PZXU/view?usp=drive_link)

> **Linux 使用者**：下載後需先賦予執行權限才能啟動。
>
> ```bash
> chmod +x PythonCPK-x86_64.AppImage
> ./PythonCPK-x86_64.AppImage
> ```

## ✨ 功能特色 (Features)

- **開箱即用**：若無指定的 `DATA.csv`，程式將自動生成一份 5.8 Sigma 的範例數據供您測試。
- **完整的製程統計計算**：
  - 基礎統計：Mean, Max, Min, Std (Overall & Within), Range。
  - 製程能力指標：Cp, Ca, Cpk。
  - 製程績效指標：Pp, Ppu, Ppl, Ppk, Cpm。
- **良率與缺陷率預估 (Yield Estimation)**：自動推算 PPM、預估良率 (%) 及對應的 Sigma 等級。
- **豐富的圖表視覺化**：
  - **趨勢圖 (Run Chart)**：檢視製程的穩定度，標示平均值與管制界線 (±3σ)。
  - **直方圖 (Histogram)**：支援常態分配擬合，並可動態顯示/隱藏 ±1σ/2σ/3σ 常態分佈區間。
  - **Q-Q Plot**：視覺化檢定資料是否符合常態分佈。
- **動態參數調整**：支援直接在介面上調整 USL/Target/LSL 規格，並透過滑桿即時改變直方圖密度與視圖縮放。
- **跨平台支援**：自動偵測 Windows、macOS 與 Linux 系統並配置合適的中文字體，避免圖表出現亂碼。

## 📦 安裝需求 (Prerequisites)

請確保您的系統已安裝 Python 3.8 (或以上) 版本。
您可以透過 `pip` 來安裝本專案所需的依賴套件：

```bash
pip install numpy pandas scipy matplotlib seaborn PyQt6
```

## 🚀 啟動方式 (Usage)

在終端機中進入程式所在目錄，執行以下指令即可啟動應用程式：

```bash
python app.py
```

### 📂 資料格式說明 (DATA.csv)
應用程式預設會讀取同一目錄下的 `DATA.csv`。
資料表最少需要包含 3 欄（第一欄為項目/名稱，後續欄位為各組數據）。**前三列必須固定設定規格**，格式範例如下：

| Items  | Spec | Group1 | Group2 | Group3 |
| ------ | ---- | ------ | ------ | ------ |
| USL    | 0.45 | 0.328  | 0.311  | 0.332  |
| Target | 0.30 | 0.309  | 0.356  | 0.335  |
| LSL    | 0.15 | 0.303  | 0.303  | 0.321  |
|        |      | 0.300  | 0.289  | 0.323  |
|        |      | 0.353  | 0.309  | 0.317  |

*您可以隨時透過應用程式左上角的 `[🔄 重讀 CSV]` 按鈕重新載入修改後的資料。*

## 📄 授權條款 (License)

本專案採用 MIT License 開源授權條款。
您可以自由地使用、修改與散佈此專案。
