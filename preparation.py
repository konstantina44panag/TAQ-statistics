#!/usr/bin/env python3
import pandas as pd
import numpy as np
import datetime
import subprocess

subprocess.run(["python3", "sign_algorithms.py"])
from sign_algorithms import tradessigns

TRADES_DATA_PATH = "/home/konstantina/ctm/trades_data.csv"
QUOTES_DATA_PATH = "/home/konstantina/complete_nbbo/quotes_data.csv"


# Read and process trade data
df = pd.read_csv(TRADES_DATA_PATH)
buys_df = tradessigns[tradessigns['Initiator'] == 1]
sells_df = tradessigns[tradessigns['Initiator'] == -1]
df = df[["TIME_M", "PRICE", "SIZE"]].rename(
    columns={"TIME_M": "time", "PRICE": "price", "SIZE": "vol"}
)
buys_df=buys_df[["regular_timestamp", "price", "vol"]].rename(
    columns={"regular_timestamp": "time"}
)
sells_df=sells_df[["regular_timestamp", "price", "vol"]].rename(
    columns={"regular_timestamp": "time"}
)
# Read and process quote data
df2 = pd.read_csv(QUOTES_DATA_PATH)
Ask = df2[["TIME_M", "BEST_ASK", "Best_AskSizeShares"]].rename(
    columns={"TIME_M": "time", "BEST_ASK": "price", "Best_AskSizeShares": "vol"}
)
Bid = df2[["TIME_M", "BEST_BID", "Best_BidSizeShares"]].rename(
    columns={"TIME_M": "time", "BEST_BID": "price", "Best_BidSizeShares": "vol"}
)



df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S.%f", errors="coerce")
buys_df["time"] = pd.to_datetime(buys_df["time"], format="%H:%M:%S.%f", errors="coerce")
sells_df["time"] = pd.to_datetime(sells_df["time"], format="%H:%M:%S.%f", errors="coerce")
Ask["time"] = pd.to_datetime(Ask["time"], format="%H:%M:%S.%f", errors="coerce")
Bid["time"] = pd.to_datetime(Bid["time"], format="%H:%M:%S.%f", errors="coerce")


start_time = pd.to_datetime("09:30:00", format="%H:%M:%S")
end_time = pd.to_datetime("16:00:00", format="%H:%M:%S")

df = df[(df["time"] >= start_time) & (df["time"] < end_time)]
buys_df = buys_df[(buys_df["time"] >= start_time) & (buys_df["time"] < end_time)]
sells_df = sells_df[(sells_df["time"] >= start_time) & (sells_df["time"] < end_time)]
Ask = Ask[(Ask["time"] >= start_time) & (Ask["time"] < end_time)]
Bid = Bid[(Bid["time"] >= start_time) & (Bid["time"] < end_time)]


df = df.dropna(subset=["time"])
buys_df = buys_df.dropna(subset=["time"])
sells_df = sells_df.dropna(subset=["time"])
Ask = Ask.dropna(subset=["time"])
Bid=Bid.dropna(subset=["time"])

