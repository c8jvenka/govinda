# Generated by Django 4.1.1 on 2022-12-27 18:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryGroups',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ItemSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=200)),
                ('item_name', models.CharField(max_length=500)),
                ('group', models.CharField(max_length=200)),
                ('customer_name', models.CharField(max_length=500)),
                ('customer_mobile', models.CharField(max_length=20)),
                ('customer_mailid', models.EmailField(max_length=254)),
                ('customer_address', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItems',
            fields=[
                ('item_code', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=500)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.inventorygroups')),
            ],
        ),
    ]
