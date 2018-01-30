from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from .models import Category, Product, Photo
from cart.forms import CartAddProductForm
from django.views.generic import ListView, DetailView


class CategoryList(ListView):
    model = Category
    template_name = 'goods/index.html'
    context_object_name = 'nodes'



class CategoryDetail(DetailView):
    model = Category
    template_name = 'goods/category_detail.html'
    context_object_name = 'nodes'
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetail, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        # default_products = obj.default_category.all()
        # products = ( product_set | default_products ).distinct()
        context["products"] = product_set
        return context
    
    #return render(request, 'goods/category_detail.html', {'category': category})


class ProductDetail(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'goods/product_detail.html'
    
    #print(pk)
    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        instance = self.get_object()
        print(instance)
        context['photos'] = Photo.objects.filter(item=instance, is_active=True)
        print(context['photos'])
        return context
    
    #form = CartAddProductForm()
    #product = get_object_or_404(Product, id=id, is_available=True)
    # photos = Photo.objects.filter(item__id=id, is_active=True)
    #photos = product.photo_set.filter(is_active=True)
    #form = CartAddProductForm()
    #context = { 'product': product,
    #            'photos': photos, 
    #            'form': form 
    #           }

    #return render(request, 'goods/product_detail.html', context)
