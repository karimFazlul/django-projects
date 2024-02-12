from django.urls import path
from api import views

urlpatterns = [
    path('categories/',  views.CategoryList.as_view(), name='catagori_list'),
    path('category/<slug:category_slug>', views.category_details, name='category_details'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),

]