from django.urls import path, include
from . import views
urlpatterns = [
	path('', views.show_cart, name='show_cart'),
	path('update_all_items/', views.update_all_cart_items, name='update_all_items'),
	
]