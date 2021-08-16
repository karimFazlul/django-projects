from rest_framework import serializers
from catalog.models import Product,Category
from cart.models import CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')
    def get_categories(self, obj):
        return CategorySerializer(obj.categories.all(), many=True).data


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = '__all__'
    def get_product(self, obj):
        return CategorySerializer(obj.product).data