from django.urls import path
from . import views

urlpatterns = [
	path('', views.show_checkout, name='checkout'),
    path('receipt/', views.show_receipt, name='checkout_receipt'),
    path('orderDetails/', views.order_details, name='order_details'),
	
]