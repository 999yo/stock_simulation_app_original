from django.contrib import admin

from .models import StockInformation  # モデルをインポート

# モデルを管理者パネルに登録
admin.site.register(StockInformation)