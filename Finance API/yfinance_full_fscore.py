# This program uses the yfinance api to get stock market data and then applies the Piotroski F-Score to evaluate each company which has a price to book ratio above 1.

import yfinance as yf

# Define the list of ticker symbols
prefilter = [
    "A", "AAPL", "ABBV", "ABNB", "ABT", "ACGL", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK",
    "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALL", "ALLE",
    "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", "AMTM", "AMZN", "ANET", "ANSS",
    "AON", "AOS", "APA", "APD", "APH", "APTV", "ARE", "ATO", "AVB", "AVGO", "AVY", "AWK",
    "AXON", "AXP", "AZO", "BA", "BAC", "BALL", "BAX", "BBY", "BDX", "BEN", "BF.B", "BG",
    "BIIB", "BK", "BKNG", "BKR", "BLDR", "BLK", "BMY", "BR", "BRK.B", "BRO", "BSX", "BWA",
    "BX", "BXP", "C", "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCI", "CCL",
    "CDNS", "CDW", "CE", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI", "CINF", "CL",
    "CLX", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF", "COO", "COP", "COR",
    "COST", "CPAY", "CPB", "CPRT", "CPT", "CRL", "CRM", "CRWD", "CSCO", "CSGP", "CSX",
    "CTAS", "CTRA", "CTSH", "CTVA", "CVS", "CVX", "CZR", "D", "DAL", "DAY", "DD", "DE",
    "DECK", "DELL", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR", "DOC", "DOV",
    "DOW", "DPZ", "DRI", "DTE", "DUK", "DVA", "DVN", "DXCM", "EA", "EBAY", "ECL", "ED",
    "EFX", "EG", "EIX", "EL", "ELV", "EMN", "EMR", "ENPH", "EOG", "EPAM", "EQIX", "EQR",
    "EQT", "ERIE", "ES", "ESS", "ETN", "ETR", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR",
    "F", "FANG", "FAST", "FCX", "FDS", "FDX", "FE", "FFIV", "FI", "FICO", "FIS", "FITB",
    "FMC", "FOX", "FOXA", "FRT", "FSLR", "FTNT", "FTV", "GD", "GDDY", "GE", "GEHC", "GEN",
    "GEV", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOG", "GOOGL", "GPC", "GPN", "GRMN",
    "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD", "HES", "HIG", "HII", "HLT", "HOLX",
    "HON", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUBB", "HUM", "HWM", "IBM", "ICE",
    "IDXX", "IEX", "IFF", "INCY", "INTC", "INTU", "INVH", "IP", "IPG", "IQV", "IR", "IRM",
    "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JBL", "JCI", "JKHY", "JNJ", "JNPR", "JPM",
    "K", "KDP", "KEY", "KEYS", "KHC", "KIM", "KKR", "KLAC", "KMB", "KMI", "KMX", "KO",
    "KR", "KVUE", "L", "LDOS", "LEN", "LH", "LHX", "LIN", "LKQ", "LLY", "LMT", "LNT",
    "LOW", "LRCX", "LULU", "LUV", "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAR", "MAS",
    "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "META", "MGM", "MHK", "MKC",
    "MKTX", "MLM", "MMC", "MMM", "MNST", "MO", "MOH", "MOS", "MPC", "MPWR", "MRK",
    "MRNA", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTD", "MU", "NCLH", "NDAQ",
    "NDSN", "NEE", "NEM", "NFLX", "NI", "NKE", "NOC", "NOW", "NRG", "NSC", "NTAP",
    "NTRS", "NUE", "NVDA", "NVR", "NWS", "NWSA", "NXPI", "O", "ODFL", "OKE", "OMC",
    "ON", "ORCL", "ORLY", "OTIS", "OXY", "PANW", "PARA", "PAYC", "PAYX", "PCAR",
    "PCG", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PLD", "PLTR",
    "PM", "PNC", "PNR", "PNW", "PODD", "POOL", "PPG", "PPL", "PRU", "PSA", "PSX", "PTC",
    "PWR", "PYPL", "QCOM", "QRVO", "RCL", "REG", "REGN", "RF", "RJF", "RL", "RMD",
    "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", "RVTY", "SBAC", "SBUX", "SCHW", "SHW",
    "SJM", "SLB", "SMCI", "SNA", "SNPS", "SO", "SOLV", "SPG", "SPGI", "SRE", "STE",
    "STLD", "STT", "STX", "STZ", "SW", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP",
    "TDG", "TDY", "TECH", "TEL", "TER", "TFC", "TFX", "TGT", "TJX", "TMO", "TMUS",
    "TPL", "TPR", "TRGP", "TRMB", "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTWO",
    "TXN", "TXT", "TYL", "UAL", "UBER", "UDR", "UHS", "ULTA", "UNH", "UNP", "UPS",
    "URI", "USB", "V", "VICI", "VLO", "VLTO", "VMC", "VRSK", "VRSN", "VRTX", "VST",
    "VTR", "VTRS", "VZ", "WAB", "WAT", "WBA", "WBD", "WDC", "WEC", "WELL", "WFC",
    "WM", "WMB", "WMT", "WRB", "WST", "WTW", "WY", "WYNN", "XEL", "XOM", "XYL",
    "YUM", "ZBH", "ZBRA", "ZTS"
]

# Create a list to store tickers with P/B < 1
tickers = []

# Fetch data for each ticker and check the P/B ratio
for ticker in prefilter:
    try:
        stock = yf.Ticker(ticker)
        pb_ratio = stock.info.get('priceToBook', None)
        if pb_ratio is not None and pb_ratio < 1:
            tickers.append(ticker)
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        #
        #
        #
        #
        #
# Dictionary to store results
results = {}

# Loop through each ticker symbol
for ticker in tickers:
    # Download the stock's information
    stock = yf.Ticker(ticker)
    score = 0  # Initialize the score for each company

    try:
        # Calculate ROA for the last two years and current operating cash flow
        roa = stock.financials.loc['Net Income'] / stock.balance_sheet.loc['Total Assets']
        roa = roa.dropna()  # Remove any null values to avoid errors
        roa =  roa.sort_index(ascending=False)
        cfo = stock.cashflow.loc['Operating Cash Flow'].dropna().iloc[0]  # Most recent non-null CFO

        if len(roa) >= 2:
            current_roa = roa.iloc[0]  # Most recent ROA
            previous_roa = roa.iloc[1]  # ROA from the previous year

            # Check if current ROA is positive
            if current_roa > 0:
                score += 1  # Award a point for positive current ROA

            # Check if current-year ROA is higher than previous-year ROA
            if current_roa > previous_roa:
                score += 1  # Award an additional point
                
            if cfo > 0:
                score += 1  # Award a point for positive CFO

            # Award additional point if CFO is higher than current-year ROA
            if cfo > current_roa:
                score += 1

    except (KeyError, IndexError, TypeError):
        pass  # Skip if data is unavailable

    try:
        # Calculate the current ratio for the last two years
        current_ratio = stock.balance_sheet.loc['Current Assets'] / stock.balance_sheet.loc['Current Liabilities']
        current_ratio = current_ratio.dropna()
        current_ratio =  current_ratio.sort_index(ascending=False)

        if len(current_ratio) >= 2:
            current_current_ratio = current_ratio.iloc[0]  # Most recent current ratio
            previous_current_ratio = current_ratio.iloc[1]  # Previous year's current ratio

            # Check if current year's current ratio is higher than the previous year's
            if current_current_ratio > previous_current_ratio:
                score += 1  # Award a point for improvement in current ratio

    except (KeyError, IndexError, TypeError):
        pass  # Skip if data is unavailable

    try:
        # Calculate the long-term debt to total assets ratio for the last two years
        long_term_debt = stock.balance_sheet.loc['Long Term Debt']
        total_assets = stock.balance_sheet.loc['Total Assets']
        long_term_debt_to_assets = long_term_debt / total_assets
        long_term_debt_to_assets = long_term_debt_to_assets.dropna()
        long_term_debt_to_assets =  long_term_debt_to_assets.sort_index(ascending=False)

        if len(long_term_debt_to_assets) >= 2:
            current_long_term_debt_to_assets = long_term_debt_to_assets.iloc[0]  # Most recent ratio
            previous_long_term_debt_to_assets = long_term_debt_to_assets.iloc[1]  # Previous year's ratio

            # Check if current year's long-term debt to total assets ratio is lower than the previous year's
            if current_long_term_debt_to_assets < previous_long_term_debt_to_assets:
                score += 1  # Award a point for improvement in the debt-to-assets ratio

    except (KeyError, IndexError, TypeError):
        pass  # Skip if data is unavailable

    try:
        # Get the number of shares outstanding for the last two years
        shares_outstanding = stock.balance_sheet.loc['Ordinary Shares Number']
        shares_outstanding = shares_outstanding.dropna()
        shares_outstanding = shares_outstanding.sort_index(ascending=False)

        if len(shares_outstanding) >= 2:
            current_shares = shares_outstanding.iloc[0]  # Most recent number of shares
            previous_shares = shares_outstanding.iloc[1]  # Previous year's number of shares

            # Check if the current year's number of shares is the same or fewer than the previous year's
            if current_shares <= previous_shares:
                score += 1  # Award a point if shares are the same or fewer

    except (KeyError, IndexError, TypeError):
        pass  # Skip if data is unavailable

    try:
        # Calculate the gross margin ratio for the last two years
        gross_profit = stock.financials.loc['Gross Profit']
        total_revenue = stock.financials.loc['Total Revenue']
        gross_profit = gross_profit.dropna()
        total_revenue = total_revenue.dropna()
        gross_margin = gross_profit / total_revenue
        gross_margin = gross_margin.dropna()
        gross_margin =  gross_margin.sort_index(ascending=False)

        if len(gross_margin) >= 2:
            current_gross_margin = gross_margin.iloc[0]  # Most recent gross margin ratio
            previous_gross_margin = gross_margin.iloc[1]  # Previous year's gross margin ratio

            # Check if current year's gross margin ratio is higher than the previous year's
            if current_gross_margin > previous_gross_margin:
                score += 1  # Award a point for improvement in gross margin ratio
    except (KeyError, IndexError, TypeError):
        pass  # Skip if data is unavailable
    
    try:
        # Calculate the asset turnover ratio for the last two years
        total_revenue = stock.financials.loc['Total Revenue']
        total_assets = stock.balance_sheet.loc['Total Assets']
        asset_turnover = stock.financials.loc['Total Revenue'] / stock.balance_sheet.loc['Total Assets']
        asset_turnover = asset_turnover.dropna()
        asset_turnover =  asset_turnover.sort_index(ascending=False)
        if len(asset_turnover) >= 2:
            current_asset_turnover = asset_turnover.iloc[0]  # Most recent asset turnover ratio
            previous_asset_turnover = asset_turnover.iloc[1]  # Previous year's asset turnover ratio
            # Check if current year's asset turnover ratio is higher than the previous year's
            if current_asset_turnover > previous_asset_turnover:
                score += 1  # Award a point for improvement in asset turnover ratio

    except (KeyError, IndexError, TypeError):
        pass  # Skip if data is unavailable
    
    # Store the final score in results
    results[ticker] = score if score > 0 else "Data unavailable"
    
# Split companies by score groups
score_groups = {}

# Group companies by their score
for ticker, score in results.items():
    if score not in score_groups:
        score_groups[score] = []
    score_groups[score].append(ticker)

# Sort the score groups by score (from highest to lowest)
sorted_score_groups = sorted(score_groups.items(), key=lambda x: x[0], reverse=True)

# Display the sorted groups
for score, tickers in sorted_score_groups:
    print(f"Score {score}:")
    for ticker in tickers:
        print(f"  - {ticker}")
    print()
print(sorted_score_groups)

