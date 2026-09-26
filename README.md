# Hedge Fund Portfolio Performance & Valuation Pipeline

## 📌 Project Overview
An end-to-end data pipeline that ingests multi-asset financial data (Equities, Crypto, Bonds), models it into a Star Schema data warehouse, calculates daily Net Asset Value (NAV) using advanced SQL, and visualizes portfolio KPIs in a Power BI executive dashboard.

## 🛠️ Tech Stack
*   **Data Ingestion:** Python (Pandas, yfinance)
*   **Data Warehouse:** Snowflake (Star Schema, Staging, ETL)
*   **Data Processing & Analytics:** MS SQL Server (T-SQL, Docker), CTEs, Window Functions, Index Optimization
*   **Visualization:** Power BI (DAX, Dynamic Row-Level Security)

## 🏗️ Architecture
1. **Python Ingestion:** Pulls historical market data and SEC 13F institutional holdings. Generates synthetic fund liability data.
2. **Snowflake (Star Schema):** Raw CSVs are loaded into a `STAGING` schema. SQL transformations populate a `ANALYTICS` schema with `DIM_DATE`, `DIM_ASSET`, `DIM_FUND`, and `FACT_DAILY_PERFORMANCE`.
3. **MS SQL Server (T-SQL):** Local Docker container used to author a stored procedure (`usp_CalculateDailyNAV`) using CTEs and window functions. Query optimization performed using non-clustered indexes.
4. **Power BI:** Executive dashboard built with DAX measures (Total Assets, NAV, Daily PnL, Fund Return). Dynamic Row-Level Security (RLS) implemented to restrict data access by fund manager email.

## 📊 Dashboard Preview
*(Insert the screenshot of your dashboard here)*

## 🚀 How to Run
1. Clone the repo.
2. Create a Python virtual environment and run `pip install -r requirements.txt` (you can generate this by running `pip freeze > requirements.txt` in your terminal).
3. Run the Python scripts in the `python_scripts/` folder to generate the CSVs.
4. Execute the SQL scripts in Snowflake or MS SQL Server.
5. Open the Power BI file or recreate the dashboard using the provided semantic model.

## 💡 Key Insights Generated
*   Total Portfolio Net Asset Value (NAV) tracking over time.
*   Daily Profit & Loss (PnL) volatility visualization.
*   Asset Class Allocation (Risk Exposure) breakdown.
*   Top Holdings by Market Value.
