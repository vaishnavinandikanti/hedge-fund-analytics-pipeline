import pandas as pd

# Read the multi-level header CSV
df = pd.read_csv('data/market_data.csv', header=[0,1], index_col=0)

# Reshape the data from wide to long format
df_long = df.stack(level=1).reset_index()

# The actual columns are: 'level_0', 'level_1', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume'
df_long.columns = ['date', 'ticker', 'adj_close', 'close', 'high', 'low', 'open', 'volume']

# Drop the Adj Close column since we don't need it for our basic NAV calculation
df_long = df_long.drop(columns=['adj_close'])

# Save it back to the data folder
df_long.to_csv('data/market_data_flat.csv', index=False)
print("✅ Flattened market data saved to 'data/market_data_flat.csv'")