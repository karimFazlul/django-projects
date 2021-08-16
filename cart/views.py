from django.shortcuts import render
from . import cart
import json
from django.http import JsonResponse


# Create your views here.

def show_cart(request):
    if request.method == 'POST':
        # print("="*60)
        # for key, value in request.POST.items():
        #     print('Key: %s' % (key) ) 
        #     # print(f'Key: {key}') in Python >= 3.7
        #     print('Value %s' % (value) )
        #     # print(f'Value: {value}') in Python >= 3.7
        # print("="*60)
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
       
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    return render(request, 'cart/v2/cart.html', locals());

# def update_all_cart_items(request):
#     if request.method == 'POST':
#          cart.update_all_cart_elements(request)
#          data = {"message": "success"}
         
#     cart_items = cart.get_cart_items(request)
#     page_title = 'Shopping Cart'
#     cart_subtotal = cart.cart_subtotal(request)
#     return render(request, 'cart/v2/cart.html', locals());
def update_all_cart_items(request):
    if request.method == 'POST':
         cart.update_all_cart_elements(request)
         data = {"message": "success"}
         return JsonResponse(data)
    # cart_items = cart.get_cart_items(request)
    # page_title = 'Shopping Cart'
    # cart_subtotal = cart.cart_subtotal(request)
    # return render(request, 'cart/v2/cart.html', locals());