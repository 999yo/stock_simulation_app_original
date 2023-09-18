import yfinance as yf
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from stock_trading_simulation.models import StockInformation
from datetime import datetime, timedelta

class StockChartView(View):
    template_name = 'stock_chart.html/stock_data_detail.html'

    def get(self, request, pk,period="1d"):
        stock_data = get_object_or_404(StockInformation, pk=pk)

        ticker_symbol = stock_data.ticker_symbol + '.T'
        stock = yf.Ticker(ticker_symbol)
        if period == "1d":
            data = stock.history(period="1y", interval="1d", rounding=True)
        elif period == "1w":
            data = stock.history(period="5y", interval="1wk", rounding=True)
        elif period == "1m":
            data = stock.history(period="10y", interval="1mo", rounding=True)
        else:
            data = stock.history(period="1y", interval="1d", rounding=True)
        acquisition_stock_price = stock_data.acquisition_stock_price

        # 必要なデータを取り出す
        timestamps = [ts.timestamp() for ts in data.index]
        prices = data[['Open', 'High', 'Low', 'Close']].values.tolist()

        context = {
            'stock_data': stock_data,
            'symbol': ticker_symbol,
            'timestamps': timestamps,
            'prices': prices,
            'acquisition_stock_price': acquisition_stock_price,
            'selected_period': period 
        }

        return render(request, self.template_name, context)
