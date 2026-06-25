import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "stock_data.csv"

TICKERS = ["NDX", "GSPC", "DJI", "GC_F", "CL_F", "BZ_F", "SI_F", "CVX", "XEL", "HG_F"]

TICKER_LABELS = {
    "NDX": "Nasdaq 100",
    "GSPC": "S&P 500",
    "DJI": "Dow Jones",
    "GC_F": "Gold Futures",
    "CL_F": "WTI Crude Oil",
    "BZ_F": "Brent Crude",
    "SI_F": "Silver Futures",
    "CVX": "Chevron",
    "XEL": "Xcel Energy",
    "HG_F": "Copper Futures",
}


def _safe_float(value):
    try:
        f = float(value)
        return f if f != 0 else None
    except (ValueError, TypeError):
        return None


def load_rows(limit=100):
    if not CSV_PATH.exists():
        return []
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows[:limit]


def get_latest_prices():
    rows = load_rows(limit=10)
    results = []
    for ticker in TICKERS:
        close_col = f"{ticker}_Close"
        open_col = f"{ticker}_Open"
        for row in rows:
            close = _safe_float(row.get(close_col))
            open_ = _safe_float(row.get(open_col))
            if close is not None:
                change = round(close - open_, 2) if open_ else None
                change_pct = round((change / open_) * 100, 2) if open_ and change else None
                results.append({
                    "ticker": ticker,
                    "label": TICKER_LABELS.get(ticker, ticker),
                    "date": row.get("Dt", ""),
                    "open": open_,
                    "close": close,
                    "high": _safe_float(row.get(f"{ticker}_High")),
                    "low": _safe_float(row.get(f"{ticker}_Low")),
                    "volume": _safe_float(row.get(f"{ticker}_Volume")),
                    "change": change,
                    "change_pct": change_pct,
                })
                break
    return results


def get_ticker_history(ticker, limit=30):
    rows = load_rows(limit=limit)
    history = []
    for row in rows:
        close = _safe_float(row.get(f"{ticker}_Close"))
        if close is not None:
            history.append({
                "date": row.get("Dt", ""),
                "open": _safe_float(row.get(f"{ticker}_Open")),
                "high": _safe_float(row.get(f"{ticker}_High")),
                "low": _safe_float(row.get(f"{ticker}_Low")),
                "close": close,
                "volume": _safe_float(row.get(f"{ticker}_Volume")),
            })
    return history
