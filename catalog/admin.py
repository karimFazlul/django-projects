from django.contrib import admin
from catalog.models import Product, Category, ProductReview
from catalog.forms import ProductAdminForm


class ProductAdmin(admin.ModelAdmin):
    # will create a form in admine site with custome validation using ProductAdminForm
    # we are validating the price field, making sure that it is not 0.0
    # whenever we try to do anything with a product object this form will be used 
    # to provide the interface
    form = ProductAdminForm
    # sets values for how the admin site lists  products
    # this fields will be shown at the overview page of products
    list_display = ('name', 'price', 'old_price', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    # this fields will be excluded from editing page
    exclude = ('created_at', 'updated_at',)
    # sets up slug to be generated from product name
    prepopulated_fields = {'slug' : ('name',)}

# registers  product model with the admin site
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists categories
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    #provides search box in the admine site
    # the search will look at this field for a match
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug' : ('name',)}
# registers  category model with the admin site    
admin.site.register(Category, CategoryAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'title', 'date', 'rating', 'is_approved')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['date']
    search_fields = ['user','content','title']
admin.site.register(ProductReview, ProductReviewAdmin)