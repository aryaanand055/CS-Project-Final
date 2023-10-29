from django.shortcuts import render, redirect
from .models import Customer, Wishlist, CartProduct, Cart, Category, Products
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import F
from django.http import HttpResponseRedirect

def home(req):
    return render(req, "home.html")

def products(req):
    categories = Category.get_all_categories()
    categoryID = req.GET.get('category')
    if categoryID:
        productsList = Products.get_all_products_by_categoryid(categoryID)
    else:
        productsList = Products.get_all_products()
    
    sort_criteria = req.GET.get('sort', 'name')  # Default to sorting by name
    sort_order = req.GET.get('order', 'asc')  # Default to ascending order    
    if sort_criteria == 'name':
        productsList = productsList.order_by('name' if sort_order == 'asc' else '-name')
    elif sort_criteria == 'price':
        productsList = productsList.order_by('price' if sort_order == 'asc' else '-price')
    elif sort_criteria == "id":
        productsList = productsList.order_by("id" if sort_order == "asc" else "-id")

    cust = req.session.get("customer_id")
    if cust:
        customer = Customer.objects.get(id=cust)
        wishlist, created = Wishlist.objects.get_or_create(user=customer)
        wishlist_products = wishlist.get_wishlist_items()
        for product in productsList:
            product.isInWishlist = product in wishlist_products
    else:
        for product in productsList:
            product.isInWishlist = False
    return render(req, 'products.html', {'products_list': productsList, "categories": categories})

def product_detail(req, product_id):
    product = Products.get_product_by_id(product_id)
    categories = Category.get_all_categories()
    cart_quantity = 0
    user = req.session.get("customer_id")
    if user:
        customer = Customer.objects.get(id=user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_quantity1 = CartProduct.objects.filter(cart=cart, product=product)
        if len(cart_quantity1) == 0:
            cart_quantity = 0
        else:
            cart_quantity = cart_quantity1[0].quantity
    return render(req, "product_detail.html", {"product": product, "categories": categories, "cart_quantity": cart_quantity})

def signupUser(req):
    if req.method == 'POST':
        form = CustomUserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            messages.success(req, f"The user {user.user_name} is registered successfully.")
            return redirect('loginUser')
        else:
            messages.error(req, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()
    return render(req, 'signup.html', {'form': form})

def tac(req):
    return render(req, 'tac.html')

def loginUser(request):
    error_message = None
    if request.method == 'POST':
        print(321123)
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        print(email, password, customer)
        if customer:
            if password == customer.password:
                print("Check successful")
                request.session['customer'] = customer.user_name
                request.session['customer_id'] = customer.id
                return redirect('products')
            else:
                print("invalud passwprd")
                error_message = 'Invalid password'
        else:
            error_message = 'Invalid email'

    return render(request, 'login.html', {'error': error_message, 'form': AuthenticationForm()})

def logoutUser(request):
    request.session.clear()
    return redirect('loginUser')

# @login_required
def view_cart(request):
    cust = request.session.get("customer_id")
    cart = Cart.objects.get(customer = cust)
    cart_items = CartProduct.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})
def view_wishlist(request):
    cust = request.session.get("customer_id")
    if cust:
        customer = Customer.objects.get(id=cust)
        # wishlist = Wishlist.get()
        wishlist, created = Wishlist.objects.get_or_create(user=customer)
        products = wishlist.get_wishlist_items()
        print(products)
    else:
        products = [] 
    return render(request, 'wishlist.html', { 'wishlist_items': products})

def add_to_cart(request, product_id):
    product = Products.objects.get(pk=product_id)
    user = request.session.get("customer_id")
    customer = Customer.objects.get(id=user)    
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    from_wishlist = request.GET.get('from_wishlist')

    # Redirect to the appropriate page
    if from_wishlist:
        return redirect('view_cart')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # return redirect('view_cart')

def remove_from_cart1(request, product_id):
    product = Products.objects.get(pk=product_id)
    user = request.session.get("customer_id")
    customer = Customer.objects.get(id=user)    
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity -= 1
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # return redirect('view_cart')

def empty_cart(req):
    print(2343)
    user = req.session.get("customer_id")
    cart = Cart.objects.get(customer=user)
    cart.cartproduct_set.all().delete()
    return redirect("products")

def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                cart_item_id = key.replace('quantity_', '')
                try:
                    cart_item = CartProduct.objects.get(id=cart_item_id)
                    quantity = int(value)
                    if quantity > 0:
                        cart_item.quantity = quantity
                        cart_item.save()
                    else:
                        cart_item.delete()
                except CartProduct.DoesNotExist:
                    pass
    return redirect('view_cart')

def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartProduct.objects.get(id=cart_item_id)
        cart_item.delete()
    except CartProduct.DoesNotExist:
        pass
    return redirect('view_cart')

from django.http import JsonResponse

def add_to_wishlist(request, product_id):
    user_id = request.session.get("customer_id")  # Replace with the actual user's ID
    print("product_id:", product_id)  # Replace with the actual product's ID
    user = Customer.objects.get(id=user_id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    product = Products.objects.get(id=product_id)
    wishlist.product.add(product)
    wishlist.save()
    return JsonResponse({'success': True})

def remove_from_wishlist(request, product_id):
    user_id = request.session.get("customer_id")  # Replace with the actual user's ID
    print("product_id:", product_id)  # Replace with the actual product's ID
    user = Customer.objects.get(id=user_id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    product = Products.objects.get(id=product_id)
    wishlist.product.remove(product)
    wishlist.save()
    return JsonResponse({'success': True})
