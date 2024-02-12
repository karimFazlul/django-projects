from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name='login'),
	path('register/', views.userRegistration, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('my_account/', views.my_account, name='my_account'),
    path('order_details/<str:order_id>/', views.order_details, name='order_details'),
    path('order_info/', views.order_info, name='order_info'),
    path('password_change/', views.password_change, name='password_change'),
	
]