from django.contrib import admin
from django.utils.safestring import mark_safe

from shopmoderno import settings
from .models import Product, Category, Review, ProductImage


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_show', 'available', 'price',)
    list_filter = ('available', 'time_create', 'time_update')
    list_editable = ('available',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ProductImageAdmin,)

    def image_show(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" />')
        return None

    image_show.__name__ = 'Картинка'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ('user', 'product', 'rating', 'review')
    ordering = ('-create_date', 'product', 'user', 'rating')
    list_display = ('user', 'product', 'rating', 'create_date')
    list_display_links = ('user', 'product')
    # readonly_fields = ('user', 'product_review', 'rating', 'review')
