from django import forms
from .models import StockInformation

class CalcForm(forms.ModelForm):
    class Meta:
        model = StockInformation
        exclude=[]
        labels = {
            "ticker_symbol":"証券コード",
            "acquisition_stock_price":"平均取得単価",
            "number_of_shares_purchased":"購入株数",
            "simulation_stock_price":"シミュレーション株価"
        }
    def clean_ticker_symbol(self):
        data = self.cleaned_data['ticker_symbol']
        if data and not data.isnumeric():
            raise forms.ValidationError("4桁の数字を入力してください。")
        return data

