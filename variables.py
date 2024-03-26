#!/usr/bin/env python3
"""This script computes important variables."""

import pandas as pd
import numpy as np
import subprocess

subprocess.run(["python3", "preparation.py"])
from preparation import trades, Buys_trades, Sells_trades, Ask, Bid


#1,2,3. The last trade/bid/ask price, volume, and timestamp
trades_1min = trades.resample("1T", on="time").agg(
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
        "price": "last_ask_price",
        "vol": "last_ask_vol",
        "time": "last_ask_time",
    },
    inplace=True,
)
bids_1min.rename(
    columns={
        "price": "last_bid_price",
        "vol": "last_bid_vol",
        "time": "last_bid_time",
    },
    inplace=True,
)

trades_1min["last_trade_time"] = trades_1min["last_trade_time"].dt.strftime("%H:%M:%S.%f")
asks_1min["last_ask_time"] = asks_1min["last_ask_time"].dt.strftime("%H:%M:%S.%f")
bids_1min["last_bid_time"] = bids_1min["last_bid_time"].dt.strftime("%H:%M:%S.%f")
trades_1min.to_csv("/home/konstantina/Statistics_Taq/output/trades_123.csv", index=True)
asks_1min.to_csv("/home/konstantina/Statistics_Taq/output/asks_123.csv", index=True)
bids_1min.to_csv("/home/konstantina/Statistics_Taq/output/bids_123.csv", index=True)

#4.Last price at which an aggressive buy/sell order for $10,000 would execute
Buys_trades["value"] = Buys_trades["price"] * Buys_trades["vol"]
Sells_trades["value"] = Sells_trades["price"] * Sells_trades["vol"]
def custom_agg_function(data):
    filtered_trades = data[data["value"] >= 10000]
    if not filtered_trades.empty:
        return filtered_trades.iloc[-1]["price"]
    else:
        return np.nan


aggr_buys_1min = Buys_trades.resample("1T", on="time").apply(custom_agg_function)
aggr_buys_1min = aggr_buys_1min.rename("aggressive buyer's price")
agrr_sells_1min= Sells_trades.resample("1T", on="time").apply(custom_agg_function)
agrr_sells_1min = agrr_sells_1min.rename("aggressive seller's price")

aggr_buys_1min.to_csv("/home/konstantina/Statistics_Taq/output/buys_4.csv", index=True)
agrr_sells_1min.to_csv("/home/konstantina/Statistics_Taq/output/sells_4.csv", index=True)

#5.VWAP of trades (and separately buys/sells) over interval
def custom_agg_function(data):
    weighted_prices = (data["price"] * data["vol"]).sum()
    total_volume = data["vol"].sum()

    if total_volume == 0:
        return 0.0
    else:
        return weighted_prices / total_volume


vwap_trades_1min = trades.resample("1T", on="time").apply(custom_agg_function)
vwap_trades_1min = vwap_trades_1min.rename("volume_weighted_price")

vwap_buys_1min = Buys_trades.resample("1T", on="time").agg(custom_agg_function)
vwap_buys_1min = vwap_buys_1min.rename("volume_weighted_price")

vwap_sells_1min = Sells_trades.resample("1T", on="time").agg(custom_agg_function)
vwap_sells_1min = vwap_sells_1min.rename("volume_weighted_price")

vwap_trades_1min.to_csv("/home/konstantina/Statistics_Taq/output/trades_5.csv", index=True)
vwap_buys_1min.to_csv("/home/konstantina/Statistics_Taq/output/buys_5.csv", index=True)
vwap_sells_1min.to_csv("/home/konstantina/Statistics_Taq/output/sells_5.csv", index=True)

#6. Simple average of trade prices (and separately buys/sells) over interval
average_trades_1min = trades.resample("1T", on="time").agg({"price": "mean"})
average_buys_1min = Buys_trades.resample("1T", on="time").agg({"price": "mean"})
average_sells_1min = Sells_trades.resample("1T", on="time").agg({"price": "mean"})

# Rename the columns 
average_trades_1min = average_trades_1min.rename(columns={"price": "mean_price"})
average_buys_1min = average_buys_1min.rename(columns={"price": "mean_price"})
average_sells_1min = average_sells_1min.rename(columns={"price": "mean_price"})

average_trades_1min.to_csv("/home/konstantina/Statistics_Taq/output/trades_6.csv", index=True)
average_buys_1min.to_csv("/home/konstantina/Statistics_Taq/output/buys_6.csv", index=True)
average_sells_1min.to_csv("/home/konstantina/Statistics_Taq/output/sells_6.csv", index=True)

#7. Volume weighted average pre/post-trade bid/ask prices (measured just before each trade and weighted by the size of each trade)

merged_trades = pd.merge_asof(trades, Ask, on='time', direction='backward', suffixes=('', '_ask'))
merged_trades = pd.merge_asof(merged_trades, Bid, on='time', direction='backward', suffixes=('', '_bid'))

merged_trades['weighted_bid'] = merged_trades['price_bid'] * merged_trades['vol']
merged_trades['weighted_ask'] = merged_trades['price_ask'] * merged_trades['vol']
merged_trades.set_index('time', inplace=True)
merged_trades.index = pd.to_datetime(merged_trades.index)

aggregation_rules = {
    'price': 'mean',  
    'vol': 'sum',   
    'weighted_bid': 'sum',  
    'weighted_ask': 'sum',  
    'price_bid': 'mean',   
    'price_ask': 'mean'     
}

one_minute_bins = merged_trades.resample('1T').agg(aggregation_rules)

one_minute_bins['vwap_bid'] = one_minute_bins['weighted_bid'] / one_minute_bins['vol']
one_minute_bins['vwap_ask'] = one_minute_bins['weighted_ask'] / one_minute_bins['vol']

one_minute_bins.to_csv("/home/konstantina/Statistics_Taq/output/pretrades_7.csv", index=True)

post_merged_trades = pd.merge_asof(trades, Ask, on='time', direction='forward', suffixes=('', '_ask'))
post_merged_trades = pd.merge_asof(post_merged_trades, Bid, on='time', direction='forward', suffixes=('', '_bid'))

post_merged_trades['weighted_bid'] = post_merged_trades['price_bid'] * post_merged_trades['vol']
post_merged_trades['weighted_ask'] = post_merged_trades['price_ask'] * post_merged_trades['vol']
aggregation_rules = {
    'price': 'mean',  
    'vol': 'sum',   
    'weighted_bid': 'sum',  
    'weighted_ask': 'sum',  
    'price_bid': 'mean',   
    'price_ask': 'mean'     
}

one_minute_bins_post = post_merged_trades.resample('1T', on='time').agg(aggregation_rules)
one_minute_bins_post['vwap_bid'] = one_minute_bins_post['weighted_bid'] / one_minute_bins_post['vol']
one_minute_bins_post['vwap_ask'] = one_minute_bins_post['weighted_ask'] / one_minute_bins_post['vol']

one_minute_bins_post.to_csv("/home/konstantina/Statistics_Taq/output/posttrades_7.csv", index=True)


#8. Time weighted version of bid/ask prices and size (in dollars) of best bid and ask 
def calculate_twap_and_volume(group):
    durations = group.index.to_series().diff().fillna(pd.Timedelta(seconds=0)).dt.total_seconds()
    time_weighted_prices = group['price'] * durations
    time_weighted_volumes = group['vol'] * durations
    total_time = durations.sum()
    twap = time_weighted_prices.sum() / total_time if total_time != 0 else 0
    twav = time_weighted_volumes.sum() / total_time if total_time != 0 else 0

    return pd.Series({'TWAP': twap, 'TWAV': twav})

trades.set_index('time', inplace=True)
Ask.set_index('time', inplace=True)
Bid.set_index('time', inplace=True)
twap_trades = trades.resample('1T').apply(calculate_twap_and_volume)
twap_asks = Ask.resample('1T').apply(calculate_twap_and_volume)
twap_bids = Bid.resample('1T').apply(calculate_twap_and_volume)

twap_trades.to_csv("/home/konstantina/Statistics_Taq/output/trades_8.csv", index=True)
twap_asks.to_csv("/home/konstantina/Statistics_Taq/output/asks_8.csv", index=True)
twap_bids.to_csv("/home/konstantina/Statistics_Taq/output/bids_8.csv", index=True)


#9. Total Volume traded over interval
if trades.index.name == 'time':
    trades.reset_index(inplace=True)

if Ask.index.name == 'time':
    Ask.reset_index(inplace=True)

if Bid.index.name == 'time':
    Bid.reset_index(inplace=True)
    
trades_resampled = trades.resample("1T", on="time").agg({"vol": "sum"})
Buys_trades_resampled = Buys_trades.resample("1T", on="time").agg({"vol": "sum"})
Sells_trades_resampled = Sells_trades.resample("1T", on="time").agg({"vol": "sum"})
Ask_resampled = Ask.resample("1T", on="time").agg({"vol": "sum"})
Bid_resampled = Bid.resample("1T", on="time").agg({"vol": "sum"})

trades_resampled.to_csv("/home/konstantina/Statistics_Taq/output/trades_9.csv", index=True)
Buys_trades_resampled.to_csv("/home/konstantina/Statistics_Taq/output/trades_9.csv", index=True)
Sells_trades_resampled.to_csv("/home/konstantina/Statistics_Taq/output/trades_9.csv", index=True)
Ask_resampled.to_csv("/home/konstantina/Statistics_Taq/output/asks_9.csv", index=True)
Bid_resampled.to_csv("/home/konstantina/Statistics_Taq/output/bids_9.csv", index=True)


#10. Number of bid/ask price/volume changes over interval
def count_changes(series):
    price_changes = series.diff()
    num_changes = (price_changes != 0).sum()
    return num_changes


trades_changes = trades.resample("1T", on="time").apply(
    {"price": count_changes, "vol": count_changes}
)
Ask_changes = Ask.resample("1T", on="time").apply(
    {"price": count_changes, "vol": count_changes}
)
Bid_changes = Bid.resample("1T", on="time").apply(
    {"price": count_changes, "vol": count_changes}
)

trades_changes.to_csv("/home/konstantina/Statistics_Taq/output/trades_10.csv", index=True)
Ask_changes.to_csv("/home/konstantina/Statistics_Taq/output/asks_10.csv", index=True)
Bid_changes.to_csv("/home/konstantina/Statistics_Taq/output/bids_10.csv", index=True)

subprocess.run("gzip /home/konstantina/Statistics_Taq/output/*.csv", shell=True)
