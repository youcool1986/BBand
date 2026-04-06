import backtrader as bt
import yfinance as yf
import pandas as pd
import math


class BollingerBandsStrategy(bt.Strategy):
    params = (
        ("period", 20),
        ("devfactor", 1.4),  # 依照您截圖上的設定 1.4
    )

    def __init__(self):
        self.order = None

        # 建立布林帶指標 (基於收盤價計算)
        self.bband = bt.indicators.BollingerBands(
            self.data.close,
            period=self.params.period,
            devfactor=self.params.devfactor
        )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 檢查訂單是否完成
        if order.status in [order.Completed]:
            self.order = None
        # 【關鍵除錯】檢查訂單是否被拒絕或取消
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f"⚠️ 警告：訂單未執行！狀態碼: {order.status} (可能是資金不足或遇到資料空值)")
            self.order = None

    def next(self):
        if self.order:
            return

        # 確保布林帶已經產生數值 (前 20 天會是 NaN，不能比較)
        if math.isnan(self.bband.lines.bot[0]):
            return

        if not self.position:
            # 買入條件：當日最低價 <= 布林帶下軌
            if self.data.low[0] <= self.bband.lines.bot[0]:
                self.order = self.buy(size=100)
        else:
            # 賣出條件：當日最高價 >= 布林帶上軌
            if self.data.high[0] >= self.bband.lines.top[0]:
                self.order = self.sell(size=100)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BollingerBandsStrategy)

    # 1. 下載資料
    print("正在下載資料...")
    df = yf.download('NQ=F', start='2023-01-01', end='2024-01-01', auto_adjust=False)

    # 處理 yfinance 可能回傳的 MultiIndex 欄位
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 【關鍵修復】清除所有包含 NaN 的無效資料列，防止訂單在隔天開盤被拒絕
    df = df.dropna()

    # 2. 載入資料 (明確指定欄位名稱)
    data = bt.feeds.PandasData(
        dataname=df,
        open='Open',
        high='High',
        low='Low',
        close='Close',
        volume='Volume',
        openinterest=None
    )
    cerebro.adddata(data)

    # 3. 設定初始資金 (設定 10 億，確保絕對夠買 size=100)
    cerebro.broker.setcash(1000000000.0)

    print('初始資金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('最終資金: %.2f' % cerebro.broker.getvalue())

    # 4. 畫圖
    cerebro.plot(style='candlestick')
