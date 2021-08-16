from django.contrib import admin
from checkout.models import Order, OrderItem

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__','date','status','transaction_id','user')
    # add filtering options 
    list_filter = ('status','date')
    # search field
    search_fields = ('email','shipping_name','billing_name','id','transaction_id')
    # add all the order items belongs to this order
    inlines = [OrderItemInline,]
    # this just add a section with a lable based on th first member of the tuple
    # for instance Basic section with especified field and so on
    fieldsets = (
    ('Basics', {'fields': ('status','email','phone')}),
    ('Shipping', {'fields':('shipping_name_first','shipping_name_last','shipping_address_1',
    'shipping_address_2','shipping_city','shipping_state',
    'shipping_zip','shipping_country')}),
    # ('Billing', {'fields':('billing_name','billing_address_1',
    # 'billing_address_2','billing_city','billing_state',
    # 'billing_zip','billing_country')})
    )
admin.site.register(Order, OrderAdmin)