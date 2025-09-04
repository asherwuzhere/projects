# Used to get stock market data and then put it in a spreadsheet for 

import yfinance as yf
import pandas as pd

# Read S&P 500 tickers from a text file
with open("s&p_500_tickers_real.txt", "r") as file:
    tickers = [line.strip() for line in file.readlines() if line.strip()]

# Placeholder for data
data = []

# Fetch data for each ticker
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        sp500 = yf.Ticker("^GSPC")  # S&P 500 index

        # Get latest market price
        history = stock.history(period="1mo")  # Fetch data for the last month
        sp500_history = sp500.history(period="1mo")

        if history.empty or sp500_history.empty:
            print(f"No recent data for {ticker}")
            continue

        # Calculate price change over the month
        price_start = history['Close'].iloc[0]
        price_end = history['Close'].iloc[-1]
        price_change = (price_end - price_start) / price_start

        # S&P 500 performance over the same period
        sp500_start = sp500_history['Close'].iloc[0]
        sp500_end = sp500_history['Close'].iloc[-1]
        sp500_change = (sp500_end - sp500_start) / sp500_start

        # Determine if the stock beat the S&P 500
        beat_sp500 = 1 if price_change > sp500_change else 0

        # Retrieve stock financial data
        info = stock.info

        data.append({
            "Ticker": ticker,
            "Price Change Last Month": price_change,
            "S&P 500 Change Last Month": sp500_change,
            "Beats S&P 500 (1=yes, 0=no)": beat_sp500,
            "Price-to-Book Ratio (P/B)": info.get("priceToBook"),
            "Price-to-Sales Ratio (P/S)": info.get("priceToSalesTrailing12Months"),
            "Enterprise Value to EBITDA": info.get("enterpriseToEbitda"),
            "Enterprise Value to Revenue": info.get("enterpriseToRevenue"),
            "Trailing P/E Ratio": info.get("trailingPE"),
            "Forward P/E Ratio": info.get("forwardPE"),
            "PEG Ratio": info.get("trailingPegRatio"),
            "Gross Margin": info.get("grossMargins"),
            "EBITDA Margin": info.get("ebitdaMargins"),
            "Operating Margin": info.get("operatingMargins"),
            "Net Profit Margin": info.get("profitMargins"),
            "Return on Assets (ROA)": info.get("returnOnAssets"),
            "Return on Equity (ROE)": info.get("returnOnEquity"),
            "Debt-to-Equity Ratio": info.get("debtToEquity"),
            "Current Ratio": info.get("currentRatio"),
            "Quick Ratio": info.get("quickRatio"),
            "Revenue Growth": info.get("revenueGrowth"),
            "Earnings Growth": info.get("earningsGrowth"),
            "Short Ratio": info.get("shortRatio"),
            "Dividend Yield": info.get("dividendYield"),
            "Payout Ratio": info.get("payoutRatio"),
        })

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("new_stock_data.csv", index=False)
print("Dataset saved to 'new_stock_data.csv'")
