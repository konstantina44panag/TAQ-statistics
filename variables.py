#!/usr/bin/env python3
import pandas as pd
import numpy as np
import subprocess

# create 1-minute time bars
subprocess.run(["python3", "time_bar.py"])
from time_bar import df
from time_bar import Ask
from time_bar import Bid

# 1,2,3
# Find the last trade price, volume, and timestamp
trades_1min = df.resample("1T", on="datetime").agg(
    {"price": "last", "vol": "last", "datetime": "last"}
)

asks_1min = Ask.resample("1T", on="datetime").agg(
    {"price": "last", "vol": "last", "datetime": "last"}
)

bids_1min = Bid.resample("1T", on="datetime").agg(
    {"price": "last", "vol": "last", "datetime": "last"}
)

# Rename columns
trades_1min.rename(
    columns={
        "price": "last_trade_price",
        "vol": "last_trade_vol",
        "datetime": "last_trade_time",
    },
    inplace=True,
)
asks_1min.rename(
    columns={
        "price": "last_trade_price",
        "vol": "last_trade_vol",
        "datetime": "last_trade_time",
    },
    inplace=True,
)
bids_1min.rename(
    columns={
        "price": "last_trade_price",
        "vol": "last_trade_vol",
        "datetime": "last_trade_time",
    },
    inplace=True,
)

trades_1min["last_trade_time"] = trades_1min["last_trade_time"].dt.strftime(
    "%H:%M:%S.%f"
)
asks_1min["last_trade_time"] = asks_1min["last_trade_time"].dt.strftime("%H:%M:%S.%f")
bids_1min["last_trade_time"] = bids_1min["last_trade_time"].dt.strftime("%H:%M:%S.%f")
print(trades_1min)
print(asks_1min)
print(bids_1min)

# 4
df["value"] = df["price"] * df["vol"]
Ask["value"] = Ask["price"] * Ask["vol"]
Bid["value"] = Bid["price"] * Bid["vol"]


def custom_agg_function(data):
    filtered_trades = data[data["value"] >= 10000]
    if not filtered_trades.empty:
        return filtered_trades.iloc[-1]["price"]
    else:
        return np.nan


aggr_trades_1min = df.resample("1T", on="datetime").apply(custom_agg_function)
aggr_trades_1min = aggr_trades_1min.rename("aggressive trade price")
print(aggr_trades_1min)
agrr_ask_1min= Ask.resample("1T", on="datetime").apply(custom_agg_function)
agrr_ask_1min = agrr_ask_1min.rename("aggressive ask price")
print(agrr_ask_1min)
agrr_bid_1min= Bid.resample("1T", on="datetime").apply(custom_agg_function)
agrr_bid_1min = agrr_bid_1min.rename("aggressive ask price")
print(agrr_bid_1min)


# 5
def custom_agg_function(data):
    weighted_prices = (data["price"] * data["vol"]).sum()
    total_volume = data["vol"].sum()

    if total_volume == 0:
        # Handle the case where total_volume is zero to avoid division by zero
        return 0.0
    else:
        return weighted_prices / total_volume


vwap_trades_1min = df.resample("1T", on="datetime").apply(custom_agg_function)
vwap_trades_1min = vwap_trades_1min.rename("volume_weighted_price")

vwap_asks_1min = Ask.resample("1T", on="datetime").agg(custom_agg_function)
vwap_asks_1min = vwap_asks_1min.rename("volume_weighted_price")

vwap_bids_1min = Bid.resample("1T", on="datetime").agg(custom_agg_function)
vwap_bids_1min = vwap_bids_1min.rename("volume_weighted_price")

print(vwap_trades_1min)
print(vwap_asks_1min)
print(vwap_bids_1min)


# 6
average_trades_1min = df.resample("1T", on="datetime").agg({"price": "mean"})
average_asks_1min = Ask.resample("1T", on="datetime").agg({"price": "mean"})
average_bids_1min = Bid.resample("1T", on="datetime").agg({"price": "mean"})

# Rename the columns for clarity
average_trades_1min = average_trades_1min.rename(columns={"price": "mean_price"})
average_asks_1min = average_asks_1min.rename(columns={"price": "mean_price"})
average_bids_1min = average_bids_1min.rename(columns={"price": "mean_price"})

print(average_trades_1min)
print(average_asks_1min)
print(average_bids_1min)

# 7?


# 8?


# 9
df_resampled = df.resample("1T", on="datetime").agg({"vol": "sum"})
print(df_resampled)

# 10
def count_changes(series):
    price_changes = series.diff()
    num_changes = (price_changes != 0).sum()
    return num_changes


trades_changes = df.resample("1T", on="datetime").apply(
    {"price": count_changes, "vol": count_changes}
)
Ask_changes = Ask.resample("1T", on="datetime").apply(
    {"price": count_changes, "vol": count_changes}
)
Bid_changes = Bid.resample("1T", on="datetime").apply(
    {"price": count_changes, "vol": count_changes}
)
print(trades_changes)
print(Ask_changes)
print(Bid_changes)
