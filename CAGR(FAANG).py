import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT", "AAPL", "NFLX", "FB"]
ohlcv_data = {}

for ticker in tickers:
    data = yf.download(ticker, period='7mo', interval='1d')
    data.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = data


def CAGR(DF):
    df = DF.copy()
    df = df.copy()
    df['return'] = df["Adj Close"].pct_change()
    df['comp_return'] = (1 + df['return']).cumprod()
    n = len(df) / 252
    CAGR = (df['comp_return'][-1]) ** (1 / n) - 1
    return CAGR


for ticker in ohlcv_data:
    print("CAGR for {} = {}".format(ticker, CAGR(ohlcv_data[ticker])))
