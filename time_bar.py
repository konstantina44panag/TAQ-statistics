#!/usr/bin/env python3
import pandas as pd

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
df = df[(df["datetime"].dt.time >= pd.to_datetime("09:30:00").time()) & 
        (df["datetime"].dt.time <= pd.to_datetime("16:00:00").time())]

Ask = Ask[(Ask["datetime"].dt.time >= pd.to_datetime("09:30:00").time()) & 
          (Ask["datetime"].dt.time <= pd.to_datetime("16:00:00").time())]

Bid = Bid[(Bid["datetime"].dt.time >= pd.to_datetime("09:30:00").time()) & 
          (Bid["datetime"].dt.time <= pd.to_datetime("16:00:00").time())]

df.set_index("datetime", inplace=True)
Ask.set_index("datetime", inplace=True)
Bid.set_index("datetime", inplace=True)

#creation of time bars and the OHLC price
ohlc_df = df["price"].resample("1T").ohlc()
ohlc_Ask = Ask["price"].resample("1T").ohlc()
ohlc_Bid = Bid["price"].resample("1T").ohlc()
print(ohlc_df)
print(ohlc_Ask)
print(ohlc_Bid)

#alternative for time bar creation
ohlc_df = df.groupby(pd.Grouper(freq='1min')).agg({'price': 'ohlc', 'vol': 'sum'})
ohlc_Ask=Ask.groupby(pd.Grouper(freq='1min')).agg({'price': 'ohlc', 'vol': 'sum'})
ohlc_Bid=Bid.groupby(pd.Grouper(freq='1min')).agg({'price': 'ohlc', 'vol': 'sum'})
print(ohlc_df)
print(ohlc_Ask)
print(ohlc_Bid)

df.reset_index(inplace=True)
Ask.reset_index(inplace=True)
Bid.reset_index(inplace=True)