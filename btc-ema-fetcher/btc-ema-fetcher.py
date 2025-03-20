import requests
import pandas as pd
import time

def get_historical_data(symbol='BTCUSDT', interval='1d', limit=200):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                          'quote_asset_volume', 'number_of_trades', 'taker_buy_base_vol',
                                          'taker_buy_quote_vol', 'ignore'])
        df['close'] = df['close'].astype(float)
        return df[['timestamp', 'close']]
    else:
        print("Error fetching data:", response.text)
        return None

def calculate_ema(df, span):
    return df['close'].ewm(span=span, adjust=False).mean()

def main():
    while True:
        print("Fetching data...")
        df = get_historical_data()
        if df is not None:
            df['EMA_20'] = calculate_ema(df, 20)
            df['EMA_50'] = calculate_ema(df, 50)
            df['EMA_200'] = calculate_ema(df, 200)
            print(df.tail(5))  # Display the latest 5 rows
        else:
            print("Failed to retrieve data.")
        
        time.sleep(60)  # Fetch data every minute

if __name__ == "__main__":
    main()
