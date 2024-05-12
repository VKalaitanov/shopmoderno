from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Review, ProductImage, ProductSize, Size, Feedback


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = (
    #     'name', 'slug', 'image', 'description', 'price',
    #     'discount_price', 'available', 'category'
    # )

    list_display = ('name', 'image_show', 'available', 'price', 'discount_price')
    list_filter = ('available', 'time_create', 'time_update')
    list_editable = ('available',)
    # readonly_fields = ('slug', )
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


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('email', 'ip_address', 'user')
    list_display_links = ('email', 'ip_address')
    readonly_fields = ('subject', 'email', 'ip_address', 'content', 'user')


admin.site.register(ProductSize)
admin.site.register(Size)
