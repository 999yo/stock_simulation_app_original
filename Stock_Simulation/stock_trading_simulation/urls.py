from django.urls import path
from .views import CalcFormView

#path関数(アクセスするアドレス、呼び出す処理)を追記
urlpatterns = [
    path('', CalcFormView.as_view(), name='stock_trading_simulation_index'),
]