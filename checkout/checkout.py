from cart import cart
from checkout.models import Order, OrderItem
from checkout.forms import CheckoutForm
from . import authnet
from ecomstore import settings
# from django.core import urlresolvers
from django.urls import reverse
import urllib
import decimal
from accounts import profile

# returns the URL from the checkout module for cart
def get_checkout_url(request):
    return reverse('checkout')

def process(request):
    # Transaction results
    # APPROVED = '1'
    # DECLINED = '2'
    # ERROR = '3'
    # HELD_FOR_REVIEW = '4'
    postdata = request.POST.copy()
    # current rendered form does not have any card information
    # that is why i am seeting it manually
    # the reason behind it is the template i am using right now
    # postdata["credit_card_number"] = "1111111111111111"
    # postdata["credit_card_type"] = "VISA"
    # postdata['credit_card_expire_month'] = '05'
    # postdata['credit_card_expire_year'] = "2025"
    # postdata['credit_card_cvv'] = '1234'
    # card_num = postdata.get('credit_card_number','')
    # exp_month = postdata.get('credit_card_expire_month','')
    # exp_year = postdata.get('credit_card_expire_year','')
    # exp_date = exp_month + exp_year
    # cvv = postdata.get('credit_card_cvv','')
    amount = cart.cart_subtotal(request)
    results = {}
    response = authnet.charge_credit_card(amount=amount,card_num='12345678910',exp_date="2035-12",card_cvv="1234")
    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                transaction_id = response.transactionResponse.transId
                order = create_order(request, transaction_id)
                results = {'order_number':order.id,'message':''}
                
            else:
                if hasattr(response.transactionResponse, 'errors') is True:
                    results = {'order_number':0,'message':response.transactionResponse.errors.error[0].errorText}
                    str(response.transactionResponse.errors.error[0].errorCode)

        # Or, print errors if the API request wasn't successful
        else:
            if hasattr(response, 'transactionResponse') is True and hasattr(
                    response.transactionResponse, 'errors') is True:
                results = {'order_number':0,'message':response.transactionResponse.errors.error[0].errorText}
                
            else:
                results = {'order_number':0,'message':response.messages.message[0]['text'].text}
                
    else:
        results = {'order_number':0,'message':'Error processing your order.'}
    
    return results

def create_order(request,transaction_id):
    print("order is being created...................")
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.transaction_id = transaction_id
    order.ip_address = request.META.get('REMOTE_ADDR')
    print("===================" + request.META.get('REMOTE_ADDR') +"================")
    order.user = None
    if request.user.is_authenticated:
        order.user= request.user
    order.status = Order.SUBMITTED
    order.save()
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            # oi.price = decimal.Decimal(ci.price()) # now using @property
            oi.price = ci.price()
            oi.product = ci.product
            oi.save()
        # all set, empty cart
        cart.empty_cart(request)
        # save profile info for future orders
        if request.user.is_authenticated:
            profile.set(request)
    # return the new order object
    return order