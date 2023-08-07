from django.db import models

class StockInformation(models.Model):
    ticker_symbol  = models.CharField(blank=True,null=True,max_length=4)
    #平均取得単価
    acquisition_stock_price = models.IntegerField(blank=True,null=True)
    #購入株数
    number_of_shares_purchased = models.IntegerField(blank=True,null=True)
    #シミュレーション株価
    simulation_stock_price = models.IntegerField(blank=True,null=True)  

    def __str__(self):
        return self.title