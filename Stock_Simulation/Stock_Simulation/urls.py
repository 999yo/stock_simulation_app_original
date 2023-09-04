from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock_trading_simulation_index/',include('stock_trading_simulation.urls')),
    path('accounts/',include('accounts.urls'), )
]
