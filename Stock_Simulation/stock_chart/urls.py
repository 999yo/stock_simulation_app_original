from django.urls import path
from .views import StockChartView,DelateSaveDataView

urlpatterns = [
    path('stock_chart_view/<int:pk>/', StockChartView.as_view(), name='stock_chart_view'),
    path('delete_saved_data/<int:pk>/', DelateSaveDataView.as_view(), name='delete_saved_data'),

]