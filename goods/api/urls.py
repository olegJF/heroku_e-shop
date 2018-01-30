# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from .views import *

urlpatterns = [
    
    url(r'^$', APIHomeView.as_view(), name='home-api'),
    url(r'^orders/', include('cart.api.urls')),
    #url(r'^photo/$', PhototListAPIView.as_view(), name='photo-api'),
    url(r'^products/$', ProductListAPIView.as_view(), name='products_api'),
    url(r'^products/(?P<pk>\d+)/$', ProductDetailAPIView.as_view(), name='products_detail_api'),
    url(r'^categories/$', CategoryListAPIView.as_view(), name='categories_api'),
    url(r'^categories/(?P<slug>[-\w]+)/$', CategoryDetailAPIView.as_view(), name='categories_detail_api'),
]
