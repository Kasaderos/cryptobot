from binance import Client
import numpy as np
from datetime import datetime, timedelta, date
import time
import numpy as np
from sklearn.linear_model import LinearRegression

def get_data():
    '''
    [
    [
        1499040000000,      // Open time
        "0.01634790",       // Open
        "0.80000000",       // High
        "0.01575800",       // Low
        "0.01577100",       // Close
        "148976.11427815",  // Volume
        1499644799999,      // Close time
        "2434.19055334",    // Quote asset volume
        308,                // Number of trades
        "1756.87402397",    // Taker buy base asset volume
        "28.46694368",      // Taker buy quote asset volume
        "17928899.62484339" // Ignore.
    ]
    ]
    '''
    df = client.get_klines(
        symbol='BTCUSDT', interval=INTERVAL, limit=1000)
    df = np.array(df)
    times = [datetime(1970, 1, 1) + timedelta(milliseconds=int(ms))
            for ms in df[:, 6]]
    close = df[:, 4]

    assert times[len(times)-1].day == date.today().day
    return times, close

def predict():
    p = 30
    _, X = get_data()
    # 1 2 3 4 5
    # 1 2 3
    #   2 3 4
    #     3 4 5

    # X       y
    # 1 2 3   4
    # 2 3 4   5
    # 3 4 5   6
    X = np.array([X[i:i+p] for i in range(len(X)-p)])
    y = np.array([X[i] for i in range(p+1, len(X)-p+1)])
    reg = LinearRegression().fit(X, y)
    print(reg.score(X, y))
    preds = [0] * p
    past = X[len(X)-p:]
    value = None
    for i in range(p):
        value = reg.predict(np.array([past]))
        preds[i] = value
        np.concatenate(past, value)
        past = past[1:]

    return value

def wait():
    while True:
        orders = client.get_all_orders()
        if len(orders) == 0:
            return 

def open_position():
    global last_price
    while True:
        predPrice = predict()
        price = client.get_avg_price(symbol=PAIR)
        # long position
        if predPrice > price and 1 - price/predPrice < eps:
            try:
                client.create_order(symbol=PAIR,
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=CACHE/price)
                wait()        
                return price
            except Exception as e:
                print(e)
        time.sleep(10)

def close_position(buy_price):
    cache = client.get_asset_balance(CURRENCY)
    while True:
        price = client.get_avg_price(symbol=PAIR)
        if price >= buy_price:
            try:
                client.create_order(
                    symbol=PAIR,
                    side=Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=cache
                )
                wait()
                return
            except Exception as e:
                print(e)
        time.sleep(10)

api_key = ''
api_secret = ''
CURRENCY = 'BTC'
PAIR = 'BTCUSDT'
INTERVAL = Client.KLINE_INTERVAL_4HOUR
CACHE = 11 # dollars
last_price = None

client = Client(api_key, api_secret)
eps = 0.01
print(client.get_asset_balance(CURRENCY))
'''
while True:
    open_price = open_position()
    close_position(open_price)
    cache = client.get_asset_balance('USDT')
    print(f"[bot] cache {cache}")
'''
# # place a test market buy order, to place an actual order use the create_order function
# order = client.create_test_order(
#     symbol='BNBBTC',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=100)

# # get all symbol prices
# prices = client.get_all_tickers()
