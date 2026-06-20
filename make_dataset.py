# 'Marketcap':'market_cap'
import pandas as pd
import os

print("Creating crypto dataset...")

folder = "archive"
all_data = []

coins = [
    "Bitcoin", "Ethereum", "Binance Coin", "XRP",
    "Cardano", "Solana", "Dogecoin",
    "Polkadot", "Polygon", "Litecoin"
]

symbols = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH",
    "Binance Coin": "BNB",
    "XRP": "XRP",
    "Cardano": "ADA",
    "Solana": "SOL",
    "Dogecoin": "DOGE",
    "Polkadot": "DOT",
    "Polygon": "MATIC",
    "Litecoin": "LTC"
}

supply = {
    "Bitcoin": 19_000_000,
    "Ethereum": 120_000_000,
    "Binance Coin": 160_000_000,
    "XRP": 50_000_000_000,
    "Cardano": 35_000_000_000,
    "Solana": 400_000_000,
    "Dogecoin": 140_000_000_000,
    "Polkadot": 1_200_000_000,
    "Polygon": 10_000_000_000,
    "Litecoin": 70_000_000
}

for coin in coins:
    path = os.path.join(folder, f"coin_{coin}.csv")

    if not os.path.exists(path):
        print(f"⚠ {coin} not found — skipped")
        continue

    df = pd.read_csv(path)

    df = df[['Date','Open','Volume']]

    df.rename(columns={
        'Date':'date',
        'Open':'price',
        'Marketcap':'market_cap',
        'Volume':'volume'
    }, inplace=True)

    df['cryptocurrency'] = coin
    df['symbol'] = symbols[coin]

    # ✅ Compute market cap
    df['market_cap'] = df['price'] * supply[coin]

    # ✅ Percent change (fill first value)
    df['percent_change_24h'] = df['price'].pct_change() * 100
    df['percent_change_24h'].fillna(0, inplace=True)

    all_data.append(df)
    print(f"✔ {coin} processed")

# merge
final_df = pd.concat(all_data, ignore_index=True)

# convert date
final_df['date'] = pd.to_datetime(final_df['date'])

# sort properly
final_df = final_df.sort_values(by=['cryptocurrency','date'])

# save
os.makedirs("dataset", exist_ok=True)
final_df.to_csv("dataset/crypto_data.csv", index=False)

print("\n🎉 SUCCESS!")
print("Rows:", final_df.shape[0])
print("Columns:", final_df.shape[1])
