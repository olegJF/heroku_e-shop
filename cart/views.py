from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from goods.models import Product
from .cart import Cart
from .models import ProductInBasket, Order
from .forms import CartAddProductForm, OrderCreateForm


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=product, quantity=data['quantity'],
                                  update_quantity=data['update'])
    return redirect('cart:detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')
    
def detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                                                           'quantity': item['quantity'], 
                                                           'update': True
                                                             })
    return render(request, 'cart/detail.html', {'cart': cart})
    
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                ProductInBasket.objects.create(order=order, product=item['product'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'cart/order_created.html',
                                {'order': order})
    form = OrderCreateForm()
    return render(request, 'cart/create_order.html', {'form': form, 'cart': cart})
            