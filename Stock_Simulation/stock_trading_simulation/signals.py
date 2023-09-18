from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import StockInformation
from django.contrib.auth.models import User

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # ユーザーに紐づいたデータを削除するロジックをここに追加します
    try:
        user_profile = StockInformation.objects.get(user=instance)
        user_profile.delete()
    except StockInformation.DoesNotExist:
        pass  # ユーザープロファイルが存在しない場合は何もしない
