from django.db import models
from django.contrib.auth.models import User

class StockInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    ticker_symbol  = models.CharField(blank=True,null=True,max_length=4)
    #平均取得単価
    acquisition_stock_price = models.FloatField(blank=True,null=True)
    #購入株数
    number_of_shares_purchased = models.IntegerField(blank=True,null=True)
    #シミュレーション株価
    simulation_stock_price = models.FloatField(blank=True,null=True)  
    #会社名
    company_name = models.TextField(blank=True,null=True)
    #購入時時価総額
    market_capitalization_at_time_of_purchase = models.FloatField(blank=True, null=True)
    #シミュレーション損益
    simulation_stock_profit_and_loss = models.FloatField(blank=True, null=True)
    #5%下落したときの株価
    stock_price_down_5per = models.FloatField(blank=True, null=True)
    #5%下落した時の評価額
    acquisition_stock_price_fall_5per = models.FloatField(blank=True, null=True)
    #5%下落した時の損失益
    acquisition_stock_price_fall_5per_profit_and_loss = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.ticker_symbol}"
    

    
