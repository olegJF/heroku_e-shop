from django.db import models
from goods.models import Product
from django.db.models.signals import post_save

ORDER_STATUS = (
	('new', 'Новый'), 
    ('pending', 'Обрабатывается'),
    ('canceled', 'Отменен'), 
    ('delivered', 'Доставлен'),
    ('paid', 'Оплачен'),
)

class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус заказа')
    slug = models.SlugField(blank=True, unique = True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name='Имя')
    customer_email = models.EmailField(blank=True, verbose_name='email')
    customer_phone_number = models.CharField(max_length=10, verbose_name='Номер телефона')
    total_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    total_price = models.DecimalField(default=0, verbose_name='Сумма', max_digits=10, decimal_places=2)
    # status = models.CharField(max_length=120, choices=ORDER_STATUS, default='new')
    status = models.ForeignKey(Status, verbose_name='Статус заказа', to_field = 'slug', default='new')
    # address =  models.CharField(verbose_name='Адрес', max_length=250)
    comment = models.TextField(blank=True, verbose_name='Доп. информация')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['id']

    def __str__(self):
        return "Заказ № %s" % str(self.pk)
        

class ProductInBasket(models.Model):
    order = models.ForeignKey(Order, blank=True)
    product = models.ForeignKey(Product, blank=True)
    quantity = models.PositiveIntegerField(default=1, blank=True, verbose_name='Количество')
    price_per_item = models.DecimalField(default=0, verbose_name='Цена', max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(default=0, verbose_name='Сумма', max_digits=10, decimal_places=2)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'товары в заказе'
     
    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_amount = self.quantity * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)
        

def all_product_in_order(sender, instance, *args, **kwargs):
    order = instance.order
    all_product = ProductInBasket.objects.filter(order=order)
    total_price = 0
    total_quantity = 0
    for product in all_product:
        total_price += product.total_amount
        total_quantity += product.quantity
        
    instance.order.total_price = total_price
    instance.order.total_quantity = total_quantity
    instance.order.save(force_update=True)
    
post_save.connect(all_product_in_order, sender=ProductInBasket)    
        