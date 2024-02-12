from django import forms

# form for adding product to cart
class ProductAddToCartForm(forms.Form):
    # quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2', 'value':'1', 'class':'quantity', 'maxlength':'5'}),
    # error_messages={'invalid':'Please enter a valid quantity.'},
    # min_value=1)
    # quantity = forms.IntegerField(error_messages={'invalid':'Please enter a valid quantity.'},
    # min_value=1)
    quantity = forms.IntegerField(initial = 1, min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())

    # override the default __init__ so we can accept request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # custom validation to check for cookies
    def clean(self):
        if self.request:
            # request.session.test_cookie_worked() returns True if cookie is enabled
            if not self.request.session.test_cookie_worked(): # if cooke is not enabled
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data