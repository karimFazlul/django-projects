from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from checkout.models import Order, OrderItem
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm
from accounts import profile
from django.utils.http import is_safe_url
from django.conf import settings
# Create your views here.

def userRegistration(request, template_name="registration/register.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            # username and password should be taken from form.cleaned_data 
            un = postdata.get('username','')
            pw = postdata.get('password1','')
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = reverse('my_account')
                return redirect(url)
    else:
        form = UserCreationForm()
    page_title = 'User Registration'
    return render(request, "registration/register.html", locals())

def loginUser(request):
    
    #! login form must be changed to a model form to ensure validation(if needed) & security 

    #*  get the redirect-url from user 
    nxt_url = request.GET.get("next", settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        #! form.is_valid must be implemented
        # nxt_url = request.POST.get("next", settings.LOGIN_REDIRECT_URL)
        # username will be taken form clean_data
        #! possible sicurity risk
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            if nxt_url is None: # no redirect-url from user
                # go to my_account page
                return redirect(settings.LOGIN_REDIRECT_URL)

            elif not is_safe_url( # requested redirect-url is not safe
                    url=nxt_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()):
                # go to my_account page
                return redirect(settings.LOGIN_REDIRECT_URL)
            else: # requested redirect-url is safe
                # go to  nxt_url
                return redirect(nxt_url)
    return render(request, "registration/login.html")

@login_required
def my_account(request):
    page_title = 'My Account'
    orders = Order.objects.filter(user=request.user)
    name = request.user.username
    return render(request, "registration/my_account.html", locals())

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)
    return render(request,"registration/order_details.html", locals())

@login_required
def order_info(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        if form.is_valid():
            profile.set(request)
            url = reverse('my_account')
            return redirect(url)
        else:
            user_profile = profile.retrieve(request)
            form = UserProfileForm(instance=user_profile)
        page_title = 'Edit Order Information'
        return render(request,"registration/order_info.html", locals())

def logoutUser(request):
    logout(request)
    return redirect('catalog_home')

def password_change(request):
    return