def user_image_path(instance, filename):
    # Generate a unique path based on user ID and current date
    user_id = instance.id if instance.id else 'temp'
    today = instance.created_at.strftime('%Y/%m/%d')
    return f'users/{user_id}/{today}/{filename}'

def category_image_path(instance, filename):
    return f'category/{instance.name}/{filename}'

def product_image_path(instance, filename):
    return f'products/{instance.category.name}/{filename}'