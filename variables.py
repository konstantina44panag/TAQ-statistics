#!/usr/bin/env python3
import pandas as pd
import numpy as np
import subprocess

# create 1-minute time bars
subprocess.run(["python3", "preparation.py"])
from preparation import df, Ask, Bid

# 1,2,3
# Find the last trade price, volume, and timestamp
trades_1min = df.resample("1T", on="time").agg(
    {"price": "last", "vol": "last", "time": "last"}
)

asks_1min = Ask.resample("1T", on="time").agg(
    {"price": "last", "vol": "last", "time": "last"}
)

bids_1min = Bid.resample("1T", on="time").agg(
    {"price": "last", "vol": "last", "time": "last"}
)

# Rename columns
trades_1min.rename(
    columns={
        "price": "last_trade_price",
        "vol": "last_trade_vol",
        "time": "last_trade_time",
    },
    inplace=True,
)
asks_1min.rename(
    columns={
        "price": "last_trade_price",
        "vol": "last_trade_vol",
        "time": "last_trade_time",
    },
    inplace=True,
)
bids_1min.rename(
    columns={
        "price": "last_trade_price",
        "vol": "last_trade_vol",
        "time": "last_trade_time",
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


aggr_trades_1min = df.resample("1T", on="time").apply(custom_agg_function)
aggr_trades_1min = aggr_trades_1min.rename("aggressive trade price")
print(aggr_trades_1min)
agrr_ask_1min= Ask.resample("1T", on="time").apply(custom_agg_function)
agrr_ask_1min = agrr_ask_1min.rename("aggressive ask price")
print(agrr_ask_1min)
agrr_bid_1min= Bid.resample("1T", on="time").apply(custom_agg_function)
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


vwap_trades_1min = df.resample("1T", on="time").apply(custom_agg_function)
vwap_trades_1min = vwap_trades_1min.rename("volume_weighted_price")

vwap_asks_1min = Ask.resample("1T", on="time").agg(custom_agg_function)
vwap_asks_1min = vwap_asks_1min.rename("volume_weighted_price")

vwap_bids_1min = Bid.resample("1T", on="time").agg(custom_agg_function)
vwap_bids_1min = vwap_bids_1min.rename("volume_weighted_price")

print(vwap_trades_1min)
print(vwap_asks_1min)
print(vwap_bids_1min)


# 6
average_trades_1min = df.resample("1T", on="time").agg({"price": "mean"})
average_asks_1min = Ask.resample("1T", on="time").agg({"price": "mean"})
average_bids_1min = Bid.resample("1T", on="time").agg({"price": "mean"})

# Rename the columns for clarity
average_trades_1min = average_trades_1min.rename(columns={"price": "mean_price"})
average_asks_1min = average_asks_1min.rename(columns={"price": "mean_price"})
average_bids_1min = average_bids_1min.rename(columns={"price": "mean_price"})

print(average_trades_1min)
print(average_asks_1min)
print(average_bids_1min)

# 7
# Reset the indices for Ask and Bid DataFrames
merged_df = pd.merge_asof(df, Ask, on='time', direction='backward', suffixes=('', '_ask'))
merged_df = pd.merge_asof(merged_df, Bid, on='time', direction='backward', suffixes=('', '_bid'))

merged_df['weighted_bid'] = merged_df['price_bid'] * merged_df['vol']
merged_df['weighted_ask'] = merged_df['price_ask'] * merged_df['vol']
merged_df.set_index('time', inplace=True)
merged_df.index = pd.to_datetime(merged_df.index)

aggregation_rules = {
    'price': 'mean',  # Taking the mean of the trade price
    'vol': 'sum',     # Summing up the trade volumes
    'weighted_bid': 'sum',  # Summing up the weighted bid values
    'weighted_ask': 'sum',  # Summing up the weighted ask values
    'price_bid': 'mean',    # Taking the mean of the bid prices
    'price_ask': 'mean'     # Taking the mean of the ask prices
}

# Resample and aggregate according to the defined rules
one_minute_bins = merged_df.resample('1T').agg(aggregation_rules)

# Calculate VWAP for each 1-minute bin
one_minute_bins['vwap_bid'] = one_minute_bins['weighted_bid'] / one_minute_bins['vol']
one_minute_bins['vwap_ask'] = one_minute_bins['weighted_ask'] / one_minute_bins['vol']
print(one_minute_bins)

post_trade_merged = pd.merge_asof(df.sort_values('time'), Ask.sort_values('time'), on='time', direction='forward', suffixes=('', '_ask'))
post_trade_merged = pd.merge_asof(post_trade_merged, Bid.sort_values('time'), on='time', direction='forward', suffixes=('', '_bid'))
post_trade_merged['weighted_price_bid'] = post_trade_merged['price_bid'] * post_trade_merged['vol']
post_trade_merged['weighted_price_ask'] = post_trade_merged['price_ask'] * post_trade_merged['vol']
aggregation_rules = {
    'weighted_price_bid': 'sum',
    'weighted_price_ask': 'sum',
    'vol': 'sum'
}

one_minute_bins_post = post_trade_merged.resample('1T', on='time').agg(aggregation_rules)
one_minute_bins_post['vwap_bid'] = one_minute_bins_post['weighted_price_bid'] / one_minute_bins_post['vol']
one_minute_bins_post['vwap_ask'] = one_minute_bins_post['weighted_price_ask'] / one_minute_bins_post['vol']
print(one_minute_bins_post)



# 8



# 9
df_resampled = df.resample("1T", on="time").agg({"vol": "sum"})
print(df_resampled)
Ask_resampled = Ask.resample("1T", on="time").agg({"vol": "sum"})
print(Ask_resampled)
Bid_resampled = Bid.resample("1T", on="time").agg({"vol": "sum"})
print(Bid_resampled)


# 10
def count_changes(series):
    price_changes = series.diff()
    num_changes = (price_changes != 0).sum()
    return num_changes


trades_changes = df.resample("1T", on="time").apply(
    {"price": count_changes, "vol": count_changes}
)
Ask_changes = Ask.resample("1T", on="time").apply(
    {"price": count_changes, "vol": count_changes}
)
Bid_changes = Bid.resample("1T", on="time").apply(
    {"price": count_changes, "vol": count_changes}
)
print(trades_changes)
print(Ask_changes)
print(Bid_changes)
