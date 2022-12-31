from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('list_main', views.list_main, name='list_main'),
    path('logout', views.logout_user, name='logout_user'),
    path('list_groups', views.list_groups, name='list_groups'),
    path('list_inventory', views.list_inventory, name='list_inventory'),
    path('add_sales', views.add_sales, name='add_sales'),
    path('import_data', views.import_data, name='import_data'),
    path('list_alerts', views.list_alerts, name='list_alerts'),
    path('export_host_list', views.export_host_list, name='export_host_list'),
    path('add_group', views.add_group, name='add_group'),
    path('edit_group', views.edit_group, name='edit_group'),
    path('delete_group', views.delete_group, name='delete_group'),
    path('add_inventory', views.add_inventory, name='add_inventory'),
    path('edit_inventory', views.edit_inventory, name='edit_inventory'),
    path('delete_inventory', views.delete_inventory, name='delete_inventory'),
    path('cart_checkout', views.cart_checkout, name='cart_checkout'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('edit_cart', views.edit_cart, name='edit_cart'),
    path('list_customers', views.list_customers, name='list_customers'),
    path('edit_customers', views.edit_customers, name='edit_customers'),
    path('delete_customers', views.delete_customers, name='delete_customers'),
    path('list_orders', views.list_orders, name='list_orders'),
    path('list_order_items', views.list_order_items, name='list_order_items'),

    




]