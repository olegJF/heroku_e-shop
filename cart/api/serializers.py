from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.serializers import StringRelatedField, PrimaryKeyRelatedField 
from cart.models import Order
#from .cart import Cart


class OrderSerializer(ModelSerializer):
    
    url = HyperlinkedIdentityField(view_name="order_detail_api")
    class Meta:
        model = Order
        fields = [
                'id',
                'customer_name',
                'customer_phone_number',
                'total_price',
                'status',
                'url',
               
        ]

class OrderDetailSerializer(ModelSerializer):
    
    
    class Meta:
        model = Order
        fields = [
                'customer_name',
                'customer_email',
                'customer_phone_number',
                'total_price',
                'status',
                'comment',
                'created',
        ]