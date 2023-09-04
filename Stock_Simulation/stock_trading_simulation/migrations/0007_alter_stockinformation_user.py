# Generated by Django 4.2.3 on 2023-08-31 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock_trading_simulation', '0006_stockinformation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockinformation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
