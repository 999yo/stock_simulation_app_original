from django import forms
from .models import StockInformation

class CalcForm(forms.ModelForm):
    class Meta:
        model = StockInformation
        exclude=["user","company_name","market_capitalization_at_time_of_purchase",
                "simulation_stock_profit_and_loss","simulation_stock_profit_and_loss","stock_price_down_5per",
                "acquisition_stock_price_fall_5per","acquisition_stock_price_fall_5per_profit_and_loss"]
        labels = {
            "ticker_symbol":"証券コード",
            "acquisition_stock_price":"平均取得単価",
            "number_of_shares_purchased":"購入株数",
            "simulation_stock_price":"シミュレーション株価"
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # キーワード引数からユーザー情報を取得
        super().__init__(*args, **kwargs)
    

    def clean_ticker_symbol(self):
        data = self.cleaned_data['ticker_symbol']
        if data and not data.isnumeric():
            raise forms.ValidationError("証券コードは、4桁の数字を入力してください。")
        return data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance