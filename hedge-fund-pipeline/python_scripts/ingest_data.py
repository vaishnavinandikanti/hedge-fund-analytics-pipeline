import yfinance as yf
import pandas as pd
import os

# Create a folder to store the raw data
os.makedirs('data', exist_ok=True)

print("Starting data ingestion...")

# --- PART 1: FETCH MULTI-ASSET MARKET DATA ---
print("Downloading market data...")
# A mix of Equities (AAPL, MSFT), Crypto (BTC-USD, ETH-USD), and Bonds (TLT)
tickers = ['AAPL', 'MSFT', 'NVDA', 'BTC-USD', 'ETH-USD', 'TLT', 'SPY']
start_date = '2022-01-01'
end_date = '2024-01-01'

# Download data from Yahoo Finance
market_data = yf.download(tickers, start=start_date, end=end_date)

# Save raw market data to CSV
market_data.to_csv('data/market_data.csv')
print(f"✅ Market data saved to 'data/market_data.csv'")

# --- PART 2: FETCH SEC 13F HEDGE FUND HOLDINGS ---
print("Downloading hedge fund holdings (SEC 13F)...")
# URL to a public Hugging Face dataset containing parsed SEC 13F filings
url = "https://huggingface.co/datasets/Kasher13/Institutional-Holdings-Dashboard/resolve/main/data.csv"

try:
    # Attempt to download the dataset
    holdings_data = pd.read_csv(url)
    
    # Filter to keep only the most recent quarter, or just take a sample for our project
    # (Using a sample to keep the file size manageable for the next steps)
    holdings_sample = holdings_data.head(500) 
    
    holdings_sample.to_csv('data/fund_holdings.csv', index=False)
    print(f"✅ Fund holdings saved to 'data/fund_holdings.csv'")
    
except Exception as e:
    print(f"⚠️ Could not download from Hugging Face. Error: {e}")
    print("Generating a synthetic holdings dataset instead so we can proceed...")
    
    # Fallback: Generate synthetic holdings if the API/URL fails
    synthetic_holdings = pd.DataFrame({
        'fund_name': ['Bridgewater Associates', 'Berkshire Hathaway', 'Citadel'] * 5,
        'ticker': ['AAPL', 'MSFT', 'NVDA', 'BTC-USD', 'ETH-USD'] * 3,
        'shares_held': [100000, 500000, 250000, 10000, 50000] * 3,
        'report_date': ['2023-09-30'] * 15
    })
    synthetic_holdings.to_csv('data/fund_holdings.csv', index=False)
    print(f"✅ Synthetic fund holdings saved to 'data/fund_holdings.csv'")

print("🎉 Data ingestion complete! Check the 'data' folder in VS Code.")