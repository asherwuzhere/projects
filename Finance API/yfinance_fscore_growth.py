import yfinance as yf

def calculate_growth_f_score(ticker):
    stock = yf.Ticker(ticker)
    score = 0  # Initialize the score for each company

    try:
        # ROA and CFO Calculations
        roa = stock.financials.loc['Net Income'] / stock.balance_sheet.loc['Total Assets']
        roa = roa.dropna().sort_index(ascending=False)
        cfo = stock.cashflow.loc['Operating Cash Flow'].dropna().iloc[0]  # Most recent non-null CFO

        if len(roa) >= 2:
            current_roa = roa.iloc[0]  # Most recent ROA
            previous_roa = roa.iloc[1]  # ROA from the previous year

            if current_roa > 0:
                score += 1  # Positive current ROA
            if current_roa > previous_roa:
                score += 1  # Improving ROA
            if cfo > 0:
                score += 1  # Positive CFO
            if cfo > current_roa:
                score += 1  # CFO > ROA

    except (KeyError, IndexError, TypeError):
        pass

    try:
        # Current Ratio Check
        current_ratio = stock.balance_sheet.loc['Total Current Assets'] / stock.balance_sheet.loc['Total Current Liabilities']
        current_ratio = current_ratio.dropna().sort_index(ascending=False)

        if len(current_ratio) >= 2:
            current_current_ratio = current_ratio.iloc[0]
            previous_current_ratio = current_ratio.iloc[1]

            if current_current_ratio > previous_current_ratio:
                score += 1  # Improving Current Ratio

    except (KeyError, IndexError, TypeError):
        pass

    try:
        # Long-Term Debt to Total Assets Ratio
        long_term_debt = stock.balance_sheet.loc['Long Term Debt']
        total_assets = stock.balance_sheet.loc['Total Assets']
        long_term_debt_to_assets = (long_term_debt / total_assets).dropna().sort_index(ascending=False)

        if len(long_term_debt_to_assets) >= 2:
            if long_term_debt_to_assets.iloc[0] < long_term_debt_to_assets.iloc[1]:
                score += 1  # Improving Debt-to-Assets Ratio

    except (KeyError, IndexError, TypeError):
        pass

    try:
        # Shares Outstanding
        shares_outstanding = stock.balance_sheet.loc['Ordinary Shares Number']
        shares_outstanding = shares_outstanding.dropna().sort_index(ascending=False)

        if len(shares_outstanding) >= 2:
            if shares_outstanding.iloc[0] <= shares_outstanding.iloc[1]:
                score += 1  # Same or fewer shares outstanding

    except (KeyError, IndexError, TypeError):
        pass

    try:
        # Gross Margin Ratio
        gross_profit = stock.financials.loc['Gross Profit']
        total_revenue = stock.financials.loc['Total Revenue']
        gross_margin = (gross_profit / total_revenue).dropna().sort_index(ascending=False)

        if len(gross_margin) >= 2:
            if gross_margin.iloc[0] > gross_margin.iloc[1]:
                score += 1  # Improving Gross Margin Ratio

    except (KeyError, IndexError, TypeError):
        pass

    try:
        # Asset Turnover Ratio
        asset_turnover = (stock.financials.loc['Total Revenue'] / stock.balance_sheet.loc['Total Assets']).dropna().sort_index(ascending=False)

        if len(asset_turnover) >= 2:
            if asset_turnover.iloc[0] > asset_turnover.iloc[1]:
                score += 1  # Improving Asset Turnover Ratio

    except (KeyError, IndexError, TypeError):
        pass

    try:
        # Revenue Increase Check
        total_revenue = stock.financials.loc['Total Revenue'].dropna().sort_index(ascending=False)

        if len(total_revenue) >= 2:
            if total_revenue.iloc[0] > total_revenue.iloc[1]:
                score += 1  # Revenue increased year over year

    except (KeyError, IndexError, TypeError):
        pass

    return score


# Continuous Input Loop
while True:
    ticker = input("\nEnter a stock ticker (or type 'exit' to quit): ").strip().upper()
    if ticker == 'EXIT':
        print("Exiting the program. Goodbye!")
        break
    
    if not ticker:
        print("Please enter a valid ticker symbol.")
        continue
    
    try:
        growth_f_score = calculate_growth_f_score(ticker)
        print(f"{ticker} Growth-Adjusted F-Score: {growth_f_score}/10")
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
