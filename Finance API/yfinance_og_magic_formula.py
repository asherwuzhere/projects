import yfinance as yf

print("Magic Formula Calculator (type 'exit' to end and list companies.)\n")

# Dictionary to store the scores of all tickers
all_scores = {}

while True:
    # Prompt the user to input a ticker symbol
    user_input = input("Ticker: ").strip().upper()

    # Exit the loop if the user types 'exit'
    if user_input == 'EXIT':
        if all_scores:
            # Sort and display scores from greatest to lowest based on EBIT/EV
            print("\nAll Magic Formula Scores:")
            for ticker, (ebit_ev, ebit_roce) in all_scores.items():
                total_score = ebit_ev + ebit_roce  # Sum of EBIT/EV and EBIT/ROCE for each company
                print(f"{ticker}: {total_score:.4f}")
        else:
            print("No scores to display.")
        print("\n*beep boop* Ending program *beep boo..*")
        break

    # Analyze the single ticker
    ticker = user_input
    stock = yf.Ticker(ticker)

    try:
        # Get the relevant financial data
        ebit = stock.financials.loc['EBIT', :].dropna().iloc[0]
        total_debt = stock.balance_sheet.loc['Total Debt', :].fillna(0).iloc[0]
        land_improvements = stock.balance_sheet.loc['Land And Improvements'].fillna(0).iloc[0]
        #properties = stock.balance_sheet.loc['Properties'].fillna(0).iloc[0]
        equipment = stock.balance_sheet.loc['Machinery Furniture Equipment'].fillna(0).iloc[0]
        accumulated_depreciation = stock.balance_sheet.loc['Accumulated Depreciation'].fillna(0).iloc[0]
        abs_accumulated_depreciation = abs(accumulated_depreciation)
        working_capital = stock.balance_sheet.loc['Working Capital'].fillna(0).iloc[0]
        cash = stock.balance_sheet.loc['Cash And Cash Equivalents', :].fillna(0).iloc[0]
        market_cap = stock.info.get('marketCap', None)
        total_assets = stock.balance_sheet.loc['Total Assets', :].dropna().iloc[0]
        current_liabilities = stock.balance_sheet.loc['Current Liabilities', :].dropna().iloc[0]

        if market_cap is None:
            raise ValueError("Market capitalization data is unavailable.")

        # Calculate Enterprise Value (EV)
        ev = market_cap + total_debt - cash

        # Calculate EBIT/EV
        ebit_ev = ebit / ev if ev > 0 else 0

        # Calculate Return on Capital Employed (ROCE)
        denom_roc = land_improvements + equipment - abs_accumulated_depreciation + working_capital
        ebit_roce = ebit / denom_roc if denom_roc > 0 else 0

        # Store the scores
        all_scores[ticker] = (ebit_ev, ebit_roce)

        # Display the result for the current ticker
        print(f"{ticker}: EBIT/EV = {ebit_ev:.4f}, ROCE = {ebit_roce:.4f}\n")

    except (KeyError, IndexError, TypeError, ValueError) as e:
        print(f"Error processing {ticker}: {e}\n")
        all_scores[ticker] = ("Data unavailable", "Data unavailable")
