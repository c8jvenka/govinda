# Generated by Django 4.1.1 on 2022-12-30 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_orders_delete_itemsales'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=200)),
                ('item_name', models.CharField(max_length=500)),
                ('group', models.CharField(max_length=200)),
                ('order_quantity', models.IntegerField(default=0)),
                ('order_price', models.IntegerField(default=0)),
                ('customer_mobile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.customers')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.orders')),
            ],
        ),
    ]
