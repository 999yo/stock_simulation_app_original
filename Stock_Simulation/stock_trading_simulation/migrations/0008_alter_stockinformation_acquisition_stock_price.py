# Generated by Django 4.2.3 on 2023-09-06 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_trading_simulation', '0007_alter_stockinformation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockinformation',
            name='acquisition_stock_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]