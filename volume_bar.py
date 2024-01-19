#!/usr/bin/env python3
import pandas as pd
import numpy as np


# for integer number of bars
def bar(x, y):
    return np.int64(x / y) * y


# Read data
df = pd.read_csv("/home/konstantina/ctm/trades_data.csv")
df = df[["TIME_M", "PRICE", "SIZE"]].rename(
    columns={"TIME_M": "time", "PRICE": "price", "SIZE": "vol"}
)

df2 = pd.read_csv("/home/konstantina/complete_nbbo/quotes_data.csv")
Ask = df2[["TIME_M", "BEST_ASK", "Best_AskSizeShares"]].rename(
    columns={"TIME_M": "time", "BEST_ASK": "price", "Best_AskSizeShares": "vol"}
)
Bid = df2[["TIME_M", "BEST_BID", "Best_BidSizeShares"]].rename(
    columns={"TIME_M": "time", "BEST_BID": "price", "Best_BidSizeShares": "vol"}
)

# Convert 'time' to datetime
df["datetime"] = pd.to_datetime(df["time"], format="%H:%M:%S.%f", errors="coerce")
Ask["datetime"] = pd.to_datetime(Ask["time"], format="%H:%M:%S.%f", errors="coerce")
Bid["datetime"] = pd.to_datetime(Bid["time"], format="%H:%M:%S.%f", errors="coerce")

# Filter for time between 09:30:00 and 16:00:00 (inclusive)
df = df[
    (df["datetime"].dt.time >= pd.to_datetime("09:30:00").time())
    & (df["datetime"].dt.time <= pd.to_datetime("16:00:00").time())
]

Ask = Ask[
    (Ask["datetime"].dt.time >= pd.to_datetime("09:30:00").time())
    & (Ask["datetime"].dt.time <= pd.to_datetime("16:00:00").time())
]

Bid = Bid[
    (Bid["datetime"].dt.time >= pd.to_datetime("09:30:00").time())
    & (Bid["datetime"].dt.time <= pd.to_datetime("16:00:00").time())
]

df.set_index("datetime", inplace=True)
Ask.set_index("datetime", inplace=True)
Bid.set_index("datetime", inplace=True)
print(df)

# volume bars
volume_threshold = 200000

volume_bars_trades = df.groupby(bar(np.cumsum(df["vol"]), volume_threshold)).agg(
    {"price": "ohlc", "vol": "sum"}
)
print(volume_bars_trades)
volume_bars_Ask = Ask.groupby(bar(np.cumsum(Ask["vol"]), volume_threshold)).agg(
    {"price": "ohlc", "vol": "sum"}
)
print(volume_bars_Ask)
volume_bars_Bid = Bid.groupby(bar(np.cumsum(Bid["vol"]), volume_threshold)).agg(
    {"price": "ohlc", "vol": "sum"}
)
print(volume_bars_Bid)
