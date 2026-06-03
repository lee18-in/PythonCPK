import sys
import os
import platform  # [新增] 用於偵測作業系統
import numpy as np
import pandas as pd
from scipy import stats
import math
import io

# GUI 相關
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QDoubleSpinBox, QComboBox, 
                             QGroupBox, QSlider, QGridLayout, QFrame, QSplitter, 
                             QCheckBox, QPushButton, QMessageBox, QTabWidget, 
                             QTableWidget, QTableWidgetItem, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeySequence

# 繪圖相關
import matplotlib.pyplot as plt 
# [修改] 使用 qtagg 自動適配 Qt 版本，解決 Linux 相容性
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns

# ==========================================
# 0. 全域設定與跨平台字體管理
# ==========================================
# 自動偵測 OS 並設定合適的中文字體
sys_name = platform.system()
if sys_name == "Windows":
    font_list = ['Microsoft JhengHei', 'SimHei', 'Arial']
elif sys_name == "Darwin": # macOS
    font_list = ['Arial Unicode MS', 'PingFang TC', 'Heiti TC']
else: # Linux
    # 優先嘗試文泉驛微米黑與 Noto Sans CJK
    font_list = ['WenQuanYi Micro Hei', 'Noto Sans CJK TC', 'Droid Sans Fallback', 'Arial']

plt.rcParams['font.sans-serif'] = font_list
plt.rcParams['axes.unicode_minus'] = False

class Colors:
    # 移除強制文字/背景色，適配 Dark Mode
    UI_BORDER       = "#BDC3C7"
    UI_TEXT_WHITE   = "#FFFFFF"     #FFFFFF 是純白色，適合用於深色背景上的文字。
    UI_HEADER_BG    = "#F0F0F0"     #F0F0F0 是一個淺灰色，適合用於表格表頭的背景。
    UI_HEADER_TEXT  = "#000000"     #000000 是純黑色，適合用於淺色背景上的文字。
    
    # 功能性顏色保持
    BTN_NORMAL      = "#3498DB"     #3498DB 是一個明亮的藍色，適合用於按鈕的正常狀態，能夠在淺色和深色背景下都保持良好的可見性和對比度。
    BTN_HOVER       = "#2980B9"     #2980B9 是一個較深的藍色，適合用於按鈕的懸停狀態，能夠提供明確的視覺反饋，讓使用者感受到互動性，同時在不同背景下都能保持良好的可見性。
    BTN_PRESS       = "#1ABC9C"     #1ABC9C 是一個鮮豔的青綠色，適合用於按鈕的按下狀態，能夠提供強烈的視覺反饋，讓使用者明確感受到按鈕被激活，同時在淺色和深色背景下都能保持良好的可見性和對比度。
    
    STATUS_RED      = "#C0392B"     #C0392B 是一個深紅色，適合用於狀態指示器的錯誤狀態，能夠提供明確的視覺反饋。
    STATUS_GREEN    = "#27AE60"     #27AE60 是一個深綠色，適合用於狀態指示器的成功狀態，能夠提供明確的視覺反饋。
    STATUS_ORANGE   = "#E67E22"     #E67E22 是一個橙色，適合用於狀態指示器的警告狀態，能夠提供明確的視覺反饋。
    STATUS_BLUE     = "#005A8D"     #005A8D 是一個深藍色，適合用於狀態指示器的信息狀態，能夠提供明確的視覺反饋。

    # 圖表顏色
    CHART_HIST      = "#00B3FF"     #00B3FF 是一個明亮的藍色，適合用於直方圖的填充顏色，能夠提供良好的視覺效果。
    CHART_EDGE      = "#000000"     #000000 是黑色，適合用於直方圖的邊框顏色。
    CHART_FIT_LINE  = "#FF0000"     #FF0000 是紅色，適合用於擬合線的顏色，能夠與其他元素形成良好的對比。
    
    LINE_LSL        = "#D170BC"     #D170BC 是一個淡紫色，適合用於下控制限 (LSL) 的線條顏色。
    LINE_USL        = "#0AECAF"     #0AECAF 是一個淡青色，適合用於上控制限 (USL) 的線條顏色。
    LINE_TARGET     = "#50199C"     #50199C 是一個深紫色，適合用於目標值的線條顏色。
    LINE_CL         = "#FF9F43"     #FF9F43 是一個橙色，適合用於中心線 (CL) 的線條顏色。
    
    ZONE_1SIGMA     = "#9EC897"     #9EC897 是一個淡綠色，適合用於 1σ 區域的填充顏色。
    ZONE_2SIGMA     = "#FFD6A5"     #FFD6A5 是一個淡橙色，適合用於 2σ 區域的填充顏色。
    ZONE_3SIGMA     = "#FFADAD"     #FFADAD 是一個淡紅色，適合用於 3σ 區域的填充顏色。
    
    QQ_DOTS         = "#0E9EFF"     #0E9EFF 是一個明亮的藍色，適合用於 Q-Q 圖的數據點顏色。
    QQ_LINE         = "#FF0000"     #FF0000 是紅色，適合用於 Q-Q 圖的參考線顏色。
    QQ_DOT_EDGE     = "#000000"     #000000 是純黑色，適合用於 Q-Q 圖數據點的邊框。
    
    RUN_LINE        = "#34495E"     #34495E 是一個深灰色，適合用於趨勢圖的線條顏色。
    RUN_MARKER      = "#3498DB"     #3498DB 是一個明亮的藍色，適合用於趨勢圖的標記顏色。

# 自定義工具列：移除容易崩潰的 Subplots 與 Customize 按鈕
class CustomToolbar(NavigationToolbar):
    toolitems = [t for t in NavigationToolbar.toolitems if t[0] not in ('Subplots', 'Customize')]

def get_c4_constant(n):
    if n <= 1: return 1
    return np.sqrt(2 / (n - 1)) * (math.gamma(n / 2) / math.gamma((n - 1) / 2))

# ==========================================
# 自定義帶有複製/貼上功能的表格元件
# ==========================================
class CustomTableWidget(QTableWidget):
    def keyPressEvent(self, event):
        # 攔截快捷鍵: 支援 Windows (Ctrl) 與 Mac (Cmd)
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection()
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste_selection()
        else:
            super().keyPressEvent(event)

    def copy_selection(self):
        indexes = self.selectedIndexes()
        if not indexes: return
        
        min_row = min(index.row() for index in indexes)
        max_row = max(index.row() for index in indexes)
        min_col = min(index.column() for index in indexes)
        max_col = max(index.column() for index in indexes)
        
        text = ""
        for r in range(min_row, max_row + 1):
            row_data = []
            for c in range(min_col, max_col + 1):
                item = self.item(r, c)
                row_data.append(item.text() if item else "")
            text += "\t".join(row_data) + "\n"
            
        QApplication.clipboard().setText(text)

    def paste_selection(self):
        text = QApplication.clipboard().text()
        if not text: return
            
        current_row = self.currentRow()
        current_col = self.currentColumn()
        if current_row < 0 or current_col < 0: return

        # 兼容 Windows (\r\n) 和 Excel 複製的資料格式
        text = text.replace('\r', '').rstrip('\n')
        rows_data = text.split('\n')
        
        for i, row_str in enumerate(rows_data):
            if current_row + i >= self.rowCount():
                self.insertRow(self.rowCount())
                
            col_data = row_str.split('\t')
            for j, cell_val in enumerate(col_data):
                if current_col + j >= self.columnCount():
                    self.insertColumn(self.columnCount())
                    # 找出目前最大的 Group 編號並產生新欄位名稱
                    max_group_num = 0
                    # 新增的欄位索引是 self.columnCount() - 1，所以我們檢查它之前的所有欄位
                    for c_idx in range(self.columnCount() - 1):
                        header_item = self.horizontalHeaderItem(c_idx)
                        if header_item:
                            col_name = header_item.text()
                            if col_name.startswith("Group"):
                                try:
                                    num = int(col_name[5:])
                                    if num > max_group_num:
                                        max_group_num = num
                                except (ValueError, IndexError):
                                    continue
                    new_col_name = f"Group{max_group_num + 1}"
                    self.setHorizontalHeaderItem(self.columnCount() - 1, QTableWidgetItem(new_col_name))
                item = self.item(current_row + i, current_col + j)
                if item is None:
                    item = QTableWidgetItem()
                    self.setItem(current_row + i, current_col + j, item)
                item.setText(cell_val)

class CPKApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Process Capability Analysis Pro v3.0 ({platform.system()})")
        self.resize(1400, 950)

        # 初始化
        self.df = pd.DataFrame()
        self.cols = []
        self.default_usl = 0.45
        self.default_target = 0.30
        self.default_lsl = 0.15

        # 1. 主介面佈局與分頁
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # --- Tab 1: CPK 分析 ---
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.tabs.addTab(self.main_widget, "📊 CPK 分析 (Analysis)")

        # --- 左側控制面板 ---
        self.control_panel = QWidget()
        self.control_layout = QVBoxLayout(self.control_panel)
        self.control_panel.setFixedWidth(280)
        self.create_controls() 
        self.main_layout.addWidget(self.control_panel)

        # --- 右側顯示區域 ---
        self.right_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 上半部：圖表區
        self.top_chart_widget = QWidget()
        self.top_chart_layout = QHBoxLayout(self.top_chart_widget)
        self.top_chart_layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. 左上：趨勢圖
        self.chart_container_run = QWidget()
        self.vbox_run = QVBoxLayout(self.chart_container_run)
        self.vbox_run.setContentsMargins(0, 0, 0, 0)
        self.fig_run = Figure(figsize=(5, 4), dpi=100)
        self.canvas_run = FigureCanvas(self.fig_run)
        self.toolbar_run = CustomToolbar(self.canvas_run, self) 
        self.vbox_run.addWidget(self.toolbar_run)
        self.vbox_run.addWidget(self.canvas_run)
        self.top_chart_layout.addWidget(self.chart_container_run, stretch=4) 

        # 2. 右上：直方圖
        self.chart_container_hist = QWidget()
        self.vbox_hist = QVBoxLayout(self.chart_container_hist)
        self.vbox_hist.setContentsMargins(0, 0, 0, 0)
        self.fig_hist = Figure(figsize=(5, 4), dpi=100)
        self.canvas_hist = FigureCanvas(self.fig_hist)
        self.toolbar_hist = CustomToolbar(self.canvas_hist, self) 
        self.vbox_hist.addWidget(self.toolbar_hist)
        self.vbox_hist.addWidget(self.canvas_hist)
        self.top_chart_layout.addWidget(self.chart_container_hist, stretch=6) 

        self.right_splitter.addWidget(self.top_chart_widget)

        # 下半部：數據儀表板
        self.data_widget = QWidget()
        self.data_layout = QGridLayout(self.data_widget)
        self.data_layout.setContentsMargins(5, 5, 5, 5)
        self.data_layout.setSpacing(10)
        
        # 左下：Q-Q Plot
        self.fig_qq = Figure(figsize=(2.5, 3), dpi=100) 
        self.canvas_qq = FigureCanvas(self.fig_qq)
        self.data_layout.addWidget(self.canvas_qq, 0, 0) 

        # 設定比例
        self.data_layout.setColumnStretch(0, 2)
        self.data_layout.setColumnStretch(1, 3)
        self.data_layout.setColumnStretch(2, 3)
        self.data_layout.setColumnStretch(3, 3)

        self.right_splitter.addWidget(self.data_widget)
        self.right_splitter.setStretchFactor(0, 55)
        self.right_splitter.setStretchFactor(1, 45)
        self.main_layout.addWidget(self.right_splitter)

        # --- Tab 2: 數據編輯 ---
        self.data_editor_widget = QWidget()
        self.data_editor_layout = QVBoxLayout(self.data_editor_widget)
        
        self.editor_toolbar = QHBoxLayout()
        self.btn_save_csv = QPushButton("💾 儲存並更新 (Save & Update)")
        self.btn_save_csv.clicked.connect(self.save_table_to_csv)
        self.btn_del_row = QPushButton("➖ 刪除選取列 (Del Row)")
        self.btn_del_row.clicked.connect(self.del_table_row)
        self.btn_del_col = QPushButton("➖ 刪除選取欄 (Del Col)")
        self.btn_del_col.clicked.connect(self.del_table_col)
        self.btn_rename_col = QPushButton("✏️ 重新命名欄位 (Rename Col)")
        self.btn_rename_col.clicked.connect(self.rename_table_col)
        
        self.editor_toolbar.addWidget(self.btn_save_csv)
        self.editor_toolbar.addWidget(self.btn_del_row)
        self.editor_toolbar.addWidget(self.btn_del_col)
        self.editor_toolbar.addWidget(self.btn_rename_col)
        self.editor_toolbar.addStretch()
        self.data_editor_layout.addLayout(self.editor_toolbar)
        
        self.table_widget = CustomTableWidget()
        self.data_editor_layout.addWidget(self.table_widget)
        self.tabs.addTab(self.data_editor_widget, "📝 數據編輯 (Data Editor)")
        
        # 套用共用樣式至數據編輯器
        self.apply_editor_styles()

        self.reload_data(silent=True)

    def create_controls(self):
        # 簡化樣式，支援 High Contrast / Dark Mode
        style = f"""
            QGroupBox {{ 
                font-weight: bold; font-size: 14px; 
                border: 1px solid {Colors.UI_BORDER}; 
                border-radius: 6px; 
                margin-top: 10px; padding-top: 10px; 
            }}
            QGroupBox::title {{ 
                subcontrol-origin: margin; left: 10px; padding: 0 5px; 
            }}
            QLabel {{ font-size: 12px; }}
            QDoubleSpinBox {{ font-size: 13px; padding: 3px; }}
            QComboBox {{ font-size: 12px; padding: 3px; }}
            QCheckBox {{ font-size: 13px; font-weight: bold; }}
            QPushButton {{ 
                background-color: {Colors.BTN_NORMAL}; 
                color: {Colors.UI_TEXT_WHITE}; 
                font-weight: bold; font-size: 13px; 
                padding: 8px; border-radius: 4px; border: none; 
            }}
            QPushButton:hover {{ background-color: {Colors.BTN_HOVER}; }}
            QPushButton:pressed {{ background-color: {Colors.BTN_PRESS}; }}
        """
        self.control_panel.setStyleSheet(style)

    def apply_editor_styles(self):
        self.data_editor_widget.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {Colors.BTN_NORMAL}; color: {Colors.UI_TEXT_WHITE}; 
                font-weight: bold; font-size: 13px; padding: 6px 10px; border-radius: 4px; border: none; 
            }}
            QPushButton:hover {{ background-color: {Colors.BTN_HOVER}; }}
            QPushButton:pressed {{ background-color: {Colors.BTN_PRESS}; }}
            QTableWidget {{ gridline-color: {Colors.UI_BORDER}; }}
            QHeaderView::section {{ background-color: {Colors.UI_HEADER_BG}; color: {Colors.UI_HEADER_TEXT}; padding: 4px; border: 1px solid {Colors.UI_BORDER}; font-weight: bold; }}
        """)

        # 1. 數據來源
        grp_box = QGroupBox("1. 數據來源 (Source)")
        grp_layout = QVBoxLayout()
        self.btn_reload = QPushButton("🔄 重讀 CSV (Reload)")
        self.btn_reload.clicked.connect(lambda: self.reload_data(silent=False))
        grp_layout.addWidget(self.btn_reload)
        self.combo_group = QComboBox()
        self.combo_group.addItem("== ALL Combined ==") 
        self.combo_group.currentTextChanged.connect(self.update_plot)
        grp_layout.addWidget(self.combo_group)
        grp_box.setLayout(grp_layout)
        self.control_layout.addWidget(grp_box)

        # 2. 檢視參數
        plot_box = QGroupBox("2. 檢視參數 (View)")
        plot_layout = QVBoxLayout()
        
        self.chk_sigma = QCheckBox("顯示 Sigma 區間 (±1/2/3σ)")
        self.chk_sigma.setChecked(True)
        self.chk_sigma.stateChanged.connect(self.update_plot)
        plot_layout.addWidget(self.chk_sigma)
        
        self.lbl_bins = QLabel("直方圖密度 (Bins): 1.20")
        plot_layout.addWidget(self.lbl_bins)

        self.slider_bins = QSlider(Qt.Orientation.Horizontal)
        self.slider_bins.setRange(50, 300) 
        self.slider_bins.setValue(120)     
        self.slider_bins.setTracking(False)  # [新增] 避免拖拉時頻繁重繪導致 Linux 當機
        self.slider_bins.valueChanged.connect(self.update_plot)
        plot_layout.addWidget(self.slider_bins)
        
        plot_layout.addWidget(QLabel("X軸縮放 (Zoom)"))
        self.slider_zoom = QSlider(Qt.Orientation.Horizontal)
        self.slider_zoom.setRange(0, 60)
        self.slider_zoom.setValue(20)
        self.slider_zoom.setTracking(False)  # [新增] 避免拖拉時頻繁重繪導致 Linux 當機
        self.slider_zoom.valueChanged.connect(self.update_plot)
        plot_layout.addWidget(self.slider_zoom)
        plot_box.setLayout(plot_layout)
        self.control_layout.addWidget(plot_box)

        # 3. 規格設定
        spec_box = QGroupBox("3. 規格設定 (Specs)")
        spec_layout = QVBoxLayout()
        self.spin_usl = self.create_spinbox("USL (上限)", 0.45, spec_layout)
        self.spin_target = self.create_spinbox("Target (中心)", 0.30, spec_layout)
        self.spin_lsl = self.create_spinbox("LSL (下限)", 0.15, spec_layout)
        spec_box.setLayout(spec_layout)
        self.control_layout.addWidget(spec_box)

        self.control_layout.addStretch()

    def create_spinbox(self, label, val, layout):
        container = QHBoxLayout()
        lbl = QLabel(label)
        spin = QDoubleSpinBox()
        spin.setRange(-9999, 9999)
        spin.setDecimals(3)
        spin.setSingleStep(0.005)
        spin.setValue(val)
        spin.valueChanged.connect(self.update_plot)
        container.addWidget(lbl)
        container.addWidget(spin)
        layout.addLayout(container)
        return spin

    def create_stat_card(self, title, data_dict, target_layout, pos=None, header_color=Colors.STATUS_BLUE):
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ border: 1px solid {Colors.UI_BORDER}; border-radius: 6px; }}")
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel(title)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            background-color: {header_color}; color: {Colors.UI_TEXT_WHITE}; font-weight: bold; font-size: 12px;
            padding: 4px; border-top-left-radius: 5px; border-top-right-radius: 5px;
        """)
        layout.addWidget(header)

        content_widget = QWidget()
        grid = QGridLayout(content_widget)
        grid.setContentsMargins(5, 5, 5, 5)
        grid.setSpacing(4)

        r = 0
        for k, v in data_dict.items():
            lbl_k = QLabel(k)
            lbl_k.setStyleSheet("font-size: 11px; font-weight: bold;") 
            lbl_v = QLabel(str(v))
            lbl_v.setStyleSheet("font-weight: bold; font-size: 12px; font-family: Consolas, Arial;")
            lbl_v.setAlignment(Qt.AlignmentFlag.AlignRight)
            grid.addWidget(lbl_k, r, 0)
            grid.addWidget(lbl_v, r, 1)
            r += 1
        layout.addWidget(content_widget)
        
        if isinstance(target_layout, QGridLayout) and pos:
            target_layout.addWidget(frame, pos[0], pos[1])
        else:
            target_layout.addWidget(frame)

    def reload_data(self, silent=False):
        filename = 'DATA.csv'
        
        # 1. 產生 5.8 Sigma 預設資料
        if not os.path.exists(filename):
            try:
                default_data = """Items,Spec,Group1,Group2,Group3,Group4,Group5
USL,0.45,0.328,0.311,0.332,0.355,0.309
Target,0.3,0.309,0.356,0.335,0.303,0.329
LSL,0.15,0.303,0.303,0.321,0.265,0.270
,,0.300,0.289,0.323,0.291,0.278
,,0.353,0.309,0.317,0.278,0.301
,,0.318,0.285,0.325,0.299,0.307
,,0.299,0.363,0.315,0.287,0.336
,,0.283,0.320,0.264,0.280,0.320
,,0.334,0.319,0.312,0.307,0.277
,,0.296,0.303,0.342,0.324,0.269
,,0.323,0.305,0.297,0.331,0.342
,,0.339,0.293,0.307,0.324,0.340
,,0.303,0.310,0.286,0.284,0.336
,,0.350,0.313,0.341,0.324,0.298
,,0.324,0.355,0.314,0.356,0.247
,,0.336,0.317,0.307,0.317,0.263
,,0.309,0.324,0.353,0.302,0.294
,,0.302,0.339,0.324,0.301,0.328
,,0.318,0.340,0.297,0.306,0.305
,,0.277,0.323,0.322,0.315,0.309"""
                
                with open(filename, 'w', encoding='utf-8-sig') as f:
                    f.write(default_data)

                if not silent:
                    QMessageBox.warning(self, "提示", f"⚠️ 找不到 {filename}，已自動建立「範例數據 (Sigma 5.8)」檔案。")
            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"無法建立檔案: {str(e)}")
                return

        # 2. 讀取與防呆
        try:
            new_df = pd.read_csv(filename)
            if new_df.shape[1] < 3: raise ValueError("CSV 格式錯誤，至少需要 3 欄")
            
            self.df = new_df
            self.cols = self.df.columns[2:].tolist()
            spec_values = pd.to_numeric(self.df.iloc[:3, 1], errors="raise").to_numpy(dtype=np.float64)
            self.default_usl = float(spec_values[0])
            self.default_target = float(spec_values[1])
            self.default_lsl = float(spec_values[2])

            self.spin_usl.blockSignals(True)
            self.spin_target.blockSignals(True)
            self.spin_lsl.blockSignals(True)
            self.combo_group.blockSignals(True)

            self.spin_usl.setValue(self.default_usl)
            self.spin_target.setValue(self.default_target)
            self.spin_lsl.setValue(self.default_lsl)

            current_selection = self.combo_group.currentText()
            self.combo_group.clear()
            self.combo_group.addItem("== ALL Combined ==")
            self.combo_group.addItems(self.cols)
            
            index = self.combo_group.findText(current_selection)
            if index >= 0: self.combo_group.setCurrentIndex(index)
            else: self.combo_group.setCurrentIndex(0)

            self.spin_usl.blockSignals(False)
            self.spin_target.blockSignals(False)
            self.spin_lsl.blockSignals(False)
            self.combo_group.blockSignals(False)

            self.update_plot()
            self.load_data_to_table()
            if not silent: QMessageBox.information(self, "成功", "✅ CSV 資料已成功重新讀取！")

        except PermissionError:
            QMessageBox.critical(self, "檔案被佔用", 
                f"❌ 無法讀取 {filename}\n\n原因：檔案正在 Excel 中開啟。\n請「關閉 Excel」後再試一次。")
        except Exception as e:
            msg = f"❌ 無法讀取 DATA.csv\n\n錯誤訊息: {str(e)}"
            if not silent: QMessageBox.critical(self, "讀取錯誤", msg)
            else: print(msg)

    def update_plot(self):
        selected_item = self.combo_group.currentText()
        usl = self.spin_usl.value()
        target = self.spin_target.value()
        lsl = self.spin_lsl.value()
        
        k_gan = self.slider_bins.value() / 100.0
        self.lbl_bins.setText(f"直方圖密度 (Bins): {k_gan:.2f}")

        padding_pct = self.slider_zoom.value() / 100.0
        show_sigma = self.chk_sigma.isChecked()

        sigma_within = 0
        sigma_overall = 0
        
        if self.df.empty: return

        if selected_item == "== ALL Combined ==":
            numeric_df = self.df.iloc[:, 2:].apply(pd.to_numeric, errors="coerce")
            raw_values = numeric_df.to_numpy(dtype=np.float64).flatten(order='F')
            data = raw_values[~np.isnan(raw_values)]

            group_stds = numeric_df.std(ddof=1)
            s_bar = float(group_stds.mean())
            counts = numeric_df.count()
            avg_n = float(counts.mean())
            c4 = get_c4_constant(avg_n)
            sigma_within = s_bar / c4 
            sigma_overall = float(np.std(data, ddof=1))
        else:
            data = pd.to_numeric(self.df[selected_item], errors="coerce").dropna().to_numpy(dtype=np.float64)
            if len(data) < 2: 
                self.clear_charts()
                return

            n_sub = len(data)
            sigma_overall = float(np.std(data, ddof=1))
            c4 = get_c4_constant(n_sub)
            sigma_within = sigma_overall / c4 
            
        if len(data) < 2: return

        n = len(data)
        mean = float(np.mean(data))
        data_min = float(np.min(data))
        data_max = float(np.max(data))
        data_range = data_max - data_min

        T = usl - lsl
        Cp = T / (6 * sigma_within)
        Ca = (mean - target) / (T / 2)
        Cpk = (1 - abs(Ca)) * Cp
        
        Cpu = (usl - mean) / (3 * sigma_overall)
        Cpl = (mean - lsl) / (3 * sigma_overall)
        Ppk = min(Cpu, Cpl)
        Pp = T / (6 * sigma_overall)
        
        tau = np.sqrt(sigma_overall**2 + (mean - target)**2)
        Cpm = T / (6 * tau)

        prob_over_usl = 1 - stats.norm.cdf((usl - mean) / sigma_overall)
        prob_below_lsl = stats.norm.cdf((lsl - mean) / sigma_overall)
        total_defect_rate = prob_over_usl + prob_below_lsl
        total_ppm = total_defect_rate * 1e6
        yield_rate = (1 - total_defect_rate) * 100
        sigma_level_excel = 3 * Ppk 

        if Ppk >= 1.67: status = "Super (六標準差)"
        elif Ppk >= 1.33: status = "Capable (足夠)"
        elif Ppk >= 1.0: status = "Marginal (尚可)"
        else: status = "Fail (不足)"

        advice = []
        if abs(Ca) > 0.125: advice.append("⚠️ 中心偏移 (調機)") 
        if Cp < 1.33:  advice.append("⚠️ 變異過大 (改善穩定)")
        if not advice and Ppk >= 1.33: advice.append("✅ 製程穩定")
        advice_text = " / ".join(advice) if advice else "需綜合分析"

        self.update_stat_cards(usl, target, lsl, mean, data_max, data_min, sigma_overall, data_range, 
                               sigma_within, Cp, Ca, Cpk, Pp, Cpu, Cpl, Ppk, Cpm, n, total_ppm, 
                               yield_rate, sigma_level_excel, status, advice_text)

        self.plot_run_chart(data, mean, usl, lsl, sigma_overall)
        self.plot_histogram(data, n, mean, sigma_overall, usl, target, lsl, k_gan, padding_pct, show_sigma)
        self.plot_qq(data)

    def clear_charts(self):
        self.fig_hist.clear(); self.canvas_hist.draw()
        self.fig_run.clear(); self.canvas_run.draw()
        self.fig_qq.clear(); self.canvas_qq.draw()

    def update_stat_cards(self, usl, target, lsl, mean, dmax, dmin, sigma_ov, drange, 
                          sigma_wi, Cp, Ca, Cpk, Pp, Cpu, Cpl, Ppk, Cpm, n, ppm, yield_r, sig_lv, status, advice):
        # 清除左下角舊卡片 (倒序刪除)
        for i in reversed(range(self.control_layout.count())):
            item = self.control_layout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if isinstance(widget, QFrame):
                widget.setParent(None)

        self.create_stat_card("規格與基礎統計 (Basic Stats)", {
            "USL": f"{usl:.3f}", "Target": f"{target:.3f}", "LSL": f"{lsl:.3f}",
            "Mean": f"{mean:.4f}", "Max": f"{dmax:.4f}", "Min": f"{dmin:.4f}",
            "Std (Overall)": f"{sigma_ov:.4f}", "Range": f"{drange:.4f}"
        }, self.control_layout, None, Colors.STATUS_BLUE)

        # 清除右下角舊卡片
        for i in reversed(range(self.data_layout.count())): 
            item = self.data_layout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if widget == self.canvas_qq:
                continue 
            if widget is not None:
                widget.setParent(None)

        self.create_stat_card("製程能力 (CPK)", {
            "Std (Within)": f"{sigma_wi:.4f}", "Cp": f"{Cp:.3f}",
            "Ca": f"{Ca:.2%}", "Cpk": f"{Cpk:.3f}", "Cpk σ": f"{3*Cpk:.2f}"
        }, self.data_layout, (0, 1), Colors.STATUS_GREEN)

        self.create_stat_card("製程績效 (PPK)", {
            "Pp": f"{Pp:.3f}", "Ppu": f"{Cpu:.3f}", "Ppl": f"{Cpl:.3f}",
            "Ppk": f"{Ppk:.3f}", "Cpm": f"{Cpm:.3f}"
        }, self.data_layout, (0, 2), Colors.STATUS_ORANGE)

        bg_status = Colors.STATUS_RED if Ppk < 1.0 else Colors.STATUS_GREEN
        ppm_str = f"{int(ppm)}" if ppm >= 1 else "< 1"
        self.create_stat_card("良率預估 (Yield)", {
            "N": f"{n}", "PPM": ppm_str, "Yield": f"{yield_r:.2f}%",
            "Sigma": f"{sig_lv:.2f}σ", "判定": status,
            "建議": advice
        }, self.data_layout, (0, 3), bg_status)

    def plot_run_chart(self, data, mean, usl, lsl, sigma):
        self.fig_run.clear()
        ax = self.fig_run.add_subplot(111)
        ax.plot(data, marker='o', linestyle='-', color=Colors.RUN_LINE, 
                markerfacecolor=Colors.RUN_MARKER, markersize=3, linewidth=1, label='Values')
        ax.axhline(mean, color=Colors.LINE_TARGET, linestyle='--', linewidth=1.5, label='Mean')
        ax.axhline(usl, color=Colors.LINE_USL, linestyle=':', alpha=0.6, label='USL')
        ax.axhline(lsl, color=Colors.LINE_LSL, linestyle=':', alpha=0.6, label='LSL')
        
        ucl = mean + 3 * sigma
        lcl = mean - 3 * sigma
        ax.axhline(ucl, color=Colors.LINE_CL, linestyle='--', linewidth=1, alpha=0.8, label='UCL (+3σ)')
        ax.axhline(lcl, color=Colors.LINE_CL, linestyle='--', linewidth=1, alpha=0.8, label='LCL (-3σ)')

        ax.set_title("Run Chart (Process Stability)", fontsize=11, fontweight='bold')
        ax.set_xlabel("Observation Index")
        ax.set_ylabel("Value")
        ax.legend(loc='upper right', fontsize='x-small', ncol=2, framealpha=0.8)
        ax.grid(True, alpha=0.3)
        self.fig_run.tight_layout()
        self.canvas_run.draw()

    def plot_histogram(self, data, n, mean, sigma, usl, target, lsl, k_gan, padding_pct, show_sigma):
        self.fig_hist.clear()
        ax = self.fig_hist.add_subplot(111)
        
        bins = int((np.log2(n) + 1) * 3 * k_gan)
        bins = max(5, bins)
        
        sns.histplot(data, kde=True, stat="density", color=Colors.CHART_HIST, bins=bins, ax=ax, 
                     edgecolor=Colors.CHART_EDGE, linewidth=0.3, alpha=0.4, zorder=3)
        
        ax.axvline(lsl, color=Colors.LINE_LSL, linestyle='-', linewidth=2, label='LSL', zorder=5)
        ax.axvline(usl, color=Colors.LINE_USL, linestyle='-', linewidth=2, label='USL', zorder=5)
        ax.axvline(target, color=Colors.LINE_TARGET, linestyle='--', linewidth=1.5, label='Target', zorder=5)
        
        x_range = usl - lsl
        x_min_plot = min(lsl, np.min(data)) - (x_range * padding_pct)
        x_max_plot = max(usl, np.max(data)) + (x_range * padding_pct)
        x = np.linspace(x_min_plot, x_max_plot, 400)
        p = stats.norm.pdf(x, mean, sigma) 
        ax.plot(x, p, color=Colors.CHART_FIT_LINE, linestyle="--", linewidth=2, label='Fit', zorder=4)

        if show_sigma:
            for i, (factor, color, lbl) in enumerate([(3, Colors.ZONE_3SIGMA, '±3σ'), 
                                                      (2, Colors.ZONE_2SIGMA, '±2σ'), 
                                                      (1, Colors.ZONE_1SIGMA, '±1σ')], 1):
                if factor > 1:
                   mask_L = (x >= mean - factor*sigma) & (x < mean - (factor-1)*sigma)
                   mask_R = (x > mean + (factor-1)*sigma) & (x <= mean + factor*sigma)
                   ax.fill_between(x, 0, p, where=mask_L, color=color, alpha=0.8, zorder=1, label=lbl)
                   ax.fill_between(x, 0, p, where=mask_R, color=color, alpha=0.8, zorder=1)
                else:
                   mask = (x >= mean - factor*sigma) & (x <= mean + factor*sigma)
                   ax.fill_between(x, 0, p, where=mask, color=color, alpha=0.8, zorder=1, label=lbl)

        ax.set_title(f"Histogram & Capability Analysis", fontsize=11, fontweight='bold')
        ax.legend(loc='upper right', fontsize='x-small', framealpha=0.9)
        ax.grid(True, alpha=0.3, zorder=0)
        self.fig_hist.tight_layout()
        self.canvas_hist.draw()

    def plot_qq(self, data):
        self.fig_qq.clear()
        ax = self.fig_qq.add_subplot(111)
        (osm_raw, osr_raw), (slope_raw, intercept_raw, _r) = stats.probplot(data, dist="norm", plot=None)
        osm = np.asarray(osm_raw, dtype=np.float64)
        osr = np.asarray(osr_raw, dtype=np.float64)
        slope = float(slope_raw)  # type: ignore
        intercept = float(intercept_raw)  # type: ignore
        ax.plot(osm, osr, 'o', color=Colors.QQ_DOTS, markersize=4, markeredgecolor=Colors.QQ_DOT_EDGE, markeredgewidth=0.5, alpha=0.6)
        ax.plot(osm, slope*osm + intercept, color=Colors.QQ_LINE, linestyle="-", linewidth=2)
        ax.set_title("Q-Q Plot", fontsize=10, fontweight='bold')
        ax.set_xlabel(""); ax.set_ylabel("")
        ax.tick_params(labelsize=8)
        ax.grid(True, alpha=0.3)
        self.fig_qq.tight_layout()
        self.canvas_qq.draw()

    # ==========================================
    # 數據編輯器相關功能
    # ==========================================
    def load_data_to_table(self):
        if self.df is None or self.df.empty:
            return
            
        # 預留額外的空白區域，讓使用者可以直接貼上資料，無需一直按新增
        EXTRA_ROWS = 50
        EXTRA_COLS = 10
        
        self.table_widget.setRowCount(self.df.shape[0] + EXTRA_ROWS)
        self.table_widget.setColumnCount(self.df.shape[1] + EXTRA_COLS)
        
        headers = list(self.df.columns.astype(str))
        # 找出目前最大的 Group 編號
        max_group_num = 0
        for col_name in headers:
            if col_name.startswith("Group"):
                try:
                    num = int(col_name[5:])
                    if num > max_group_num:
                        max_group_num = num
                except (ValueError, IndexError):
                    continue

        for i in range(EXTRA_COLS):
            headers.append(f"Group{max_group_num + i + 1}")
        self.table_widget.setHorizontalHeaderLabels(headers)
        
        for row in range(self.df.shape[0]):
            for col in range(self.df.shape[1]):
                val = self.df.iloc[row, col]
                item = QTableWidgetItem(str(val) if pd.notna(val) else "")
                self.table_widget.setItem(row, col, item)
                
    def save_table_to_csv(self):
        rows = self.table_widget.rowCount()
        cols = self.table_widget.columnCount()
        
        headers = []
        for col in range(cols):
            header_item = self.table_widget.horizontalHeaderItem(col)
            headers.append(header_item.text() if header_item else f"Col{col}")
            
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.table_widget.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
            
        new_df = pd.DataFrame(data, columns=headers)
        
        # 儲存前清除完全空白的列和欄 (自動清理保留區域)
        new_df.replace("", np.nan, inplace=True)
        new_df.dropna(how="all", axis=0, inplace=True)
        new_df.dropna(how="all", axis=1, inplace=True)
        new_df.fillna("", inplace=True)
        
        try:
            new_df.to_csv('DATA.csv', index=False, encoding='utf-8-sig')
            QMessageBox.information(self, "成功", "✅ 資料已成功儲存並同步更新分析結果！")
            self.reload_data(silent=True)
        except PermissionError:
            QMessageBox.critical(self, "檔案被佔用", "❌ 無法儲存 DATA.csv\n\n原因：檔案正在 Excel 中開啟。請「關閉 Excel」後再試一次。")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"儲存失敗: {str(e)}")

    def del_table_row(self):
        row = self.table_widget.currentRow()
        if row >= 0: self.table_widget.removeRow(row)
        else: QMessageBox.warning(self, "提示", "請先點選想刪除的「列 (Row)」")

    def del_table_col(self):
        col = self.table_widget.currentColumn()
        if col >= 0: self.table_widget.removeColumn(col)
        else: QMessageBox.warning(self, "提示", "請先點選想刪除的「欄位 (Column)」")

    def rename_table_col(self):
        col = self.table_widget.currentColumn()
        if col < 0: return QMessageBox.warning(self, "提示", "請先點選一個欄位內的儲存格")
        old_name = self.table_widget.horizontalHeaderItem(col).text() if self.table_widget.horizontalHeaderItem(col) else f"Col{col}"
        new_name, ok = QInputDialog.getText(self, "重新命名欄位", "輸入新名稱:", text=old_name)
        if ok and new_name: self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem(new_name))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Microsoft JhengHei", 10)
    app.setFont(font)
    window = CPKApp()
    window.show()
    sys.exit(app.exec())
