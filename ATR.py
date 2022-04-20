
import yfinance as yf
tickers = ["AMZN", "GOOG", "MSFT", "AAPL", "NFLX", "FB"]
ohlcv_data = {}

for ticker in tickers:
    data = yf.download(ticker,period='1mo', interval='5m')
    data.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = data
    
#The Current Period High - Current Period Low
#The Absolute Value (abs) of the Current Period High - (The Previous Period Close)
#The Absolute Value (abs) of the Current Period Low - (The Previous Period Close)
#true range = max[(high - low), abs(high - previous close), abs (low - previous close)]

def ATR(DF, n=14):
    df = DF.copy()
    df['H-L'] = df["High"] - df["Low"]
    df['H-PC'] = df["High"] - df["Adj Close"].shift(1)
    df['L-PC'] = df["Low"] - df["Adj Close"].shift(1)
    df['TR'] = df[["H-L","H-PC", "L-PC"]].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].ewm(com=n, min_periods=n).mean()
    return df['ATR']

for ticker in ohlcv_data:
    ohlcv_data[ticker]['ATR'] = ATR(ohlcv_data[ticker])