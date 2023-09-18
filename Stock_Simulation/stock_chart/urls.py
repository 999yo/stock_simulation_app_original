from django.urls import path
from .views import StockChartView


urlpatterns = [
    path('stock_chart_view/<int:pk>/', StockChartView.as_view(), name='stock_chart_view'),

]