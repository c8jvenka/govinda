from cgi import print_exception
from pyexpat import model
from unicodedata import name
from django.db import models
from django.utils import timezone
# Create your models here.


class InventoryGroups(models.Model):
    name = models.CharField(max_length=200,	primary_key=True)
    desc = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)

class InventoryItems(models.Model):
    item_code=models.CharField(max_length=200,	primary_key=True)
    name=models.CharField(max_length=500)
    quantity=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    date=models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(InventoryGroups,null=True, on_delete=models.SET_NULL)


class Cart(models.Model):
    item_code=models.CharField(max_length=200,	primary_key=True)
    name=models.CharField(max_length=500)
    order_quantity=models.IntegerField(default=0)
    item_price=models.IntegerField(default=0)
    order_price=models.IntegerField(default=0)
    date=models.DateTimeField(default=timezone.now)
    item_group = models.CharField(max_length=500)



class Customers(models.Model):
    customer_mobile=models.CharField(max_length=20, primary_key=True)
    customer_name=models.CharField(max_length=500)
    customer_mailid=models.EmailField(max_length=254)
    customer_address=models.CharField(max_length=1000)

class Orders(models.Model):
    order_id=models.CharField(max_length=50, primary_key=True)
    order_status=models.CharField(max_length=20)
    order_date=models.DateTimeField()
    order_total=models.IntegerField(default=0)
    customer_mobile=models.ForeignKey(Customers,on_delete=models.CASCADE)

class ItemSales(models.Model):
    item_code=models.CharField(max_length=200)
    item_name=models.CharField(max_length=500)
    group = models.CharField(max_length=200)
    order_quantity=models.IntegerField(default=0)
    item_price=models.IntegerField(default=0)
    order_price=models.IntegerField(default=0)
    customer_mobile=models.ForeignKey(Customers,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Orders,on_delete=models.CASCADE)

