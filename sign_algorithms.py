#!/usr/bin/env python3
"""This script processes trade and quote data and finds the Trade sign according to various classification algorithms, following Jukartis (2020)."""
import datetime
import pandas as pd
from classifytrades import TradeClassification
# Set the maximum number of rows to display
pd.set_option('display.max_rows', 500)


TRADES_DATA_PATH = "/home/konstantina/ctm/trades_data.csv"
QUOTES_DATA_PATH = "/home/konstantina/complete_nbbo/quotes_data.csv"


# Function to handle both formats of time
def handle_time_format(time_col):
    time_col = pd.to_datetime(time_col, format="%H:%M:%S.%f", errors="coerce")
    missing = time_col.isna()
    time_col[missing] = pd.to_datetime(
        time_col[missing], format="%H:%M:%S", errors="coerce"
    ).dt.time
    return time_col.dt.time


# Function to convert time to seconds since midnight
def time_to_seconds(t):
    return (t.hour * 3600 + t.minute * 60 + t.second) + t.microsecond / 1e6


# Read and process trade data
df = pd.read_csv(TRADES_DATA_PATH)
df = df[["TIME_M", "PRICE", "SIZE"]].rename(
    columns={"TIME_M": "time", "PRICE": "price", "SIZE": "vol"}
)
df["time"] = handle_time_format(df["time"])
df = df[df["time"] >= datetime.time(9, 30)]

# Read and process quote data
df2 = pd.read_csv(QUOTES_DATA_PATH)
Ask = df2[["TIME_M", "BEST_ASK", "Best_AskSizeShares"]].rename(
    columns={"TIME_M": "time", "BEST_ASK": "price", "Best_AskSizeShares": "vol"}
)
Bid = df2[["TIME_M", "BEST_BID", "Best_BidSizeShares"]].rename(
    columns={"TIME_M": "time", "BEST_BID": "price", "Best_BidSizeShares": "vol"}
)
Ask["time"] = handle_time_format(Ask["time"])
Bid["time"] = handle_time_format(Bid["time"])
Ask = Ask[Ask["time"] >= datetime.time(9, 30)]
Bid = Bid[Bid["time"] >= datetime.time(9, 30)]

# Reset the indices for Ask and Bid DataFrames
df.reset_index(drop=True, inplace=True)
Ask.reset_index(drop=True, inplace=True)
Bid.reset_index(drop=True, inplace=True)

# Convert 'time' to seconds since midnight for TradeClassification
df["time"] = df["time"].apply(time_to_seconds)
Ask["time"] = Ask["time"].apply(time_to_seconds)
Bid["time"] = Bid["time"].apply(time_to_seconds)

print(df.head(100))
print(Ask.head(100))
print(Bid.head(100))


tc = TradeClassification(df, Ask=Ask, Bid=Bid)
tc.classify(method="bvc", freq=0, reduce_precision=True)

print(tc.df_tr.head(200))


# Function to Convert Seconds to Time Format
def seconds_to_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return "{:02d}:{:02d}:{:06.3f}".format(hours, minutes, seconds)


tc.df_tr["regular_timestamp"] = tc.df_tr["time_org"].apply(seconds_to_time)
print(tc.df_tr.head(200))
