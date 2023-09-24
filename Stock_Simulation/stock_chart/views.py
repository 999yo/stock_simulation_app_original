import yfinance as yf
from django.shortcuts import render, get_object_or_404
from django.views import View
from stock_trading_simulation.models import StockInformation
from django.shortcuts import redirect



class StockChartView(View):
    template_name = 'stock_chart.html/stock_data_detail.html'

    def get(self, request, pk, period="1d"):
        stock_data = get_object_or_404(StockInformation, pk=pk)

        ticker_symbol = stock_data.ticker_symbol + '.T'
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(period="3y", interval="1d", rounding=True)
        acquisition_stock_price = stock_data.acquisition_stock_price

        # 必要なデータを取り出す
        timestamps = [ts.timestamp() for ts in data.index]
        prices = data[['Open', 'High', 'Low', 'Close']].values.tolist()

        context = {
            'stock_data': stock_data,
            'ticker_symbol': ticker_symbol,
            'acquisition_stock_price': acquisition_stock_price,
            'timestamps': timestamps,
            'prices': prices,
            'selected_period': period 
        }

        return render(request, self.template_name, context)

class DelateSaveDataView(View):
    def get(self, request, pk):
        try:
            stock_data = StockInformation.objects.get(pk=pk)
            stock_data.delete()
        except StockInformation.DoesNotExist:
            pass
        return redirect('stock_data_list')