# Generated by Django 4.1.1 on 2022-12-29 20:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_inventoryitems_price_inventoryitems_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('item_code', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('order_quantity', models.IntegerField(default=0)),
                ('item_price', models.IntegerField(default=0)),
                ('order_price', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('item_group', models.CharField(max_length=500)),
            ],
        ),
    ]
