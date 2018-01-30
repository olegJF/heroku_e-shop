from django.contrib import admin
from .models import Order, ProductInBasket, Status


class ProductInBasketInLine(admin.TabularInline):
    model = ProductInBasket
    


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInBasketInLine]
    exclude = ('created', 'updated')
    
    
    class Meta:
        model = Order

        
admin.site.register(Order, OrderAdmin)


class ProductInBasketAdmin(admin.ModelAdmin):
    
    #exclude = ('slug',)
    
    class Meta:
        model = ProductInBasket


admin.site.register(ProductInBasket, ProductInBasketAdmin)

   
class StatusAdmin(admin.ModelAdmin):
    #exclude = ('slug',)
    
    class Meta:
        model = Status



admin.site.register(Status, StatusAdmin)
