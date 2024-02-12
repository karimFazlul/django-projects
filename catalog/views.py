from django.shortcuts import render, redirect 
from catalog.models import Category, Product
from django.shortcuts import get_object_or_404
from cart.forms import ProductAddToCartForm
from cart import cart
from stats import statistics
from ecomstore.settings import PRODUCTS_PER_ROW
from .forms import ProductReviewForm
from .models import ProductReview

#* Create your views here.

def index(request):
    page_title = 'eBazar'
    featured = Product.featured.all()[0:PRODUCTS_PER_ROW]
    recently_viewed = statistics.get_recently_viewed(request)
    #* for now I am showing the recommended products on Home page
    #* It should go to Product View page later
    search_recs = statistics.recommended_from_search(request)
    view_recs = statistics.recommended_from_views(request)
    return render(request, 'catalog/index.html', locals())


#* this functin shows a single category 
#* and all products that belongs to the perticular categoy
def show_category(request, category_slug):
    # getting the requested category
    # getting the category where slug == requested slug
    c = get_object_or_404(Category, slug=category_slug)
    # getting all the products that belongs to the category
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    context ={
       "category": c,
       "products": products,
       "page_title": page_title,
       "meta_keywords": meta_keywords,
       "meta_description": meta_description,
    }
    return render(request, 'catalog/shop-grid-left.html', context)
    
#* this function shows a single product details
def show_product(request, product_slug):
    
    # get the product where slug == requested slug
    product = get_object_or_404(Product, slug=product_slug)
    statistics.log_product_view(request, product) # save product view in databse for recommendation purpose

    categories = product.categories.filter(is_active=True)
    page_title = product.name
    meta_keywords = product.meta_keywords
    meta_description = product.meta_description
    product_reviews = ProductReview.approved.filter(product=product).order_by('-date')
    review_form = ProductReviewForm()

    # context ={
    #    "product": product,
    #    "categories": categories,
    #    "page_title": page_title,
    #    "meta_keywords": meta_keywords,
    #    "meta_description": meta_description,
    # }

    if request.method == 'POST':
        
        
        # add to cart...create the bound form
        postdata = request.POST.copy()
        # request parameter is passed to check if the cookies is enable or not
        # have a look at the form itself
        form = ProductAddToCartForm(request, postdata)
        #check if posted data is valid
        if form.is_valid():
            print("success")
            #add to cart and redirect to cart page
            cart.add_to_cart(request) 
            # if test cookie worked, get rid of it
            # the cooke was set on first get request
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                
            # TODO: I will remove it letter to allow user to continue shopping
            return redirect('show_cart')
    else:
        # it’s a GET, create the unbound form.
        form = ProductAddToCartForm(request=request, label_suffix=':')
        # assign the hidden input value to  product slug
        form.fields['product_slug'].widget.attrs['value'] = product_slug
        # set the test cookie on our first GET request
        # to check if user cooke is enable so that we can store cart_id 
        request.session.set_test_cookie()
   
    return render(request,'catalog/product-detail.html', locals())
   