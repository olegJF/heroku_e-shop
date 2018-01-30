from goods.models import Category, Product, Photo
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.reverse import reverse as api_reverse
from rest_framework.response import Response
from .serializers import CategorySerializer
from .serializers import ProductDetailSerializer
from .serializers import CategoryDetailSerializer
from .serializers import ProductSerializer
from .serializers import PhotoSerializer
from cart.models import Order



class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #pagination_class = CategoryPagination


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug' # for slug search
    

class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    
    
    
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #pagination_class = ProductPagination

    
class PhototListAPIView(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_field='image'

class APIHomeView(APIView):
    
    def get(self, request, format=None):
        data = {
            "products":{
                "count": Product.objects.all().count(),
                "url": api_reverse('products_api', request=request),
                },
            "categories":{
                "count": Category.objects.all().count(),
                "url": api_reverse('categories_api', request=request),
                },
            "orders":{
                "count": Order.objects.all().count(),
                "url": api_reverse('orders_api', request=request),
                },
        }
        return Response(data)
