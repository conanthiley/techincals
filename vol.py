import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT", "AAPL", "NFLX", "FB"]
ohlcv_data = {}

for ticker in tickers:
    data = yf.download(ticker, period='7mo', interval='1d')
    data.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = data


def volatility(DF):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    vol = df['return'].std() * np.sqrt(252)
    return vol


for ticker in ohlcv_data:
    print("Vol for {} = {}".format(ticker, volatility(ohlcv_data[ticker])))