from .models import Category

def categories(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return {'categories': categories}