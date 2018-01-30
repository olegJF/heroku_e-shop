# -*- coding: utf-8 -*-

from django.conf.urls import url
from goods import views

urlpatterns = [
    url(r'^$', views.CategoryList.as_view(), name='home'),
    url(r'^product/(?P<pk>\d+)/$', views.ProductDetail.as_view(), name='product_detail'),
    url(r'^category/(?P<slug>[-\w]+)/$', views.CategoryDetail.as_view(), name='category_detail'),
]
