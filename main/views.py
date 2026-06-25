from django.shortcuts import render
import stocks


def index(request):
    return render(request, "main/home.html")


def stocks_view(request):
    ticker = request.GET.get("ticker", "GSPC")
    if ticker not in stocks.TICKERS:
        ticker = "GSPC"
    latest = stocks.get_latest_prices()
    history = stocks.get_ticker_history(ticker, limit=30)
    return render(request, "main/stocks.html", {
        "latest": latest,
        "history": history,
        "selected_ticker": ticker,
        "selected_label": stocks.TICKER_LABELS.get(ticker, ticker),
        "tickers": [(t, stocks.TICKER_LABELS.get(t, t)) for t in stocks.TICKERS],
    })
