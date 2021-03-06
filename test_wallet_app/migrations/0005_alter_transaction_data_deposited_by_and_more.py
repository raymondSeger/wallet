# Generated by Django 4.0.1 on 2022-01-27 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_wallet_app', '0004_alter_transaction_data_deposited_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_data',
            name='deposited_by',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Deposited By'),
        ),
        migrations.AlterField(
            model_name='transaction_data',
            name='withdrawn_by',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Withdrawn By'),
        ),
    ]
