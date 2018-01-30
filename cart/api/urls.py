# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import *

urlpatterns = [
    
    url(r'^$', OrderListAPIView.as_view(), name='orders_api'),
    #url(r'^photo/$', PhototListAPIView.as_view(), name='photo-api'),
    url(r'^(?P<pk>\d+)/$', OrderDetailAPIView.as_view(), name='order_detail_api'),
    
]
