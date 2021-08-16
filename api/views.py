from rest_framework.decorators import api_view, permission_classes
from catalog.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer,CartItemSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from cart import cart
from rest_framework import status

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['GET'])
@permission_classes([AllowAny]) # anyone is allowed to see this route
def category_details(request, category_slug):
    # getting the requested category
    # getting the category where slug == requested slug
    c = get_object_or_404(Category, slug=category_slug)
    # getting all the products that belongs to the category
    products = c.product_set.all()
    serializer = ProductSerializer(products, many=True)
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    # return JsonResponse(serializer.data, safe=False)
    return Response(serializer.data)
    
# handle form validation in the front end
# permission must change to IsAuthenticated
@api_view(['POST'])
@permission_classes([AllowAny]) # anyone is allowed to see this route
def add_to_cart(request):
    # if serializer.is_valid must be implemented
    cart.add_to_cart(request) 
    return Response({'message':'product successfully added to cart'}, status=status.HTTP_200_OK) # just send a success message

@api_view(['GET','POST'])
@permission_classes([AllowAny]) # anyone is allowed to see this route
def show_cart(request):
    if request.method == 'GET':
        cart_items = cart.get_cart_items(request)
        serializer = CartItemSerializer(cart_items , many=True)
        return Response(serializer.data)
