from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import CalcForm
import yfinance as yf
from .models import StockInformation
from django.http import JsonResponse
from django.urls import reverse_lazy 
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import redirect

class CalcFormView(FormView):
    template_name = "stock_trading_simulation_HTML/home.html"
    form_class = CalcForm
    success_url = reverse_lazy('stock_trading_simulation_index') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = None
        context['current_stock_price'] = None
        context['calculation_performed'] = False
        return context
      
    def form_valid(self, form):
        ticker_symbol = form.cleaned_data['ticker_symbol']
        acquisition_stock_price = form.cleaned_data['acquisition_stock_price']
        number_of_shares_purchased = form.cleaned_data['number_of_shares_purchased']
        simulation_stock_price = form.cleaned_data['simulation_stock_price']
       
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

        if acquisition_stock_price is None or number_of_shares_purchased is None or simulation_stock_price is None:
            # 1つ以上の必要なフォームフィールドが空白の場合、適切なメッセージやデフォルト値を表示する
            return render(self.request, self.template_name, {
                'form': form,
                'ticker_symbol':ticker_symbol,
                'company_name': company_name,
                'current_stock_price': current_stock_price,
                'simulation_stock_price':simulation_stock_price,
                'number_of_shares_purchased':number_of_shares_purchased,
                'acquisition_stock_price':acquisition_stock_price,
                'market_capitalization_at_time_of_purchase': None,
                'simulation_stock_profit_and_loss': None,
                'acquisition_stock_price_fall_5': None,
                'acquisition_stock_price_fall_5_profit_and_loss': None,
            })
                
        if self.request.POST.get('calculate'):
            # 購入時時価総額
            market_capitalization_at_time_of_purchase = acquisition_stock_price * number_of_shares_purchased
            # シミュレーション損益
            simulation_stock_profit_and_loss = (simulation_stock_price * number_of_shares_purchased) - market_capitalization_at_time_of_purchase
            #平均取得単価から、5%下落したときの株価（平均取得単価×0.95)
            stock_price_down_5per = acquisition_stock_price*0.95
            #平均取得単価から5%下落した際の評価額(購入時時価総額*0.95)
            acquisition_stock_price_fall_5per = market_capitalization_at_time_of_purchase*0.95
            #平均取得単価から5%下落した際の損益(平均取得単価から5%下落した際の評価額-購入時時価総額)
            acquisition_stock_price_fall_5per_profit_and_loss = acquisition_stock_price_fall_5per-market_capitalization_at_time_of_purchase

            return render(self.request, self.template_name, {
            'form': form,
            'ticker_symbol':ticker_symbol,
            'company_name':company_name,
            'current_stock_price':current_stock_price,
            'simulation_stock_price':simulation_stock_price,
            'number_of_shares_purchased':number_of_shares_purchased,
            'acquisition_stock_price':acquisition_stock_price,
            'market_capitalization_at_time_of_purchase': market_capitalization_at_time_of_purchase,
            'simulation_stock_profit_and_loss': simulation_stock_profit_and_loss,
            'stock_price_down_5per':stock_price_down_5per,
            'acquisition_stock_price_fall_5per':acquisition_stock_price_fall_5per,
            'acquisition_stock_price_fall_5per_profit_and_loss':acquisition_stock_price_fall_5per_profit_and_loss,})
        
        return super().form_valid(form)
    
class SaveResultsView(View):
    def post(self, request):
        if request.user.is_authenticated:
            ticker_symbol = request.POST.get('ticker_symbol')
            acquisition_stock_price = request.POST.get('acquisition_stock_price')
            number_of_shares_purchased = request.POST.get('number_of_shares_purchased')
            simulation_stock_price = request.POST.get('simulation_stock_price')
        
        if acquisition_stock_price is None or number_of_shares_purchased is None or simulation_stock_price is None or ticker_symbol is None:
            return JsonResponse({'message': '必要な情報が不足しています。'}, status=400)

        try:
            market_capitalization_at_time_of_purchase = float(acquisition_stock_price) * int(number_of_shares_purchased)
            simulation_stock_profit_and_loss = (float(simulation_stock_price) * int(number_of_shares_purchased)) - market_capitalization_at_time_of_purchase
            stock_price_down_5per = float(acquisition_stock_price) * 0.95
            acquisition_stock_price_fall_5per = market_capitalization_at_time_of_purchase * 0.95
            acquisition_stock_price_fall_5per_profit_and_loss = acquisition_stock_price_fall_5per - market_capitalization_at_time_of_purchase

            stock_info = StockInformation(
                user=self.request.user,
                ticker_symbol=ticker_symbol,
                acquisition_stock_price=float(acquisition_stock_price),
                number_of_shares_purchased=int(number_of_shares_purchased),
                simulation_stock_price=float(simulation_stock_price),
                market_capitalization_at_time_of_purchase=market_capitalization_at_time_of_purchase,
                simulation_stock_profit_and_loss=simulation_stock_profit_and_loss,
                stock_price_down_5per=stock_price_down_5per,
                acquisition_stock_price_fall_5per=acquisition_stock_price_fall_5per,
                acquisition_stock_price_fall_5per_profit_and_loss=acquisition_stock_price_fall_5per_profit_and_loss,
            )
            stock_info.save()
            return JsonResponse({'message': 'データを保存しました。'})

        except ValueError:
            return JsonResponse({'message': '入力された情報が不正です。'}, status=400)

class StockDataListView(ListView):
    template_name = "stock_trading_simulation_HTML/stock_data_list.html"
    model = StockInformation
    context_object_name = "stock_date_list"

    def get_queryset(self):
        return StockInformation.objects.filter(user=self.request.user)

class DelateSaveDataView(View):
    def get(self, request, pk):
        try:
            saved_data = StockInformation.objects.get(pk=pk)
            saved_data.delete()
        except StockInformation.DoesNotExist:
            pass
        return redirect('stock_data_list')