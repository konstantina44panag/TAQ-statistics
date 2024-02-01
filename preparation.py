#!/usr/bin/env python3
"""This script prepares the datasets to be implemented on algorithms for trade signs and estimation of variables."""
import pandas as pd
import datetime
from bar_analysis import MarketBars
from sign_algorithms import TradeAnalyzer
import datetime

# Set the maximum number of rows to display
pd.set_option('display.max_rows', 500)

TRADES_DATA_PATH = "/home/konstantina/ctm/trades_data.csv"
QUOTES_DATA_PATH = "/home/konstantina/complete_nbbo/quotes_data.csv"

# Preparation for the tradesign algorithm
def handle_time_format(time_col):
    time_col = pd.to_datetime(time_col, format="%H:%M:%S.%f", errors="coerce")
    missing = time_col.isna()
    time_col[missing] = pd.to_datetime(
        time_col[missing], format="%H:%M:%S", errors="coerce"
    ).dt.time
    return time_col.dt.time

def time_to_seconds(t):
    return (t.hour * 3600 + t.minute * 60 + t.second) + t.microsecond / 1e6


# Read and process trade data
trades = pd.read_csv(TRADES_DATA_PATH)
trades = trades[["TIME_M", "PRICE", "SIZE"]].rename(
    columns={"TIME_M": "regular_time", "PRICE": "price", "SIZE": "vol"}
)


trades2 = pd.read_csv(QUOTES_DATA_PATH)
Ask = trades2[["TIME_M", "BEST_ASK", "Best_AskSizeShares"]].rename(
    columns={"TIME_M": "regular_time", "BEST_ASK": "price", "Best_AskSizeShares": "vol"}
)
Bid = trades2[["TIME_M", "BEST_BID", "Best_BidSizeShares"]].rename(
    columns={"TIME_M": "regular_time", "BEST_BID": "price", "Best_BidSizeShares": "vol"}
)

trades["regular_time"] = handle_time_format(trades["regular_time"])
Ask["regular_time"] = handle_time_format(Ask["regular_time"])
Bid["regular_time"] = handle_time_format(Bid["regular_time"])
trades = trades[(trades["regular_time"] >= datetime.time(9, 29)) & (trades["regular_time"] <= datetime.time(16, 0))]
Ask = Ask[(Ask["regular_time"] >= datetime.time(9, 29)) & (Ask["regular_time"] <= datetime.time(16, 0))]
Bid = Bid[(Bid["regular_time"] >= datetime.time(9, 29)) & (Bid["regular_time"] <= datetime.time(16, 0))]

trades.reset_index(drop=True, inplace=True)
Ask.reset_index(drop=True, inplace=True)
Bid.reset_index(drop=True, inplace=True)

trades["time"] = trades["regular_time"].apply(time_to_seconds)
Ask["time"] = Ask["regular_time"].apply(time_to_seconds)
Bid["time"] = Bid["regular_time"].apply(time_to_seconds)

trades['vol'] = trades['vol'].astype(int)
Ask['vol'] = Ask['vol'].astype(int)
Bid['vol'] = Bid['vol'].astype(int)

analyzer = TradeAnalyzer(trades, Ask, Bid)
tradessigns = analyzer.classify_trades()

tradessigns = tradessigns[(tradessigns["regular_time"] >= datetime.time(9, 30))]
tradessigns.to_csv("/home/konstantina/Statistics_Taq/test/tradessigns_lr.csv", index=True)

print(tradessigns)

trades = trades[["regular_time", "price", "vol"]].rename(columns={"regular_time": "time"})
Ask = Ask[["regular_time", "price", "vol"]].rename(columns={"regular_time": "time"})
Bid = Bid[["regular_time", "price", "vol"]].rename(columns={"regular_time": "time"})
trades = trades[(trades["time"] >= datetime.time(9, 30))]
Ask = Ask[(Ask["time"] >= datetime.time(9, 30))]
Bid= Bid[(Bid["time"] >= datetime.time(9, 30))]
Buys_trades = tradessigns[tradessigns['Initiator'] == 1][["regular_time", "price", "vol"]] \
    .rename(columns={"regular_time": "time"})
Sells_trades = tradessigns[tradessigns['Initiator'] == -1][["regular_time", "price", "vol"]] \
    .rename(columns={"regular_time": "time"})

trades = trades.dropna(subset=["time"])
Buys_trades = Buys_trades.dropna(subset=["time"])
Sells_trades = Sells_trades.dropna(subset=["time"]) 
Ask = Ask.dropna(subset=["time"])
Bid = Bid.dropna(subset=["time"])

trades["time"] = pd.to_datetime(trades["time"], format="%H:%M:%S.%f", errors="coerce")
Buys_trades["time"] = pd.to_datetime(Buys_trades["time"], format="%H:%M:%S.%f", errors="coerce")
Sells_trades["time"] = pd.to_datetime(Sells_trades["time"], format="%H:%M:%S.%f", errors="coerce")
Ask["time"] = pd.to_datetime(Ask["time"], format="%H:%M:%S.%f", errors="coerce")
Bid["time"] = pd.to_datetime(Bid["time"], format="%H:%M:%S.%f", errors="coerce")


#Create time_bars, volume_bars, dollar_bars
market_bars = MarketBars(trades, Ask, Bid, 200000, 2500000)
volume_bars_trades, volume_bars_ask, volume_bars_bid = market_bars.compute_volume_bars()
dollar_bars_trades, dollar_bars_ask, dollar_bars_bid = market_bars.compute_dollar_bars()
ohlc_trades, ohlc_ask, ohlc_bid = market_bars.compute_time_bars()

# Export each DataFrame to a CSV file
volume_bars_trades.to_csv("/home/konstantina/Statistics_Taq/output/volume_bars_trades.csv", index=True)
volume_bars_ask.to_csv("/home/konstantina/Statistics_Taq/output/volume_bars_ask.csv", index=True)
volume_bars_bid.to_csv("/home/konstantina/Statistics_Taq/output/volume_bars_bid.csv", index=True)
dollar_bars_trades.to_csv("/home/konstantina/Statistics_Taq/output/dollar_bars_trades.csv", index=True)
dollar_bars_ask.to_csv("/home/konstantina/Statistics_Taq/output/dollar_bars_ask.csv", index=True)
dollar_bars_bid.to_csv("/home/konstantina/Statistics_Taq/output/dollar_bars_bid.csv", index=True)
ohlc_trades.to_csv("/home/konstantina/Statistics_Taq/output/ohlc_trades.csv", index=True)
ohlc_ask.to_csv("/home/konstantina/Statistics_Taq/output/ohlc_asks.csv", index=True)
ohlc_bid.to_csv("/home/konstantina/Statistics_Taq/output/ohlc_bids.csv", index=True)