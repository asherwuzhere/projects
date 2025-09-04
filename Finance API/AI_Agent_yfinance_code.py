# Since I have used the yfinance API in many of my projects, I decided to attempt to make a "GPT" or an AI agent trained specifically for coding with yfinance. This is a sample code that it wrote.

import yfinance as yf
import pandas as pd

# Define the stock universe (e.g., S&P 500 tickers)
def get_sp500_tickers():
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(sp500_url)
    df = tables[0]
    return df['Symbol'].tolist()

# Calculate Earnings Yield and Return on Capital for each stock
def calculate_magic_formula_metrics(tickers):
    data = []

    for ticker in tickers:
        try:
            # Fetch financial data using yfinance
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get relevant metrics
            market_cap = info.get('marketCap')
            ebit = info.get('ebitda')  # Approximate EBIT
            total_debt = info.get('totalDebt', 0)
            cash = info.get('totalCash', 0)
            enterprise_value = market_cap + total_debt - cash if market_cap else None

            # Calculate Return on Capital (ROC)
            total_assets = info.get('totalAssets')
            current_liabilities = info.get('currentLiabilities', 0)
            invested_capital = (total_assets - current_liabilities) if total_assets else None
            roc = ebit / invested_capital if ebit and invested_capital else None

            # Calculate Earnings Yield
            earnings_yield = ebit / enterprise_value if ebit and enterprise_value else None

            # Append to data if metrics are valid
            if roc and earnings_yield:
                data.append({
                    'Ticker': ticker,
                    'Earnings Yield': earnings_yield,
                    'Return on Capital': roc
                })

        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    return pd.DataFrame(data)

# Rank stocks based on Magic Formula criteria
def rank_stocks(df):
    # Rank by Earnings Yield and Return on Capital
    df['Earnings Yield Rank'] = df['Earnings Yield'].rank(ascending=False)
    df['ROC Rank'] = df['Return on Capital'].rank(ascending=False)

    # Calculate combined rank
    df['Magic Formula Rank'] = df['Earnings Yield Rank'] + df['ROC Rank']

    # Sort by combined rank
    return df.sort_values(by='Magic Formula Rank').reset_index(drop=True)

if __name__ == "__main__":
    # Get the tickers
    sp500_tickers = get_sp500_tickers()

    # Calculate metrics
    print("Calculating Magic Formula metrics...")
    metrics_df = calculate_magic_formula_metrics(sp500_tickers)

    # Rank stocks
    print("Ranking stocks based on Magic Formula...")
    ranked_stocks = rank_stocks(metrics_df)

    # Display the top 10 stocks
    print(ranked_stocks.head(10))
