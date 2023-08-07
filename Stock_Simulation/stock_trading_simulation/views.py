from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import CalcForm
import yfinance as yf

class CalcFormView(FormView):
    template_name = "stock_trading_simulation_HTML/stock_index.html"
    form_class = CalcForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = None
        context['current_stock_price'] = None
        return context
    
    def form_valid(self, form):
        acquisition_stock_price = form.cleaned_data['acquisition_stock_price']
        number_of_shares_purchased = form.cleaned_data['number_of_shares_purchased']
        simulation_stock_price = form.cleaned_data['simulation_stock_price']
        ticker_symbol = form.cleaned_data['ticker_symbol']

        if acquisition_stock_price is None or number_of_shares_purchased is None or simulation_stock_price is None or ticker_symbol is None:
            # 1つ以上の必要なフォームフィールドが空白の場合、適切なメッセージやデフォルト値を表示する
            return render(self.request, self.template_name, {
                'form': form,
                'ticker_symbol':ticker_symbol,
                'company_name': None,
                'current_stock_price': None,
                'simulation_stock_price':simulation_stock_price,
                'number_of_shares_purchased':number_of_shares_purchased,
                'acquisition_stock_price':acquisition_stock_price,
                'market_capitalization_at_time_of_purchase': None,
                'simulation_stock_profit_and_loss': None,
                'acquisition_stock_price_fall_5': None,
                'acquisition_stock_price_fall_5_profit_and_loss': None,
            })

        # ここから先は、株価情報の取得や計算を行うコードを記述する
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

        # 購入時時価総額
        market_capitalization_at_time_of_purchase = acquisition_stock_price * number_of_shares_purchased
        # シミュレーション損益
        simulation_stock_profit_and_loss = (simulation_stock_price * number_of_shares_purchased) - market_capitalization_at_time_of_purchase
        # 平均取得単価から5%下落した際の評価額
        acquisition_stock_price_fall_5 = market_capitalization_at_time_of_purchase * number_of_shares_purchased * 0.95 
        # 5%下落時の評価額 
        acquisition_stock_price_fall_5_profit_and_loss = acquisition_stock_price_fall_5 - market_capitalization_at_time_of_purchase

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
            'acquisition_stock_price_fall_5':acquisition_stock_price_fall_5,
            'acquisition_stock_price_fall_5_profit_and_loss':acquisition_stock_price_fall_5_profit_and_loss,
        })
