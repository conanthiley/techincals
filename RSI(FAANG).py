
import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT", "AAPL", "NFLX", "FB"]
ohlcv_data = {}

for ticker in tickers:
    data = yf.download(ticker,period='1mo', interval='5m')
    data.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = data

#RSI = 100 – 100/ (1 + RS)
#RS = Average Gain of n days UP  / Average Loss of n days DOWN

#pinescript formula:
#change = change(close)
#gain = change >= 0 ? change : 0.0
#loss = change < 0 ? (-1) * change : 0.0
#avgGain = rma(gain, 14)
#avgLoss = rma(loss, 14)
#rs = avgGain / avgLoss
#rsi = 100 - (100 / (1 + rs))


def RSI(DF, n=14):
    df = DF.copy()
    df['change'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['change'] >= 0, df['change'], 0)
    df['loss'] = np.where(df['change'] < 0, -1 * df['change'], 0)
    df['avgGain'] = df['gain'].ewm(alpha=1/n, min_periods=n).mean()
    df['avgLoss'] = df['loss'].ewm(alpha=1/n, min_periods=n).mean()
    df['RS'] = df['avgGain']/df['avgLoss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']

for ticker in ohlcv_data:
    ohlcv_data[ticker]['RSI'] = RSI(ohlcv_data[ticker])
