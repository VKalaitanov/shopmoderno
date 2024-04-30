from .models import Product


def product_image_directory_path(instance, filename):
    """Метод для сохранения фотографий по нужному пути"""
    if isinstance(instance, Product):
        return f'product_images/{instance.category.slug}/{instance.slug}/{filename}'
    return f'product_images/{instance.product.category.slug}/{instance.product.slug}/{filename}'
