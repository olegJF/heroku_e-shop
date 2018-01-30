from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.detail, name='detail'),
    url(r'^remove/(?P<product_id>\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^add/(?P<product_id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^order_create/$', views.order_create, name='order_create'),
]