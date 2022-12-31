from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,	logout
from django.contrib.auth.decorators import login_required
from	.models	import *
from django.utils import timezone
from	django.shortcuts	import	render,	get_object_or_404
from django.db.models import Q
from django.db.models import Sum
from datetime import datetime

import	datetime
import	csv
import	os
import	subprocess
import	openpyxl
import	functools
import	pdb
import logging
import	re
import requests
import	json
import time
import random
import string

# Create your views here.

def index(request):
    #return HttpResponse("Hello Worls ")
    return render(request,'products/MenuList.html')

@login_required
def list_main(request):
    return render(request,'products/MenuList.html')

def	login_user(request):
							error=""
							if	request.POST:
										uid=request.POST['uid']
										pwd	=request.POST['pwd']
										user1 = authenticate(username=uid, password=pwd)
										if	user1	is	not	None:
																login(request,user1)
																
																return render(request,"products/MenuList.html", {})
										else:
														error="Invalid	Credentials"
							return	render(request,'products/Login.html',{'error':error})

def	logout_user(request):
				logout(request)
				success="Successfully"
				return	render(request,'products/Login.html',{'success':success})

@login_required
def list_alerts(request):
    
        return render(request,'products/ListAlerts.html',{})

@login_required
def list_groups(request):

        return render(request,'products/ListGroups.html',{'inventorygroup':InventoryGroups.objects.all()})


@login_required
def	export_host_list(request):
					response=HttpResponse(content_type='text/csv')
					response['Content-Disposition']	=	'attachment;	filename=PowerVCHosts'	+	str(datetime.datetime.now())	+	'.csv'
					writer=csv.writer(response)
					writer.writerow(['FSP_/_BMC_IP','Serial','Location','CEC_Name','FSP_Credentials',	'Host_Type',	'Firmware_Level',	'HMC_IP',	'Novalink_IP',	'VIOS1',	'VIOS2',	'Proc_/_Memory',	'Model',	'Network_Ports',	'Fabric_Switch1',	'Fabric_Switch2',	'Primary_VLAN',	'Connected_Storages',	'Owner',	'Squad',	'LAB'])
					hosts={}
					for	h	in	hosts:
								writer.writerow([])
					return	response

@login_required
def add_group(request):
				success=""
				error=""
				ig=""
				now1=timezone.now()
				if	request.POST:
								if	'grp_name'	in	request.POST:
										if	str(request.POST['grp_name']).strip():
												try:
													ig= InventoryGroups.objects.get(pk=str(request.POST['grp_name']).strip())
													error="Inventory Group with the same name already present"
												except	InventoryGroups.DoesNotExist:	
															gname=str(request.POST['grp_name']).strip()
															gdesc=request.POST['grp_desc']
															gdate= now1
															ig=InventoryGroups(name=gname,desc=gdesc,date=gdate)
															ig.save()
															success="Group	is	successfully	created"
										else:
															error="Mandatory	fields	are	missing"
				return render(request,'products/AddGroup.html',{'now':now1,	'psuccess':success,	'perror':error})


@login_required
def edit_group(request):
						perror=""
						psuccess=""
						eg=""
						ig=""
						if	request.POST:
									if	'edit_gr'	in	str(request.POST):
												try:
																eg = InventoryGroups.objects.get(pk=str(request.POST['edit_gr']).strip())
																return render(request,'products/EditGroup.html',{'ig':eg})
												except	InventoryGroups.DoesNotExist:																																	
																perror="Given Inventory Group Doesn't exist"

									elif	'gr_name'	in	str(request.POST):
											if 'gr_desc' in	str(request.POST) :			
												ig=get_object_or_404(InventoryGroups,	pk=str(request.POST['gr_name']).strip())
												ig.desc=request.POST['gr_desc']
												ig.save()
												psuccess="Successfully Edited the Inventory group"
											
						return render(request,'products/EditGroup.html',{'perror':perror,'psuccess':psuccess})


@login_required
def delete_group(request):
						perror=""
						psuccess=""
						dg=""
						ig=""
						if	request.POST:
									if	'delete_gr'	in	str(request.POST):
												try:
																dg = InventoryGroups.objects.get(pk=str(request.POST['delete_gr']).strip())
																return render(request,'products/DeleteGroup.html',{'dg':dg,'perror':perror,'psuccess':psuccess})
												except	InventoryGroups.DoesNotExist:																																	
																perror="Given Inventory Group Doesn't exist"

									elif 'gr_name'	in	str(request.POST):
												ig=get_object_or_404(InventoryGroups,	pk=str(request.POST['gr_name']).strip())
												ig.delete()
												psuccess="Successfully Deleted the Inventory group"
											
						return render(request,'products/DeleteGroup.html',{'perror':perror,'psuccess':psuccess})

@login_required
def list_inventory(request):
	qs=""
	qs=InventoryItems.objects.all()
	item_g=request.GET.get('item_group')
	item_n=request.GET.get('item_name')
	item_c=request.GET.get('item_code')

	if item_g !="" and item_g is not None:
			qs=qs.filter(group=get_object_or_404(InventoryGroups,	pk=str(item_g).strip()))
	if item_n !="" and item_n is not None:
			qs=qs.filter(name__icontains=item_n)
	if item_c !="" and item_c is not None:
			qs=qs.filter(item_code__icontains=item_c)
	
	return render(request,'products/ListInventoryItem.html',{'inventory':InventoryItems.objects.all(),'ig':InventoryGroups.objects.all(),'qs':qs})

@login_required
def edit_cart(request):
		perror=""
		psuccess=""
		cart_list=""
		order_list=""
		edit="Yes"
		if Cart.objects.count()==0:
			edit=""
		if request.POST:
				edit=""
				if 'i_code' in request.POST and request.POST.get('i_code') != "":
							if 'order' in request.POST:
								cart_list=request.POST.getlist('i_code')
								order_list=request.POST.getlist('order')
								i=0
								while i < len(order_list):
									o_item=""
									c_item=""
									c_item=Cart.objects.get(pk=str(cart_list[i]).strip())
									o_item=InventoryItems.objects.get(pk=str(cart_list[i]).strip())
									if order_list[i] != c_item.order_quantity:
										o_item.quantity+=(c_item.order_quantity-int(order_list[i]))
										o_item.save()
										if int(order_list[i])==0:
											c_item.delete()
										else:
											c_item.order_quantity=int(order_list[i])
											c_item.save()
										
									
									i+=1
		its=Cart.objects.all()
		for j in its:
				j.order_price=j.order_quantity * j.item_price
				j.save()
		return render(request,'products/AddSalesItem.html',{'qs':InventoryItems.objects.all(),'ig':InventoryGroups.objects.all(),'edit':edit,'total':Cart.objects.aggregate(Sum('order_price'))['order_price__sum'],'cart':Cart.objects.all()})

@login_required
def update_cart(request):
			perror=""
			psuccess=""
			qs=""
			qs=InventoryItems.objects.all()
			item_g=request.GET.get('item_group')
			item_n=request.GET.get('item_name')
			item_c=request.GET.get('item_code')

			if item_g !="" and item_g is not None:
					qs=qs.filter(group=get_object_or_404(InventoryGroups,	pk=str(item_g).strip()))
			if item_n !="" and item_n is not None:
					qs=qs.filter(name__icontains=item_n)
			if item_c !="" and item_c is not None:
					qs=qs.filter(item_code__icontains=item_c)

			if request.POST:
					if 'i_code' in request.POST and request.POST.get('i_code') != "":
							if 'order' in request.POST:
								cart_list=request.POST.getlist('i_code')
								order_list=request.POST.getlist('order')
								i=0
								while i < len(order_list):
									o_item=""
									c_item=""
									if(int(order_list[i])>0):
										o_item=InventoryItems.objects.get(pk=str(cart_list[i]).strip())
										o_item.quantity-=int(order_list[i])
										o_item.save()
										try:
											c_item=Cart.objects.get(pk=str(cart_list[i]).strip())
											c_item.order_quantity+=int(order_list[i])
											c_item.order_price=int(c_item.order_quantity*c_item.item_price)
											c_item.save()
										except	Cart.DoesNotExist:
												c_item=Cart(item_code=o_item.item_code,name=o_item.name,order_quantity=int(order_list[i]),item_price=o_item.price,order_price=((o_item.price)*(int(order_list[i]))),item_group=str(o_item.group.name))
												c_item.save()
									i+=1
								
			its=Cart.objects.all()
			for j in its:
				j.order_price=j.order_quantity * j.item_price
				j.save()
			return render(request,'products/AddSalesItem.html',{'qs':qs,'ig':InventoryGroups.objects.all(),'total':Cart.objects.aggregate(Sum('order_price'))['order_price__sum'],'cart':its,'perror':perror,'psuccess':psuccess})

@login_required
def clear_cart(request):
			perror=""
			psuccess=""
			item=""
			qs=Cart.objects.all()
			for cart_item in qs:
					try:
						item=InventoryItems.objects.get(pk=str(cart_item.item_code).strip()) 
						item.quantity=item.quantity+cart_item.order_quantity
						item.save()
						cart_item.delete()
					except:
						perror+="Cart Item not found in the inventory "+cart_item.item_code
			
			return render(request,'products/AddSalesItem.html',{'cart':Cart.objects.all(),'qs':InventoryItems.objects.all(),'ig':InventoryGroups.objects.all(),'perror':perror,'psuccess':psuccess})

@login_required
def add_inventory(request):
				success=""
				error=""
				item=""
				now1=timezone.now()
				if	request.POST:
								if	'item_code'	in	request.POST:
										if	str(request.POST['item_code']).strip():
												try:
													item= InventoryItems.objects.get(pk=str(request.POST['item_code']).strip())
													error="Inventory Item with the same Item code  already present"
												except	InventoryItems.DoesNotExist:
															item_code=str(request.POST['item_code']).strip()
															name=str(request.POST['item_name']).strip()
															item_quantity= int(str(request.POST['quantity']).strip())
															item_price=int(str(request.POST['price']).strip())
															date=now1
															group=get_object_or_404(InventoryGroups,	pk=str(request.POST['item_group']).strip())
															item=InventoryItems(item_code=item_code, name=name, quantity=int(item_quantity),price=int(item_price),date=date,group=group)
															item.save()
															success="Inventory Item	is	successfully Added"
										else:
															error="Mandatory	fields	are	missing"
				return render(request,'products/AddInventoryItem.html',{'now':now1,'ig':InventoryGroups.objects.values_list('name',flat=True),	'psuccess':success,	'perror':error})


@login_required
def edit_inventory(request):
						perror=""
						psuccess=""
						item=""
						if	request.POST:
									if	'edit_item'	in	str(request.POST):
												try:
																item = InventoryItems.objects.get(pk=str(request.POST['edit_item']).strip())
																return render(request,'products/EditInventoryItem.html',{'item':item,'ig':InventoryGroups.objects.values_list('name',flat=True)})
												except	InventoryItems.DoesNotExist:																																	
																perror="Given Inventory Item Doesn't exist"

									elif	'item_code'	in	str(request.POST):
												item=get_object_or_404(InventoryItems,	pk=str(request.POST['item_code']).strip())
												item.name=str(request.POST['item_name']).strip()
												item.quantity= int(str(request.POST['quantity']).strip())
												item.price=int(str(request.POST['price']).strip())
												item.group=get_object_or_404(InventoryGroups,	pk=str(request.POST['item_group']).strip())
												item.save()
												psuccess="Inventory Item	is	successfully Edited"
												
											
						return render(request,'products/EditInventoryItem.html',{'ig':InventoryGroups.objects.values_list('name',flat=True),'perror':perror,'psuccess':psuccess})

@login_required
def delete_inventory(request):
						perror=""
						psuccess=""
						item=""
						if	request.POST:
									if	'delete_item'	in	str(request.POST):
												try:
																item = InventoryItems.objects.get(pk=str(request.POST['delete_item']).strip())
																return render(request,'products/DeleteInventoryItem.html',{'ditem':item,'perror':perror,'psuccess':psuccess})
												except	InventoryItems.DoesNotExist:																																	
																perror="Given Inventory Item Doesn't exist"

									elif	'item_code'	in	str(request.POST):
												item=get_object_or_404(InventoryItems,	pk=str(request.POST['item_code']).strip())
												item.delete()
												psuccess="Inventory Item is	successfully Deleted"
												
											
						return render(request,'products/DeleteInventoryItem.html',{'perror':perror,'psuccess':psuccess})


@login_required
def list_customers(request):
	perror=""
	psuccess=""
	qs=Customers.objects.all()
	mobile=request.GET.get('mobile')
	name=request.GET.get('name')
	mail=request.GET.get('mail')
	addr=request.GET.get('address')

	if mobile !="" and mobile is not None:
			qs=qs.filter(group=get_object_or_404(Customers,	pk=str(mobile).strip()))
	if name !="" and name is not None:
			qs=qs.filter(customer_name__icontains=name)
	if mail !="" and mail is not None:
			qs=qs.filter(customer_mailid__icontains=mail)
	if addr !="" and addr is not None:
			qs=qs.filter(customer_address__icontains=addr)


	return render(request,'products/ListCustomers.html',{'customers':qs,'perror':perror,'psuccess':psuccess})

@login_required
def edit_customers(request):
		perror=""
		psuccess=""
		qs=Customers.objects.all()
		return render(request,'products/ListCustomers.html',{'customers':qs,'perror':perror,'psuccess':psuccess})

@login_required
def delete_customers(request):
		perror=""
		psuccess=""
		qs=Customers.objects.all()	
		return render(request,'products/ListCustomers.html',{'customers':qs,'perror':perror,'psuccess':psuccess})


@login_required
def add_sales(request):
        return render(request,'products/AddSalesItem.html',{})


@login_required
def edit_sales(request):
        return render(request,'products/EditSalesItem.html',{})


@login_required
def delete_sales(request):
        return render(request,'products/DeleteSalesItem.html',{})

@login_required
def cart_checkout(request):
		perror=""
		psuccess=""
		size=20
		order=""
		chars=string.ascii_lowercase + string.digits
		rdm='ISKONGNT'+''.join(random.choice(chars) for _ in range(size))
		cust=""


		if request.POST and str(request.POST['mobile']).strip():	

				try:
					cust= Customers.objects.get(pk=str(request.POST['mobile']).strip())
				except	Customers.DoesNotExist:
							mobile=request.POST.get('mobile')
							name=request.POST.get('name')
							mail=request.POST.get('mail')
							addr=request.POST.get('address')
							cust= Customers(customer_mobile=mobile,customer_name=name,customer_mailid=mail,customer_address=addr)
							cust.save()
				order=Orders(order_id=rdm,order_status='Success',order_date=timezone.now(),order_total=int(Cart.objects.aggregate(Sum('order_price'))['order_price__sum']),customer_mobile=Customers.objects.get(pk=cust.customer_mobile))
				order.save()
				for item in Cart.objects.all():
					ist=ItemSales(item_code=item.item_code,item_name=item.name,group=item.item_group,order_quantity=item.order_quantity,item_price=InventoryItems.objects.get(pk=item.item_code).price,order_price=item.order_price,customer_mobile=Customers.objects.get(pk=cust.customer_mobile),order_id=Orders.objects.get(pk=order.order_id))
					ist.save()
					item.delete()
				qs=ItemSales.objects.all()
				qs=qs.filter(order_id=order.order_id)
				return render(request,'products/ConfirmOrder.html',{'cust':cust,'order':order,'qs':qs,'total':qs.aggregate(Sum('order_price'))['order_price__sum'],'psuccess':psuccess,'perror':perror})
		
		return render(request,'products/CartCheckOut.html',{'cust':cust,'cart':Cart.objects.all(),'total':Cart.objects.aggregate(Sum('order_price'))['order_price__sum'],'psuccess':psuccess,'perror':perror})

@login_required
def list_orders(request):
		qs=""
		qs=Orders.objects.all()
		order_id=request.GET.get('order_id')
		order_status=request.GET.get('order_status')
		order_date=request.GET.get('order_date')
		order_total=request.GET.get('order_total')
		order_customer=request.GET.get('order_customer')
		
		if order_id !="" and order_id is not None:
				qs=qs.filter(order_id__icontains=order_id)
		if order_status !="" and order_status is not None:
				qs=qs.filter(order_status__icontains=order_status)
		if order_date !="" and order_date is not None:
				qs=qs.filter(order_date__date=datetime.datetime.strptime(order_date,'%Y-%m-%d').date())
		if order_total !="" and order_total is not None:
				qs=qs.filter(order_total__icontains=order_total)
		if order_customer !="" and order_customer is not None:
				try: 
					qs=qs.filter(customer_mobile=Customers.objects.get(pk=str(order_customer).strip())	)
				except Customers.DoesNotExist:
					qs=qs


		return render(request,'products/ListOrders.html',{'orders':qs})
@login_required
def list_order_items(request):
		qs=""
		qs=ItemSales.objects.all()
		order_id=request.GET.get('order_id')
		
		
		if order_id !="" and order_id is not None:
				try:
					qs=qs.filter(order_id=Orders.objects.get(pk=str(order_id).strip()))
		
				except Orders.DoesNotExist:
					qs=qs
					
		return render(request,'products/ListOrderedItems.html',{'order_items':qs})

@login_required
def import_data(request):
        return render(request,'products/ImportData.html',{})

