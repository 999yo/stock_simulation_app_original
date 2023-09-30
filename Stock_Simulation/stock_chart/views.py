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
        stock_info = stock.info
        data = stock.history(period="3y", interval="1d", rounding=True)
        acquisition_stock_price= stock_data.acquisition_stock_price

        if stock_info:
            current_stock_price = stock_info.get('currentPrice')
        else:
            current_stock_price = None
        
        if current_stock_price is not None:
            number_of_shares_purchased = stock_data.number_of_shares_purchased
            market_capitalization_at_time_stock_of_purchase = stock_data.market_capitalization_at_time_of_purchase
            stock_data.current_stock_price = current_stock_price
            # current_profit_and_loss を計算
            current_profit_and_loss = current_stock_price * number_of_shares_purchased - market_capitalization_at_time_stock_of_purchase
            # stock_data に current_profit_and_loss をセット
            stock_data.current_profit_and_loss = current_profit_and_loss
        else:
            stock_data.current_profit_and_loss = None
        
        # 必要なデータを取り出す
        timestamps = [ts.timestamp() for ts in data.index]
        prices = data[['Open', 'High', 'Low', 'Close']].values.tolist()

        context = {
            'stock_data': stock_data,
            'ticker_symbol': ticker_symbol,
            "acquisition_stock_price" :acquisition_stock_price,
            "current_stock_price":current_stock_price,
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