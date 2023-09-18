from django.urls import path
from .views import CalcFormView,StockDataListView,SaveResultsView,AboutStockSimulation,DelateSaveDataView


urlpatterns = [
    path('home', CalcFormView.as_view(), name='home'),
    path('about', AboutStockSimulation.as_view(), name='about'),
    path('stock_data_list/', StockDataListView.as_view(), name='stock_data_list'),
    path('save/', SaveResultsView.as_view(), name='save_results'), 
    path('stock/save/results/', SaveResultsView.as_view(), name='save_results'),
    path('delete_saved_data/<int:pk>/', DelateSaveDataView.as_view(), name='delete_saved_data'),
]