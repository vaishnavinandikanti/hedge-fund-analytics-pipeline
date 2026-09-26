import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

os.makedirs('data', exist_ok=True)
print("Generating synthetic fund and liability data...")

# --- PART 1: CREATE DIM_FUND ---
funds = pd.DataFrame({
    'fund_key': [1, 2, 3],
    'fund_name': ['Alpha Capital', 'Beta Partners', 'Gamma Global'],
    'fund_style': ['Long/Short Equity', 'Global Macro', 'Event Driven'],
    'benchmark': ['SPY', 'SPY', 'TLT'],
    'fund_manager_email': ['manager_a@hedgefund.com', 'manager_b@hedgefund.com', 'manager_c@hedgefund.com']
})
funds.to_csv('data/dim_fund.csv', index=False)
print("✅ Saved 'data/dim_fund.csv'")

# --- PART 2: CREATE FUND LIABILITIES ---
# Generate daily liabilities (management fees + operational expenses) for 2022-2023
date_range = pd.date_range(start='2022-01-01', end='2024-01-01', freq='B') # 'B' for business days
liabilities_list = []
liability_key = 1

for fund_id in [1, 2, 3]:
    for date in date_range:
        # Base management fee: random amount between $1,000 and $5,000
        mgmt_fee = np.random.uniform(1000, 5000)
        # Operational expense: random amount between $200 and $1,000
        op_expense = np.random.uniform(200, 1000)
        
        liabilities_list.append({
            'liability_key': liability_key,
            'fund_key': fund_id,
            'date': date.strftime('%Y-%m-%d'),
            'liability_type': 'Management Fee',
            'amount': round(mgmt_fee, 2)
        })
        liability_key += 1
        
        liabilities_list.append({
            'liability_key': liability_key,
            'fund_key': fund_id,
            'date': date.strftime('%Y-%m-%d'),
            'liability_type': 'Operational Expense',
            'amount': round(op_expense, 2)
        })
        liability_key += 1

liabilities_df = pd.DataFrame(liabilities_list)
liabilities_df.to_csv('data/fund_liabilities.csv', index=False)
print("✅ Saved 'data/fund_liabilities.csv'")

# --- PART 3: MAP HOLDINGS TO OUR FUNDS ---
# Load the holdings we downloaded in Step 2
try:
    holdings_df = pd.read_csv('data/fund_holdings.csv')
    
    # Randomly assign our 3 fund_keys to the holdings so each fund has a portfolio
    np.random.seed(42) # For reproducibility
    holdings_df['fund_key'] = np.random.choice([1, 2, 3], size=len(holdings_df))
    
    # Add a holding_key (primary key)
    holdings_df.reset_index(inplace=True)
    holdings_df.rename(columns={'index': 'holding_key'}, inplace=True)
    
    # Keep only the columns we need for Snowflake
    final_holdings = holdings_df[['holding_key', 'fund_key', 'ticker', 'shares_held', 'report_date']]
    final_holdings.to_csv('data/dim_holding.csv', index=False)
    print("✅ Saved 'data/dim_holding.csv'")
    
except FileNotFoundError:
    print("⚠️ Could not find 'data/fund_holdings.csv'. Please ensure Step 2 ran successfully.")

print("🎉 Step 3 complete! You now have 3 new CSV files in your 'data' folder.")