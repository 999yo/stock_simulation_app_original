from django.views.generic.edit import FormView
from .forms import CalcForm
import yfinance as yf
from .models import StockInformation
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy

class CalcFormView(FormView):
    template_name = "stock_trading_simulation_HTML/home.html"
    form_class = CalcForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        ticker_symbol = form.cleaned_data['ticker_symbol']
        acquisition_stock_price = form.cleaned_data['acquisition_stock_price']
        number_of_shares_purchased = form.cleaned_data['number_of_shares_purchased']
        simulation_stock_price = form.cleaned_data['simulation_stock_price']
        date = form.cleaned_data['date']
 
        try:
            ticker = ticker_symbol + '.T'
            stock = yf.Ticker(ticker)
            stock_info = stock.info

            if stock_info:
                company_name = stock_info.get('longName')
                current_stock_price = stock_info.get('currentPrice')
            else:
                company_name = None
                current_stock_price = None

        except Exception as e:
            print(e)
            company_name = None
            current_stock_price = None

        if ticker_symbol is None or acquisition_stock_price is None or number_of_shares_purchased is None or simulation_stock_price is None or date is None:
            return render(self.request, self.template_name, {
                'form': form,
                'ticker_symbol': ticker_symbol,
                'company_name': company_name,
                'current_stock_price': current_stock_price,
                'simulation_stock_price': simulation_stock_price,
                'number_of_shares_purchased': number_of_shares_purchased,
                'acquisition_stock_price': acquisition_stock_price,
                'date': date,
            })

        if self.request.POST.get('calculate'):
            market_capitalization_at_time_of_purchase = acquisition_stock_price * number_of_shares_purchased
            simulation_stock_profit_and_loss = (simulation_stock_price * number_of_shares_purchased) - market_capitalization_at_time_of_purchase
            stock_price_down_5per = acquisition_stock_price * 0.95 #購入時株価より5%下がったときの株価
            acquisition_stock_price_fall_5per = market_capitalization_at_time_of_purchase * 0.95 #5%下落したときの時価評価額
            acquisition_stock_price_fall_5per_profit_and_loss = acquisition_stock_price_fall_5per - market_capitalization_at_time_of_purchase
            stock_price_down_10per = acquisition_stock_price * 0.90  # 10%下落
            acquisition_stock_price_fall_10per = market_capitalization_at_time_of_purchase * 0.90
            acquisition_stock_price_fall_10per_profit_and_loss = acquisition_stock_price_fall_10per - market_capitalization_at_time_of_purchase
            stock_price_down_30per = acquisition_stock_price * 0.7  # 10%下落
            acquisition_stock_price_fall_30per = market_capitalization_at_time_of_purchase * 0.7
            acquisition_stock_price_fall_30per_profit_and_loss = acquisition_stock_price_fall_30per - market_capitalization_at_time_of_purchase
        
            return render(self.request, self.template_name, {
                'form': form,
                'ticker_symbol': ticker_symbol,
                'date': date,
                'company_name': company_name,
                'current_stock_price': current_stock_price,
                'simulation_stock_price': simulation_stock_price,
                'number_of_shares_purchased': number_of_shares_purchased,
                'acquisition_stock_price': acquisition_stock_price,
                'market_capitalization_at_time_of_purchase': market_capitalization_at_time_of_purchase,
                'simulation_stock_profit_and_loss': simulation_stock_profit_and_loss,
                'stock_price_down_5per': stock_price_down_5per,
                'acquisition_stock_price_fall_5per': acquisition_stock_price_fall_5per,
                'acquisition_stock_price_fall_5per_profit_and_loss': acquisition_stock_price_fall_5per_profit_and_loss,
                'stock_price_down_10per': stock_price_down_10per,
                'acquisition_stock_price_fall_10per': acquisition_stock_price_fall_10per,
                'acquisition_stock_price_fall_10per_profit_and_loss': acquisition_stock_price_fall_10per_profit_and_loss,
                'stock_price_down_30per': stock_price_down_30per,
                'acquisition_stock_price_fall_30per': acquisition_stock_price_fall_30per,
                'acquisition_stock_price_fall_30per_profit_and_loss': acquisition_stock_price_fall_30per_profit_and_loss,
                })

        return super().form_valid(form)

        
class SaveResultsView(View):
    def post(self, request):
        if request.user.is_authenticated:
            ticker_symbol = request.POST.get('ticker_symbol')
            acquisition_stock_price = request.POST.get('acquisition_stock_price')
            number_of_shares_purchased = request.POST.get('number_of_shares_purchased')
            simulation_stock_price = request.POST.get('simulation_stock_price')
            date = request.POST.get('date')
               
        try:
                ticker = ticker_symbol + '.T'
                stock = yf.Ticker(ticker)
                stock_info = stock.info
                
                if stock_info:
                    company_name = stock_info.get('longName')
                    
                else:
                    company_name = None

        except Exception as e:
            print(e)
            company_name = None
        try:
            market_capitalization_at_time_of_purchase = float(acquisition_stock_price) * int(number_of_shares_purchased)
            simulation_stock_profit_and_loss = (float(simulation_stock_price) * int(number_of_shares_purchased)) - market_capitalization_at_time_of_purchase
            stock_price_down_5per = float(acquisition_stock_price) * 0.95
            acquisition_stock_price_fall_5per = market_capitalization_at_time_of_purchase * 0.95
            acquisition_stock_price_fall_5per_profit_and_loss = acquisition_stock_price_fall_5per - market_capitalization_at_time_of_purchase
            stock_price_down_10per = float(acquisition_stock_price) * 0.9 # 10%下落
            acquisition_stock_price_fall_10per = market_capitalization_at_time_of_purchase * 0.90
            acquisition_stock_price_fall_10per_profit_and_loss = acquisition_stock_price_fall_10per - market_capitalization_at_time_of_purchase
            stock_price_down_30per = float(acquisition_stock_price) * 0.7# 10%下落
            acquisition_stock_price_fall_30per = market_capitalization_at_time_of_purchase * 0.70
            acquisition_stock_price_fall_30per_profit_and_loss = acquisition_stock_price_fall_30per - market_capitalization_at_time_of_purchase

            stock_info = StockInformation(
                user=self.request.user,
                date=date,
                ticker_symbol=ticker_symbol,
                company_name=company_name,
                acquisition_stock_price=float(acquisition_stock_price),
                number_of_shares_purchased=int(number_of_shares_purchased),
                simulation_stock_price=float(simulation_stock_price),
                market_capitalization_at_time_of_purchase=market_capitalization_at_time_of_purchase,
                simulation_stock_profit_and_loss=simulation_stock_profit_and_loss,
                stock_price_down_5per=stock_price_down_5per,
                acquisition_stock_price_fall_5per=acquisition_stock_price_fall_5per,
                acquisition_stock_price_fall_5per_profit_and_loss=acquisition_stock_price_fall_5per_profit_and_loss,
                stock_price_down_10per = stock_price_down_10per,
                acquisition_stock_price_fall_10per = acquisition_stock_price_fall_10per,
                acquisition_stock_price_fall_10per_profit_and_loss = acquisition_stock_price_fall_10per_profit_and_loss,
                stock_price_down_30per = stock_price_down_30per, 
                acquisition_stock_price_fall_30per =  stock_price_down_30per,
                acquisition_stock_price_fall_30per_profit_and_loss = acquisition_stock_price_fall_30per_profit_and_loss
            )
            stock_info.save()
            return JsonResponse({'message': '結果を保存しました。シミュレーションリストで保存した内容を確認できます。'})

        except ValueError:
            return JsonResponse({'message': '入力された情報が不正です。'}, status=400)

class StockDataListView(ListView):
    template_name = "stock_trading_simulation_HTML/stock_data_list.html"
    model = StockInformation
    context_object_name = "stock_data_list"
    paginate_by = 5
    def get_queryset(self):
        queryset = StockInformation.objects.filter(user=self.request.user).order_by('acquisition_stock_price')
        
        for stock_data in queryset:
            try:
                ticker = stock_data.ticker_symbol + '.T'
                stock = yf.Ticker(ticker)
                stock_info = stock.info

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
            except Exception as e:
                print(e)
                stock_data.current_profit_and_loss = None
        return queryset

class DelateSaveDataView(View):
    def get(self, request, pk):
        try:
            saved_data = StockInformation.objects.get(pk=pk)
            saved_data.delete()
        except StockInformation.DoesNotExist:
            pass
        return redirect('stock_data_list')
    
class AboutStockSimulation(View):
    def get(self, request):
        return render(request, 'stock_trading_simulation_HTML/about.html')
