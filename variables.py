#!/usr/bin/env python3
import pandas as pd
import numpy as np
import subprocess

subprocess.run(["python3", "preparation.py"])
from preparation import df, buys_df, sells_df, Ask, Bid


#1,2,3. The last trade/bid/ask price, volume, and timestamp
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

#4.Last price at which an aggressive buy/sell order for $10,000 would execute
buys_df["value"] = buys_df["price"] * buys_df["vol"]
sells_df["value"] = sells_df["price"] * sells_df["vol"]
def custom_agg_function(data):
    filtered_trades = data[data["value"] >= 10000]
    if not filtered_trades.empty:
        return filtered_trades.iloc[-1]["price"]
    else:
        return np.nan


aggr_buys_1min = buys_df.resample("1T", on="time").apply(custom_agg_function)
aggr_buys_1min = aggr_buys_1min.rename("aggressive buyer's price")
agrr_sells_1min= sells_df.resample("1T", on="time").apply(custom_agg_function)
agrr_sells_1min = agrr_sells_1min.rename("aggressive seller's price")
print(aggr_buys_1min)
print(agrr_sells_1min)


#5.VWAP of trades (and separately buys/sells) over interval
def custom_agg_function(data):
    weighted_prices = (data["price"] * data["vol"]).sum()
    total_volume = data["vol"].sum()

    if total_volume == 0:
        return 0.0
    else:
        return weighted_prices / total_volume


vwap_trades_1min = df.resample("1T", on="time").apply(custom_agg_function)
vwap_trades_1min = vwap_trades_1min.rename("volume_weighted_price")

vwap_buys_1min = buys_df.resample("1T", on="time").agg(custom_agg_function)
vwap_buys_1min = vwap_buys_1min.rename("volume_weighted_price")

vwap_sells_1min = sells_df.resample("1T", on="time").agg(custom_agg_function)
vwap_sells_1min = vwap_sells_1min.rename("volume_weighted_price")

print(vwap_trades_1min)
print(vwap_buys_1min)
print(vwap_sells_1min)


#6. Simple average of trade prices (and separately buys/sells) over interval
average_trades_1min = df.resample("1T", on="time").agg({"price": "mean"})
average_buys_1min = buys_df.resample("1T", on="time").agg({"price": "mean"})
average_sells_1min = sells_df.resample("1T", on="time").agg({"price": "mean"})

# Rename the columns 
average_trades_1min = average_trades_1min.rename(columns={"price": "mean_price"})
average_buys_1min = average_buys_1min.rename(columns={"price": "mean_price"})
average_sells_1min = average_sells_1min.rename(columns={"price": "mean_price"})

print(average_trades_1min)
print(average_buys_1min)
print(average_sells_1min)

#7. Volume weighted average pre/post-trade bid/ask prices (measured just before each trade and weighted by the size of each trade)

merged_df = pd.merge_asof(df, Ask, on='time', direction='backward', suffixes=('', '_ask'))
merged_df = pd.merge_asof(merged_df, Bid, on='time', direction='backward', suffixes=('', '_bid'))

merged_df['weighted_bid'] = merged_df['price_bid'] * merged_df['vol']
merged_df['weighted_ask'] = merged_df['price_ask'] * merged_df['vol']
merged_df.set_index('time', inplace=True)
merged_df.index = pd.to_datetime(merged_df.index)

aggregation_rules = {
    'price': 'mean',  
    'vol': 'sum',   
    'weighted_bid': 'sum',  
    'weighted_ask': 'sum',  
    'price_bid': 'mean',   
    'price_ask': 'mean'     
}

one_minute_bins = merged_df.resample('1T').agg(aggregation_rules)

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



#8. Time weighted version of bid/ask prices and size (in dollars) of best bid and ask (Holden and Jacobsen 2014)
def calculate_twap_and_volume(group):
    durations = group.index.to_series().diff().fillna(pd.Timedelta(seconds=0)).dt.total_seconds()
    time_weighted_prices = group['price'] * durations
    time_weighted_volumes = group['vol'] * durations
    total_time = durations.sum()
    twap = time_weighted_prices.sum() / total_time if total_time != 0 else 0
    twav = time_weighted_volumes.sum() / total_time if total_time != 0 else 0

    return pd.Series({'TWAP': twap, 'TWAV': twav})

df.set_index('time', inplace=True)
Ask.set_index('time', inplace=True)
Bid.set_index('time', inplace=True)
twap_trades = df.resample('1T').apply(calculate_twap_and_volume)
twap_asks = Ask.resample('1T').apply(calculate_twap_and_volume)
twap_bids = Bid.resample('1T').apply(calculate_twap_and_volume)
print(twap_trades)
print(twap_asks)
print(twap_bids)

#9. Total Volume traded over interval
if df.index.name == 'time':
    df.reset_index(inplace=True)

if Ask.index.name == 'time':
    Ask.reset_index(inplace=True)

if Bid.index.name == 'time':
    Bid.reset_index(inplace=True)
    
df_resampled = df.resample("1T", on="time").agg({"vol": "sum"})
Ask_resampled = Ask.resample("1T", on="time").agg({"vol": "sum"})
Bid_resampled = Bid.resample("1T", on="time").agg({"vol": "sum"})
print(df_resampled)
print(Ask_resampled)
print(Bid_resampled)


#10. Number of bid/ask price/volume changes over interval
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
