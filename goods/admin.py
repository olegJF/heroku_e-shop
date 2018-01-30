from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, Photo, Brand


class PhotoInLine(admin.TabularInline):
    model = Photo


class ProductInLine(admin.TabularInline):
    list_display = [field.name for field in Product._meta.fields]
    model = Product
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInLine]

    class Meta:
        model = Product


class CategoryAdmin(MPTTModelAdmin):

    # exclude = ('slug',)
    inlines = [ProductInLine]

    class Meta:
        model = Category

        
class BrandAdmin(admin.ModelAdmin):
    #exclude = ('slug',)
    
    class Meta:
        model = Brand

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Photo)
admin.site.register(Brand, BrandAdmin)
