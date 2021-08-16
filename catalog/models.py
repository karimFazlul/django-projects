from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# model manager for active categories
class ActiveCategoryManager(models.Manager):
    def get_query_set(self):
        return super().get_query_set().filter(is_active=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,help_text='Unique value for product page URL, created from name.')
    description = models.TextField(null = True, blank = True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=255, help_text="Comma-delimited set of SEO keywords for meta tag",null = True, blank = True)
    meta_description = models.CharField("Meta Description", max_length=255,help_text='Content for description meta tag', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # model managers
    objects = models.Manager()
    active = ActiveCategoryManager()
    class Meta:
        # table name in the database that will overwrite django's default name app_modelName
        db_table = 'categories'
        ordering = ['-created_at']
        # explecitely defining the plural form of our model name
        # django e-commerce page-53
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # this will retur  an url using the pattern used in catalog_category(name of the url)
        # ecomstore/produc/product_slug/
        return reverse('catalog_category', kwargs={ 'category_slug': self.slug })

# model manager for active products
class ActiveProductManager(models.Manager):
    def get_query_set(self):
        return super().get_query_set().filter(is_active=True)

# model manager for featured products
class FeaturedProductManager(models.Manager):
    def all(self):
        return super(FeaturedProductManager, self).all().filter(is_active=True).filter(is_featured=True)

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,help_text='Unique value for product page URL, created from name.')
    brand = models.CharField(max_length=50)
    # sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00)
    # image = models.CharField(max_length=100)
    # image = models.ImageField(upload_to='images/products/main', null = True, blank = True)
    thumbnail = models.ImageField(upload_to='images/products/thumbnails', null = True, blank = True)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null = True, blank = True)
    meta_description = models.CharField(max_length=1000, help_text='Content for description meta tag', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category,blank = True)
    # model managers
    objects = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()
    class Meta:
        # table name in the database
        db_table = 'products'
        ordering = ['-created_at']
    def __str__(self):
        return self.name
    # returns the url for each product
    def get_absolute_url(self):
        return reverse('catalog_product', kwargs={ 'product_slug': self.slug })
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None
    
    # this one returns orders that have  currnet item in it 
    def cross_sells(self):
        from checkout.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self) # get all orders that have this product in it 
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self) # eclude the current product from order items
        products = Product.active.filter(orderitem__in=order_items).distinct() # get all distinct items
        return products
    # this one provides full user shopping list who bought current items
    # this one provides more data about possible related product then the previous one
    def cross_sells_user(self):
        from checkout.models import Order, OrderItem
        from django.contrib.auth.models import User
        users = User.objects.filter(order__orderitem__product=self) # get the users who have bought the current product
        items = OrderItem.objects.filter(order__user__in=users).exclude(product=self) # get all order items of those users, ecept this product
        products = Product.active.filter(orderitem__in=items).distinct() # get all distinct items
        return products

    def cross_sells_hybrid(self):

        from checkout.models import Order, OrderItem
        from django.contrib.auth.models import User
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(   Q(order__in=orders) |
                                            Q(order__user__in=users)
                                        ).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products
    
class ActiveProductReviewManager(models.Manager):
    def all(self):
        return super(ActiveProductReviewManager, self).all().filter(is_approved=True)
        
class ProductReview(models.Model):
    RATINGS = ((5,5),(4,4),(3,3),(2,2),(1,1),)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
    is_approved = models.BooleanField(default=True)
    content = models.TextField()
    objects = models.Manager()
    approved = ActiveProductReviewManager()