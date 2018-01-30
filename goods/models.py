# -*- coding: utf-8 -*-
from django.db import models
from unidecode import unidecode
from django.core.urlresolvers import reverse
from .fields import ThumbnailImageField
from mptt.models import MPTTModel, TreeForeignKey

CHOICE_MEASUREMENT = (  ('pcs','шт.'),
                        ('kg','кг.'), 
                        ('l','л.'),)


class Category(MPTTModel):
    name = models.CharField(max_length=100, help_text='Введите название категории',
                            verbose_name='Категория товара', unique=True)
    slug = models.SlugField(blank=True)
    parent = TreeForeignKey('self', verbose_name='Родительская категория', blank=True,
                            null=True, related_name='children', on_delete=models.CASCADE)
    level = models.IntegerField(default=0, db_index=True)
    description = models.TextField(verbose_name='Описание категории', blank=True)
    image = models.ImageField(verbose_name='Фото категории', blank=True, upload_to='category_img')

    def save(self, *args, **kwargs):
        self.slug = '{}'.format(unidecode(self.name).replace('-', '_').replace(' ', '_').replace("'", '').lower())
        if self.parent_id:
            self.level = self.parent.level + 1
        super(Category, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'
        
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Бренд производителя', unique=True)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        self.slug = '{}'.format(unidecode(self.name).replace('-', '_').replace(' ', '_').replace("'", '').lower())
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        
class ProductQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(is_available=True)


class ProductManager(models.Manager):
    
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()
        

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория товара', db_index=True)
    brand = models.ForeignKey(Brand, db_index=True)
    name = models.CharField(max_length=100,  verbose_name='Название товара')
    # slug = models.SlugField(blank=True)
    description = models.TextField(verbose_name='Описание товара', blank=True)
    price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    measurement = models.CharField(max_length=10, choices=CHOICE_MEASUREMENT, default='pcs', verbose_name='измерение')
    value = models.FloatField(default=0, verbose_name='зачение')
    # quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    is_available = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    
    objects = ProductManager()

    # def save(self, *args, **kwargs):
    #     self.slug = '{}'.format(unidecode(self.name).replace('-', '_').replace(' ', '_').lower())
    #     super(Good, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'товары'
        ordering = ['name']

    def __str__(self):
        return '%s_%s_%s_%s' % (self.category, self.brand, self.name, self.value)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"pk": self.pk})
        
        
# def user_directory_path(instance, filename):
#     return 'good_{0}_{1}/{2}'.format(instance.slug, instance.brand, filename)


class Photo(models.Model):
    item = models.ForeignKey(Product, related_name='photos', verbose_name='Товар', on_delete=models.CASCADE)
    # title = models.CharField(max_length=100, verbose_name='Название фото')
    image = ThumbnailImageField(upload_to="goods_img", verbose_name='Фото')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'фотографии'
        ordering = ['pk']

    # def __unicode__(self):
        # return 'For %s _ %s' % (self.item.brand, self.item.name)

    def __str__(self):
        return 'For %s _ %s' % (self.item.brand, self.item.name)



