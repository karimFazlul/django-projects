from django import forms
from catalog.models import Product,ProductReview


# form for admin page
# is used for adding, updating or deleting product in admin page
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    # runs when form.is_valid() is called
    # validates price with custom validations
    # clean_field => runs custom validatio on the especifide field
    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['price']

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        exclude = ('user','product', 'is_approved')

