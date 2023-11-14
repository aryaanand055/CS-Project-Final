from .models import Category 
def categories(request):
    return {'categories': Category.get_all_categories()}
