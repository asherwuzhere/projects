import yfinance as yf

# List of company ticker symbols
'''tickers = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "BRK.B", "NVDA", "TSLA", "META", "UNH", "JNJ", "V", "XOM", "PG", "JPM", "MA", "HD", "CVX", "ABBV", "MRK",
    "PEP", "KO", "LLY", "AVGO", "BAC", "COST", "TMO", "MCD", "WMT", "CSCO", "PFE", "ADBE", "DIS", "CRM", "TXN", "ACN", "LIN", "NFLX", "ABT", "DHR",
    "NKE", "INTC", "CMCSA", "VZ", "NEE", "WFC", "MDT", "HON", "UNP", "BMY", "PM", "LOW", "UPS", "MS", "RTX", "SCHW", "AMGN", "IBM", "AMT", "CVS",
    "T", "LMT", "QCOM", "INTU", "DE", "AMD", "CAT", "SPGI", "PLD", "GS", "BLK", "ELV", "AXP", "ISRG", "PYPL", "ADP", "NOW", "MDLZ", "ZTS", "SYK", "C",
    "CB", "GILD", "BKNG", "TMUS", "ADI", "REGN", "MO", "CL", "USB", "MMM", "GE", "CSX", "PGR", "CCI", "ETN", "SO", "EQIX", "HUM", "BDX", "BSX", "SHW",
    "ITW", "WM", "DUK", "EW", "AON", "TGT", "FISV", "EMR", "NSC", "COF", "APD", "EOG", "KMB", "VRTX", "FDX", "COP", "FCX", "AEP", "KLAC", "MAR", "PSA",
    "MCO", "HCA", "DG", "ORLY", "OXY", "SLB", "EXC", "CTAS", "AIG", "MU", "CHTR", "PPG", "SPG", "MTB", "ROST", "SRE", "ADSK", "PSX", "HLT", "DLR", "AZO",
    "PRU", "TRV", "F", "WELL", "MNST", "VLO", "LRCX", "BIIB", "KMI", "HSY", "D", "ALL", "NOC", "MPC", "ATVI", "PCAR", "STZ", "ED", "TEL", "EBAY", "CTSH",
    "WMB", "CRWD", "AMP", "MCK", "ADM", "PXD", "NXPI", "ODFL", "AFL", "PH", "CMG", "WEC", "ECL", "CME", "SYY", "MSCI", "DLTR", "IDXX", "PAYX", "FIS", "FAST",
    "NEM", "ORCL", "AWK", "GLW", "ROK", "VRSK", "ANET", "STT", "BK", "AME", "GPN", "WY", "GD", "ES", "ENPH", "BAX", "RSG", "EXPE", "PPL", "MTD", "FTNT",
    "HIG", "XYL", "DTE", "BKR", "CARR", "KEYS", "DFS", "AEE", "SNPS", "TDG", "AAL", "ZBH", "VFC", "CDW", "EFX", "HPQ", "FMC", "TSN", "BBY", "AJG", "VTRS",
    "ABC", "HPE", "IQV", "LYB", "CMS", "ETSY", "NTRS", "PKI", "WAT", "NUE", "IEX", "ATO", "OTIS", "CHD", "DRI", "FTV", "CTRA", "DOV", "ZBRA", "HOLX", "BXP",
    "CNP", "WBA", "PWR", "NVR", "STE", "MKC", "KR", "MOS", "RJF", "AMPH", "LUV", "UAL", "WHR", "OKE", "BBWI", "TSCO", "PEAK", "BMRN", "COO", "BALL", "PARA",
    "CINF", "TECH", "LNT", "IP", "CF", "HII", "IR", "PTC", "LW", "CE", "CPB", "RE", "JKHY", "FRC", "CBOE", "TYL", "TER", "AKAM", "NCLH", "SIVB", "GNRC", "WDC",
    "HAS", "CLX", "WYNN", "BRO", "HRL", "BF.B", "A", "TPR", "TRMB", "ALB", "RCL", "CAG", "LW", "SEE", "ZION", "KMX", "BIO", "GPC", "L", "NWL", "IRM", "BBBY",
    "AVY", "AAP", "ALK", "CMA", "ETR", "EVRG", "LDOS", "NDSN", "PKG", "ROL", "RL", "SWK", "TXT", "VTR", "WRB", "XRAY", "YUM", "JNPR", "OGN", "LEG", "NI"
]'''
# New list to store companies that pass filters
qualified_companies = []

# List of sectors to exclude
excluded_sectors = ["Financial Services", "Utilities"]

# Loop through each ticker in the tickers list
for ticker in tickers:
    stock = yf.Ticker(ticker)
    try:
        # Extract necessary data
        market_cap = stock.info.get('marketCap', 0)
        sector = stock.info.get('sector', '')
        country = stock.info.get('country', '')
        symbol = stock.info.get('symbol', '')

        # Check if the company meets all conditions
        if market_cap > 100_000_000 and sector not in excluded_sectors and country == "United States" and "ADR" not in symbol:
            # Extract financial data
            ebit = stock.financials.loc['EBIT', :].dropna().iloc[0]
            total_debt = stock.balance_sheet.loc['Total Debt', :].fillna(0).iloc[0]
            cash = stock.balance_sheet.loc['Cash And Cash Equivalents', :].fillna(0).iloc[0]
            shareholders_equity = stock.balance_sheet.loc['Stockholders Equity', :].fillna(0).iloc[0]

            # Calculate Enterprise Value
            enterprise_value = market_cap + total_debt - cash
            invested_capital = total_debt + shareholders_equity - cash

            ebit_to_ev = round(ebit / enterprise_value, 4) if enterprise_value > 0 else None
            roic = round(ebit / invested_capital, 3) if invested_capital > 0 else None

            # Add to qualified companies list
            qualified_companies.append((symbol, ebit_to_ev, roic))
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# Rank by EBIT / EV (from highest to lowest)
qualified_companies.sort(key=lambda x: x[1] or -1, reverse=True)
ranked_ebit_to_ev = [(rank, symbol, ebit_to_ev) for rank, (symbol, ebit_to_ev, _) in enumerate(qualified_companies, 1)]

# Rank by ROIC (from highest to lowest)
qualified_companies.sort(key=lambda x: x[2] or -1, reverse=True)
ranked_roic = [(rank, symbol, roic) for rank, (symbol, _, roic) in enumerate(qualified_companies, 1)]

# Combine rankings into a single list
ebit_rankings = {symbol: rank for rank, symbol, _ in ranked_ebit_to_ev}
roic_rankings = {symbol: rank for rank, symbol, _ in ranked_roic}
combined_ranking = [
    (symbol, ebit_rankings[symbol], roic_rankings[symbol]) 
    for symbol in ebit_rankings.keys() & roic_rankings.keys()
]
combined_ranking.sort(key=lambda x: x[1] + x[2])

# Display the results
print("\n--- Top 20 Ranked by EBIT / EV ---")
for rank, symbol, ebit_to_ev in ranked_ebit_to_ev[:20]:
    print(f"{rank}. {symbol}: EBIT / EV = {ebit_to_ev if ebit_to_ev is not None else 'N/A'}")

print("\n--- Top 20 Ranked by ROIC ---")
for rank, symbol, roic in ranked_roic[:20]:
    print(f"{rank}. {symbol}: ROIC = {roic if roic is not None else 'N/A'}")

print("\n--- Top 20 Combined Rankings (Based on Sum of Ranks) ---")
for symbol, ebit_rank, roic_rank in combined_ranking[:20]:
    combined_rank = ebit_rank + roic_rank
    print(f"{symbol}: Combined Rank = {combined_rank} (EBIT / EV Rank = {ebit_rank}, ROIC Rank = {roic_rank})")
