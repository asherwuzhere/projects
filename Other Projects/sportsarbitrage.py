import requests

API_KEY = "8483ad510693ded3a1610dba9ce063dc"

# ===============================
# ALLOWED SPORTSBOOKS
# Set to None to allow ALL books
# ===============================
ALLOWED_BOOKS = {
    "DraftKings",
    "FanDuel",
    "BetMGM",
    "Caesars",
    "PointsBet",
    "BetRivers",
    "Unibet",
    "Fanatics",
    "Bet365",
    "Pinnacle",
    "Circa Sports",
    "Bovada",
    "BetOnline.ag"
}
ALLOWED_BOOKS = None

MAX_ARB_PCT = 5.0      # discard garbage arbs
MAX_ABS_ODDS = 500    # discard extreme longshots


def american_to_decimal(odds):
    if odds > 0:
        return 1 + odds / 100
    return 1 + 100 / abs(odds)


def stake_percentages(o1, o2):
    d1 = american_to_decimal(o1)
    d2 = american_to_decimal(o2)
    p1 = 1 / d1
    p2 = 1 / d2
    total = p1 + p2
    return (p1 / total) * 100, (p2 / total) * 100


def process_event(event):
    best = {}

    for book in event.get("bookmakers", []):
        book_name = book.get("title")
        if ALLOWED_BOOKS is not None and book_name not in ALLOWED_BOOKS:
            continue

        for market in book.get("markets", []):
            key = market.get("key")
            outcomes = market.get("outcomes", [])
            if key not in {"h2h", "totals", "spreads"} or len(outcomes) != 2:
                continue

            # -------- H2H --------
            if key == "h2h":
                home = event["home_team"]
                away = event["away_team"]
                odds = {o["name"]: o["price"] for o in outcomes}
                if home not in odds or away not in odds:
                    continue
                market_id = ("h2h", home, away)
                sides = [(home, odds[home], None), (away, odds[away], None)]

            # -------- TOTALS --------
            elif key == "totals":
                names = sorted(o["name"] for o in outcomes)
                if names != ["Over", "Under"]:
                    continue
                p1 = outcomes[0]["point"]
                p2 = outcomes[1]["point"]
                if p1 != p2:
                    continue
                market_id = ("totals", float(p1))
                sides = [(o["name"], o["price"], p1) for o in outcomes]

            # -------- SPREADS --------
            else:
                home = event["home_team"]
                away = event["away_team"]
                by_name = {o["name"]: o for o in outcomes}
                if home not in by_name or away not in by_name:
                    continue

                p1 = by_name[home]["point"]
                p2 = by_name[away]["point"]

                if p1 is None or p2 is None:
                    continue
                if round(float(p1) + float(p2), 6) != 0.0:
                    continue
                if not (p1 < 0 < p2 or p2 < 0 < p1):
                    continue

                market_id = ("spreads", abs(float(p1)))
                sides = [
                    (home, by_name[home]["price"], p1),
                    (away, by_name[away]["price"], p2)
                ]

            if market_id not in best:
                best[market_id] = {}

            for name, price, point in sides:
                if abs(price) > MAX_ABS_ODDS:
                    continue
                if name not in best[market_id] or price > best[market_id][name][0]:
                    best[market_id][name] = (price, book_name, point)

    arbs = []

    for market_id, sides in best.items():
        if len(sides) != 2:
            continue

        (n1, a), (n2, b) = list(sides.items())
        if a[1] == b[1]:
            continue

        d1 = american_to_decimal(a[0])
        d2 = american_to_decimal(b[0])
        arb_pct = (1 - (1 / d1 + 1 / d2)) * 100

        if arb_pct <= 0 or arb_pct > MAX_ARB_PCT:
            continue

        arbs.append({
            "type": market_id[0],
            "label": market_id,
            "side1": (n1, a),
            "side2": (n2, b),
            "profit_pct": arb_pct
        })

    return arbs


sports = [
    "basketball_nba",
    "basketball_ncaab",
    "americanfootball_nfl",
    "americanfootball_ncaaf",
    "baseball_mlb",
    "icehockey_nhl"
]

for sport in sports:
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h,totals,spreads",
        "oddsFormat": "american"
    }

    events = requests.get(url, params=params).json()
    if not isinstance(events, list):
        continue

    for event in events:
        for arb in process_event(event):
            s1, s2 = arb["side1"], arb["side2"]

            print("\n===============================")
            print(f"ARBITRAGE FOUND — {sport.upper()} — {arb['type'].upper()}")
            print(f"{s1[0]} @ {s1[1][1]} : {s1[1][0]}")
            print(f"{s2[0]} @ {s2[1][1]} : {s2[1][0]}")

            p1, p2 = stake_percentages(s1[1][0], s2[1][0])
            print("\nStake Percentages:")
            print(f"  {s1[0]}: {p1:.2f}%")
            print(f"  {s2[0]}: {p2:.2f}%")
            print(f"\nProfit Margin: {arb['profit_pct']:.3f}%")
