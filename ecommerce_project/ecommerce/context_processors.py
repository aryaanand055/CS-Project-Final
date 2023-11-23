from .models import Category , Brand
def categories(request):
    return {'categories': Category.get_all_categories()}
def brands(request):
    return {'brands': Brand.get_all_brands()}
