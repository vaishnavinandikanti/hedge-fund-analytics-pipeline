USE HedgeFundDB;
GO

CREATE OR ALTER PROCEDURE usp_CalculateDailyNAV
    @FundID INT,
    @StartDate DATE,
    @EndDate DATE
AS
BEGIN
    SET NOCOUNT ON;

    -- CTE 1: Calculate the total market value of all assets held on each day
    WITH AssetValues AS (
        SELECT 
            d.full_date AS valuation_date,
            SUM(f.market_value) AS total_asset_value
        FROM FACT_DAILY_PERFORMANCE f
        JOIN DIM_DATE d ON f.date_key = d.date_key
        WHERE f.fund_key = @FundID
          AND d.full_date BETWEEN @StartDate AND @EndDate
        GROUP BY d.full_date
    ),
    
    -- CTE 2: Calculate the total liabilities for each day
    Liabilities AS (
        SELECT 
            date AS valuation_date,
            SUM(amount) AS total_liabilities
        FROM FUND_LIABILITIES
        WHERE fund_key = @FundID
          AND date BETWEEN @StartDate AND @EndDate
        GROUP BY date
    )

    -- Final SELECT: Join the CTEs and calculate NAV
    SELECT 
        COALESCE(av.valuation_date, l.valuation_date) AS ValuationDate,
        ISNULL(av.total_asset_value, 0) AS TotalAssets,
        ISNULL(l.total_liabilities, 0) AS TotalLiabilities,
        (ISNULL(av.total_asset_value, 0) - ISNULL(l.total_liabilities, 0)) AS NetAssetValue,
        
        -- Window Function: Running Total of NAV over the period
        SUM(ISNULL(av.total_asset_value, 0) - ISNULL(l.total_liabilities, 0)) 
            OVER (ORDER BY COALESCE(av.valuation_date, l.valuation_date)) AS RunningNAV
            
    FROM AssetValues av
    FULL OUTER JOIN Liabilities l ON av.valuation_date = l.valuation_date
    ORDER BY ValuationDate;
END;
GO