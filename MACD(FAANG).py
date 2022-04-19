
import yfinance as yf
tickers = ["AMZN", "GOOG", "MSFT", "AAPL", "FB", "NFLX"]
ohlcv_data = {}

for ticker in tickers:
    data = yf.download(ticker,period='1mo', interval='15m')
    data.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = data
     

#MACD Line: (12-day EMA - 26-day EMA)

def MACD(DF, a=12,b=26,c=9):
    df = DF.copy()
    df["ma_fast"] = df["Adj Close"].ewm(span=a, min_periods=a).mean()
    df["ma_slow"] = df["Adj Close"].ewm(span=b, min_periods=b).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = df["macd"].ewm(span=c, min_periods=c).mean()
    return df.loc[:,["macd", "signal"]]
    
for ticker in ohlcv_data:
    ohlcv_data[ticker][["MACD", "SIGNAL"]] = MACD(ohlcv_data[ticker])
    
