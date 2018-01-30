from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.serializers import StringRelatedField, PrimaryKeyRelatedField 
from goods.models import Category, Product, Photo, Brand

class CategorySerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='categories_detail_api', lookup_field = 'slug')
    
    class Meta:
        model = Category
        fields = ('name', 'slug', 'url')
        

        
        
class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug')
        
     
class ProductSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='products_detail_api')
    category = CategorySerializer()
    brand = BrandSerializer()
    class Meta:
        model = Product
        fields = ('id', 'category', 'brand', 'name',
         'price', 'is_available', 'url')

         
class CategoryDetailSerializer(ModelSerializer):
    product_set = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = ('name', 'slug', 'parent', 'description', 'product_set')
        
       
class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', 'is_active')
        
        
class ProductDetailSerializer(ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    photos = PhotoSerializer(many=True, read_only=True )
    # print('img', images)
    class Meta:
        model = Product
        fields = ('id', 'category', 'brand', 'name',
        'description', 'price', 'is_available', 'created', 'photos')