from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.index, name='catalog_home'),
	path('category/<slug:category_slug>', views.show_category, name='catalog_category'),
	path('product/<slug:product_slug>', views.show_product, name='catalog_product'),

	# path('update_item/', views.updateItem, name="update_item"),
	# path('process_order/', views.processOrder, name="process_order"),
]

