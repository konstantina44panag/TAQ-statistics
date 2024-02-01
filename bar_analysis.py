import pandas as pd
import numpy as np
"""This script transforms the data to bar variables, time bars, volume bars and dollar bars."""

class MarketBars:
    def __init__(self, df, ask, bid, volume_threshold, market_value):
        self.df = df
        self.ask = ask
        self.bid = bid
        self.volume_threshold = volume_threshold
        self.market_value = market_value

    def bar(self, x, y):
        return np.int64(x / y) * y

    def compute_volume_bars(self):
        volume_bars_trades = self.df.groupby(self.bar(np.cumsum(self.df["vol"]), self.volume_threshold)).agg(
            {"time": "last", "price": "ohlc", "vol": "sum"}
        )
        volume_bars_ask = self.ask.groupby(self.bar(np.cumsum(self.ask["vol"]), self.volume_threshold)).agg(
             {"time": "last", "price": "ohlc", "vol": "sum"}
        )
        volume_bars_bid = self.bid.groupby(self.bar(np.cumsum(self.bid["vol"]), self.volume_threshold)).agg(
             {"time": "last", "price": "ohlc", "vol": "sum"}
        )
        return volume_bars_trades, volume_bars_ask, volume_bars_bid

    def compute_dollar_bars(self):
        self.df["value"] = self.df["price"] * self.df["vol"]
        dollar_bars_trades = self.df.groupby(self.bar(np.cumsum(self.df["value"]), self.market_value)).agg(
            {"time": "last", "price": "ohlc", "vol": "sum", "value" : "sum"}
        )

        self.ask["value"] = self.ask["price"] * self.ask["vol"]
        dollar_bars_ask = self.ask.groupby(self.bar(np.cumsum(self.ask["value"]), self.market_value)).agg(
            {"time": "last", "price": "ohlc", "vol": "sum", "value" : "sum"}
        )

        self.bid["value"] = self.bid["price"] * self.bid["vol"]
        dollar_bars_bid = self.bid.groupby(self.bar(np.cumsum(self.bid["value"]), self.market_value)).agg(
            {"time": "last", "price": "ohlc", "vol": "sum", "value" : "sum"}
        )
        return dollar_bars_trades, dollar_bars_ask, dollar_bars_bid

    def compute_time_bars(self, frequency='1T'):
        if not pd.api.types.is_datetime64_any_dtype(self.df.index):
            self.df = self.df.set_index('time')
        if not pd.api.types.is_datetime64_any_dtype(self.ask.index):
            self.ask = self.ask.set_index('time')
        if not pd.api.types.is_datetime64_any_dtype(self.bid.index):
            self.bid = self.bid.set_index('time')
        ohlc_df = self.df.resample(frequency).agg({'price': 'ohlc', 'vol': 'sum'})
        ohlc_ask = self.ask.resample(frequency).agg({'price': 'ohlc', 'vol': 'sum'})
        ohlc_bid = self.bid.resample(frequency).agg({'price': 'ohlc', 'vol': 'sum'})
        return ohlc_df, ohlc_ask, ohlc_bid

