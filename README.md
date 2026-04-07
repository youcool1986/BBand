# Bollinger Bands Backtrader Strategy

這是一個使用 Backtrader 框架實現的簡單 Bollinger Bands (布林通道) 交易策略範例。策略基於 yfinance 下載的 Nasdaq 期貨 (NQ=F) 歷史資料，進行回測。買入條件為當日最低價觸及布林帶下軌，賣出條件為當日最高價觸及布林帶上軌。專案包含錯誤處理、NaN 資料清除，以及足夠的初始資金設定，以確保回測順利運行。

## 專案描述
- **策略邏輯**：
  - **買入**：如果當日最低價 <= 布林帶下軌，買入 100 單位。
  - **賣出**：如果持有部位且當日最高價 >= 布林帶上軌，賣出 100 單位。
- **指標參數**：
  - 週期 (period)：20
  - 偏差因子 (devfactor)：1.4
- **資料來源**：yfinance 下載的 NQ=F 資料 (2023-01-01 至 2024-01-01)。
- **回測設定**：初始資金 10 億美元，確保無資金不足問題。
- **輸出**：回測結果包括初始/最終資金，並繪製 K 線圖 (candlestick)。

此策略僅供學習與回測用途，不適合實際交易。請自行調整參數或風險管理。

## 需求
- Python 3.6+
- 必要套件：
  - backtrader
  - yfinance
  - pandas
  - matplotlib (用於繪圖)

## 安裝
1. 建立虛擬環境 (可選，但推薦)：
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. 安裝依賴套件：
   ```
   pip install backtrader yfinance pandas matplotlib
   ```

## 使用方式
1. 將代碼儲存為 `bollinger_strategy.py`。
2. 在終端運行：
   ```
   python bollinger_strategy.py
   ```
3. 輸出：
   - 終端會顯示資料下載進度、初始/最終資金。
   - 自動開啟回測圖表 (K 線圖，包含布林帶指標)。

**範例輸出**：
```
正在下載資料...
初始資金: 1000000000.00
最終資金: [計算結果].00
```
- 圖表將顯示交易點位 (買入/賣出箭頭)。

## 策略細節
- **初始化**：使用 `bt.indicators.BollingerBands` 計算上軌、中軌、下軌 (基於收盤價)。
- **訂單處理**：在 `notify_order` 中檢查訂單狀態，若取消/拒絕，會印出警告 (e.g., 資金不足或 NaN 資料)。
- **next() 邏輯**：
  - 跳過布林帶未計算完成的初期資料 (NaN 值)。
  - 無部位時檢查買入條件。
  - 有部位時檢查賣出條件。
- **資料處理**：
  - 使用 yfinance 下載資料，並清除所有 NaN 行。
  - 以 PandasData 載入 Backtrader，指定 Open/High/Low/Close/Volume 欄位。

## 注意事項
- **風險**：這是回測策略，歷史表現不代表未來。實際交易需考慮滑點、手續費、稅務等。
- **客製化**：
  - 修改 `params` 中的 period 或 devfactor 以調整布林帶。
  - 變更 `yf.download` 的股票代碼、日期範圍來測試其他資產。
  - 增加風險管理 (e.g., 停損、部位大小調整)。
- **常見問題**：
  - 如果圖表不顯示，確保 matplotlib 已安裝並支援後端。
  - yfinance 可能因網路問題下載失敗，重試或檢查 VPN。
- **Backtrader 提示**：若訂單被拒絕，檢查 `notify_order` 的警告訊息，通常是資料問題或資金不足。

## 貢獻
歡迎 fork 此專案並提交 pull request。如果有 bug 或改進建議，請開 issue。

## 授權
MIT License - 免費使用、修改、分發，但無保證。
