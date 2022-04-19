import yfinance as yf
tickers = ["AMZN", "GOOG", "MSFT", "AAPL", "NFLX", "FB"]
ohlcv_data = {}

for ticker in tickers:
    data = yf.download(ticker,period='1mo', interval='15m')
    data.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = data
    

#Middle Band – 20 Day Simple Moving Average
#Upper Band – 20 Day Simple Moving Average + (Standard Deviation x 2)
#Lower Band – 20 Day Simple Moving Average - (Standard Deviation x 2)
    
def Boll_Band(DF, n=14):
    df = DF.copy()
    df['MB'] = df["Adj Close"].rolling(n).mean()
    df['UB'] = df["MB"] + 2* df['Adj Close'].rolling(n).std(ddof=0)
    df['LB'] = df["MB"] - 2* df['Adj Close'].rolling(n).std(ddof=0)
    df['BB_width'] = df['UB'] - df['LB']
    return df[['MB', 'UB', 'LB', 'BB_width']]


for ticker in ohlcv_data:
   ohlcv_data[ticker][['MB', 'UB', 'LB', 'BB_width']] = Boll_Band(ohlcv_data[ticker],20)