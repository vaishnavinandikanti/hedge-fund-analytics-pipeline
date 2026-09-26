-- 1. Create Database
CREATE DATABASE HedgeFundDB;
GO

USE HedgeFundDB;
GO

-- 2. Create Dimension Tables
CREATE TABLE DIM_DATE (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT,
    day INT
);

CREATE TABLE DIM_ASSET (
    asset_key INT PRIMARY KEY,
    ticker VARCHAR(20),
    asset_class VARCHAR(20)
);

CREATE TABLE DIM_FUND (
    fund_key INT PRIMARY KEY,
    fund_name VARCHAR(100),
    fund_style VARCHAR(50),
    benchmark VARCHAR(20),
    fund_manager_email VARCHAR(100)
);

-- 3. Create Fact Table
CREATE TABLE FACT_DAILY_PERFORMANCE (
    date_key INT,
    fund_key INT,
    asset_key INT,
    shares_held FLOAT,
    close_price FLOAT,
    market_value FLOAT,
    PRIMARY KEY (date_key, fund_key, asset_key)
);

-- 4. Create Liabilities Table
CREATE TABLE FUND_LIABILITIES (
    liability_key INT PRIMARY KEY,
    fund_key INT,
    date DATE,
    liability_type VARCHAR(50),
    amount FLOAT
);
GO

-- 5. Insert Sample Data (Simulating our Snowflake data)
-- Insert Dates
INSERT INTO DIM_DATE (date_key, full_date, year, month, day) VALUES 
(20230101, '2023-01-01', 2023, 1, 1),
(20230102, '2023-01-02', 2023, 1, 2),
(20230103, '2023-01-03', 2023, 1, 3),
(20230104, '2023-01-04', 2023, 1, 4),
(20230105, '2023-01-05', 2023, 1, 5);

-- Insert Assets
INSERT INTO DIM_ASSET (asset_key, ticker, asset_class) VALUES 
(1, 'AAPL', 'Equity'),
(2, 'MSFT', 'Equity'),
(3, 'BTC-USD', 'Crypto');

-- Insert Funds
INSERT INTO DIM_FUND (fund_key, fund_name, fund_style, benchmark, fund_manager_email) VALUES 
(1, 'Alpha Capital', 'Long/Short Equity', 'SPY', 'manager_a@hedgefund.com'),
(2, 'Beta Partners', 'Global Macro', 'SPY', 'manager_b@hedgefund.com');

-- Insert Fact Performance Data
INSERT INTO FACT_DAILY_PERFORMANCE (date_key, fund_key, asset_key, shares_held, close_price, market_value) VALUES 
(20230101, 1, 1, 1000, 150.00, 150000.00),
(20230101, 1, 2, 500, 250.00, 125000.00),
(20230102, 1, 1, 1000, 155.00, 155000.00),
(20230102, 1, 2, 500, 252.00, 126000.00),
(20230103, 1, 1, 1000, 152.00, 152000.00),
(20230103, 1, 2, 500, 248.00, 124000.00),
(20230101, 2, 3, 10, 30000.00, 300000.00),
(20230102, 2, 3, 10, 31000.00, 310000.00),
(20230103, 2, 3, 10, 30500.00, 305000.00);

-- Insert Liabilities
INSERT INTO FUND_LIABILITIES (liability_key, fund_key, date, liability_type, amount) VALUES 
(1, 1, '2023-01-01', 'Management Fee', 1500.00),
(2, 1, '2023-01-02', 'Management Fee', 1550.00),
(3, 1, '2023-01-03', 'Management Fee', 1520.00),
(4, 2, '2023-01-01', 'Management Fee', 3000.00),
(5, 2, '2023-01-02', 'Management Fee', 3100.00),
(6, 2, '2023-01-03', 'Management Fee', 3050.00);
GO