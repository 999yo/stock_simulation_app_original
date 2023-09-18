from django.apps import AppConfig

class StockTradingSimulationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_trading_simulation'

    def ready(self):
        from .signals import delete_user_related_data 