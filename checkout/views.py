from django.shortcuts import render, redirect
from django.urls import reverse
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem
from checkout import checkout
from cart import cart
from accounts import profile
from cart import cart

# Create your views here.
def show_checkout(request):
    if cart.is_empty(request):
        cart_url = reverse('show_cart')
        return redirect(cart_url)
    if request.method == 'POST':
        
        postdata = request.POST.copy()
        # current rendered form does not have any card information
        # that is why i am seeting it manually
        # the reason behind it is the template i am using right now
        # postdata["credit_card_number"] = "1111111111111111"
        # postdata["credit_card_type"] = "VISA"
        # postdata['credit_card_expire_month'] = '05'
        # postdata['credit_card_expire_year'] = "2025"
        # postdata['credit_card_cvv'] = '1234'

        print("="*60)
        # for key, value in postdata:
        #     print('Key: %s' % (key) ) 
        #     # print(f'Key: {key}') in Python >= 3.7
        #     print('Value %s' % (value) )
        #     # print(f'Value: {value}') in Python >= 3.7
        print(postdata)
        print("="*60)
        form = CheckoutForm(postdata)
        if form.is_valid():
            response = checkout.process(request)
            order_number = response.get('order_number',0)
            error_message = response.get('message','')
            print(error_message*10)
            if order_number:
                print("hi"*60)
                request.session['order_number'] = order_number
                receipt_url = reverse('checkout_receipt')
                return redirect(receipt_url)
        else:
            error_message = 'Correct the errors below'
            print("="*60)
            print(error_message)
            print("="*60)
    else:
        if request.user.is_authenticated:
            print('++++++++++++++++ Authenticated User +++++++++++++')
            user_profile = profile.retrieve(request)
            # filled the form with user pre-existing information
            form = CheckoutForm(instance=user_profile)
        else:
            print('++++++++++++++++ Unauthenticated User +++++++++++++')
            # empty form
            form = CheckoutForm()
    cart_items = cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)  
    page_title = 'Checkout'
    return render(request,'checkout/v2/checkout.html', locals())

def show_receipt(request):
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session['order_number']
    else:
        cart_url = reverse('show_cart')
        return redirect(cart_url)
    return render(request, 'checkout/v2/receipt.html',locals())

def order_details(request):
    # user = profile.retrieve(request)
    itemset = []
    if request.user.is_authenticated:
        orders = Order.objects.filter(user_id=request.user.id)
        if orders:
            for order in orders:
                itemset.append(OrderItem.objects.filter(order=order)) 
    # print(items) 
    print("="*60)
    for items in itemset:
        for item in items:
            print(item.order.id)           
    return render(request,'checkout/v2/myOrder.html', locals())