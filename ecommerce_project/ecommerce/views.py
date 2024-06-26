from django.shortcuts import render, redirect
from .models import *
from .forms import CustomUserCreationForm, CustomUserLogin
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.models import Site
import requests
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST
from django.db.models import Sum, F, FloatField
from decimal import Decimal

def categories(request):
    return {'categories': Category.get_all_categories()}
def brands(request):
    return {'brands': Brand.get_all_brands()}

def home(req):
    return render(req, "home.html", {"navbarmode": "navbar-ligh", "logoInverted":"-inverted"})

def products(req):
    categoryID = req.GET.get('category')
    brandID = req.GET.get('brand')
    if brandID and categoryID:
        productsList = Products.objects.filter(brand=brandID, category=categoryID)
    elif brandID:
        productsList = Products.objects.filter(brand=brandID)
    elif categoryID:
        productsList = Products.objects.filter(category=categoryID)
    else:
        productsList = Products.get_all_products()
    
    sort_criteria = req.GET.get('sort', 'id')  # Default to sorting by id
    sort_order = req.GET.get('order', 'desc')  # Default to ascending desc    #So that new products can be displayed at the first
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
            first_image = product.images.first()
            product.image = first_image.image if first_image else None
            product.isInWishlist = product in wishlist_products
    else:
        for product in productsList:
            first_image = product.images.first()
            product.image = first_image.image if first_image else None
            product.isInWishlist = False

    return render(req, 'products.html', {'products_list': productsList})

def product_detail(req, product_id):
    product = Products.get_product_by_id(product_id)
    productImages = product.images.all()
    categories = Category.get_all_categories()
    cart_quantity = 0
    user = req.session.get("customer_id")
    if user:
        customer = Customer.objects.get(id=user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_quantity1 = CartProduct.objects.filter(cart=cart, product=product)
        wishlist, created = Wishlist.objects.get_or_create(user=customer)
        wishlist_products = wishlist.get_wishlist_items()
        product.isInWishlist = product in wishlist_products
        if len(cart_quantity1) == 0:
            cart_quantity = 0
        
        else:
            cart_quantity = cart_quantity1[0].quantity
    
    
    return render(req, "product_detail.html", {"product": product, "cart_quantity": cart_quantity, "images": productImages})

def signupUser(req):
    if req.method == 'POST':
        form = CustomUserCreationForm(req.POST)
        if form.is_valid():
            # Verify that the data has not been tampered with
            email = form.cleaned_data['email']
            otp = req.POST.get('otp')
            session_otp = req.session.get('otp')
            session_email = req.session.get('email')

            if session_otp and session_email:
                if session_otp == otp and session_email == email:
                    del req.session['otp']
                    # Manually hash the password before saving
                    user = form.save(commit=False)
                    user.password = make_password(form.cleaned_data['password'])
                    user.save()
                    messages.success(req, f"The user {user.user_name} is registered successfully.")
                    return redirect('loginUser')
                else:
                    messages.error(req, "Data mismatch. Registration failed.")
            else:
                messages.error(req, "OTP or email not found.")
        else:
            messages.error(req, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()
    return render(req, 'signup.html', {'form': form})

from django.core.mail import send_mail
import random

def verifyUser(req, email):
    try:
        user =  Customer.objects.get(email = email)
        return JsonResponse({"success": True, "msg": "Customer exists"})
    
    except Customer.DoesNotExist:
        return JsonResponse({"success": False, "msg": "Customer doesn't exist"})


def send_otp_view(request, email):
    if request.method == 'POST':
        otp = ''.join(random.choices('0123456789', k=6))
        request.session['otp'] = otp
        request.session['email'] = email

        # Compose the email message
        subject = 'Your OTP for registration'
        message = f'Your OTP is: {otp}'
        sender_email = 'aryaanand052@gmail.com'  
        recipient_email = email

        try:
            send_mail(subject, message, sender_email, [recipient_email])
            return JsonResponse({'success': True, 'message': f"An OTP has been sent to {email}. Please check your email."})
        except Exception as e:
            print(f'Error sending OTP email: {e}')
            return JsonResponse({'success': False, 'message': "Failed to send OTP. Please try again later."})
    else:
        return JsonResponse({'success': False, 'message': "Invalid request method."})

def change_email(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_email = request.POST.get('new_email')
        otp = request.POST.get('otp')

        if current_password and new_email:
            customerID = request.session.get("customer_id")
            customer = Customer.objects.get(id = customerID)

            if check_password(current_password, customer.password):
                session_otp = request.session.get('otp')
                session_email = request.session.get('email')
                if session_otp and session_email:
                    if session_email == new_email and session_otp == otp:
                
                        customer.email = new_email
                        customer.save()
                        messages.info(request,"Your Email has been updated successfully!")
                        return redirect('profile')
                    else:
                        messages.error(request, "OTP incorrect. Email change reverted.")
                        return redirect('profile')
                else:
                    messages.error(request, "OTP or Email not found")
                    return redirect('profile')
            else:
                messages.error(request, "Incorrect password. Please try again.")
                return redirect('profile')
        else:
            messages.error(request, "Both current password and new email address are required.")
            return redirect('profile')
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        customerID = request.session.get("customer_id")
        customer = Customer.objects.get(id = customerID)
        if check_password(current_password, customer.password):
            customer.password = make_password(new_password)
            customer.save()
            messages.success(request, "Password successfully changed")
            return redirect("profile")
        else:
            messages.error(request, "Password is Incorrect.")
            return redirect('profile')

def verify_otp_view(request, otp):
    print(otp)
    if request.method == 'POST':
        aotp = request.session.get("otp")
        if otp == aotp:  
            return JsonResponse({'success': True, 'message': "OTP verification successful."})
        else:
            return JsonResponse({'success': False, 'message': "Invalid OTP. Please try again."})
    else:
        return JsonResponse({'success': False, 'message': "Invalid request method."})

def tac(req):
    return render(req, 'tac.html')

def loginUser(request):
    if request.method == 'POST':
        form = CustomUserLogin(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email=email).first()
        if customer:
            if check_password(password, customer.password):
                request.session['customer'] = customer.user_name
                request.session['customer_id'] = customer.id
                return redirect('products')
            else:
                messages.warning(request, "Invalid Password. Try again with correct credentials.")
        else:
            print("Email not found")
            messages.warning(request, "Email not found")
    return render(request, 'login.html', {'form': CustomUserLogin()})

def logoutUser(request):
    request.session.clear()
    return redirect('loginUser')

def view_cart(request):
    cust = request.session.get("customer_id")
    if cust:
        cart, created = Cart.objects.get_or_create(customer_id=cust)
        cart_items = CartProduct.objects.filter(cart=cart)
        shippingCharge = ShippingCharge.objects.get(country = "India").charge
        print(shippingCharge)
        # Retrieve all details about the product along with images
        cart_items_with_details = []
        for cart_item in cart_items:
            product = cart_item.product
            product_images = product.images.all()
            product_details = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category,
                'brand': product.brand,
                'description': product.description,
                'images': product_images,
                'quantity': cart_item.quantity
            }
            cart_items_with_details.append(product_details)
        
        return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items_with_details, 'shipping_charge': shippingCharge})
    
    messages.info(request, "Login to add items to cart")
    return redirect("loginUser")

def view_wishlist(request):
    cust = request.session.get("customer_id")
    if cust:
        customer = Customer.objects.get(id=cust)
        
        wishlist, created = Wishlist.objects.get_or_create(user=customer)
        products = wishlist.get_wishlist_items()
        for product in products:
            first_image = product.images.first()
            product.image = first_image.image if first_image else None
        
    else:
        products = [] 
    return render(request, 'wishlist.html', { 'wishlist_items': products})


def add_to_cart(request, product_id):
    # Check whether the user is logged in
    cust = request.session.get('customer_id')
    if not cust:
        messages.info(request, "Login to add items to cart")
        return redirect("loginUser")
        
    if request.method == 'POST':
        from_wishlist = request.GET.get("from_wishlist")
        product = Products.objects.get(pk=product_id)
        user = request.session.get("customer_id")
        customer = Customer.objects.get(id=user)    
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if from_wishlist:
            user = Customer.objects.get(id=request.session.get("customer_id"))
            wishlist, created = Wishlist.objects.get_or_create(user=user)
            product = Products.objects.get(id=product_id)
            wishlist.product.remove(product)
            wishlist.save()
            if(cart_item.quantity + 1 > 9):
                response_data = {
                    'success': True,
                    'message': 'Product moved to cart successfully.',
                    'cart_quantity': cart_item.quantity
                    }
                return JsonResponse(response_data)

        if not created:
            if (cart_item.quantity + 1 > 9 ):
                messages.error(request,"Item quantity cannot exceed 9.")
                response_data = {
                    'success': False,
                    'message': 'Product cannot be added to cart as quantity exceeds 9',
                    'cart_quantity': cart_item.quantity
                }
                return JsonResponse(response_data)
            else:
                cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()
        
        update_cart_pricing(request)
        response_data = {
            'success': True,
            'message': 'Product added to cart successfully.',
            'cart_quantity': cart_item.quantity
        }
        return JsonResponse(response_data)

def remove_from_cart1(request, product_id):
    if request.method == 'POST':
        product = Products.objects.get(pk=product_id)
        user = request.session.get("customer_id")
        customer = Customer.objects.get(id=user)    
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.quantity = 0
            cart_item.save()
            zero_quantity_cart_items = CartProduct.objects.filter(quantity=0)
            for cart_item in zero_quantity_cart_items:
                cart_item.clean_up()
        update_cart_pricing(request)
        response_data = {
            'success': True,
            'message': 'Product removed from cart successfully.',
            'cartQuantity': cart_item.quantity,
        }
        return JsonResponse(response_data)

def remove_all_from_cart(request, product_id):
    if request.method == 'POST':
        product = Products.objects.get(pk=product_id)
        user = request.session.get("customer_id")
        customer = Customer.objects.get(id=user)    
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        
        cart_item.quantity = 0
        cart_item.save()
        zero_quantity_cart_items = CartProduct.objects.filter(quantity=0)
        for cart_item in zero_quantity_cart_items:
            cart_item.clean_up()
        update_cart_pricing(request)
        response_data = {
            'success': True,
            'message': 'Product removed from cart successfully.',
            'cartQuantity': cart_item.quantity,
        }
        return JsonResponse(response_data)

def update_cart_pricing(request):
    user_id = request.session.get("customer_id")
    if user_id:
        cart = Cart.objects.get(customer=user_id)
        cart_items = CartProduct.objects.filter(cart=cart)
        total_price = cart_items.aggregate(total_price=Sum(F('quantity') * F('product__price'), output_field=FloatField()))['total_price'] or Decimal('0')
        cart.total_price = total_price
        if cart.offer:
            discount_percentage = cart.offer.discount_percentage
            print(discount_percentage)
            discounted_price = int(total_price) - int(int(total_price)*int(discount_percentage)/100)
            cart.discounted_price = discounted_price
        else:
            cart.discounted_price = total_price
        cart.save()

        return JsonResponse({'success': True, 'message': 'Cart pricing updated successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'User not logged in'}, status=400)

def empty_cart(req):
    user = req.session.get("customer_id")
    cart = Cart.objects.get(customer=user)
    cart.cartproduct_set.all().delete()
    cleanCart()
    update_cart_pricing(req)
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
                        zero_quantity_cart_items = CartProduct.objects.filter(quantity=0)
                        for cart_item in zero_quantity_cart_items:
                            cart_item.clean_up()
                except CartProduct.DoesNotExist:
                    pass
    update_cart_pricing(request)
    return redirect('view_cart')


def update_cart1(request, product_id, quantity):
    if request.method == 'POST':
        product = Products.objects.get(pk=product_id)
        user = request.session.get("customer_id")
        customer = Customer.objects.get(id=user)    
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()
        update_cart_pricing(request)
        return JsonResponse({'success': True})
    else:
        update_cart_pricing(request)
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
from django.http import JsonResponse

def remove_from_cart(request, product_id):
    if request.method == 'GET':
        product = Products.objects.get(pk=product_id)
        user_id = request.session.get("customer_id")
        
        if user_id:
            try:
                customer = Customer.objects.get(id=user_id)
                cart = Cart.objects.get(customer=customer)
                cart_item = CartProduct.objects.get(cart=cart, product=product)
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
                    zero_quantity_cart_items = CartProduct.objects.filter(quantity=0)
                    for cart_item in zero_quantity_cart_items:
                        cart_item.clean_up()
                # Return a JSON response indicating success
                update_cart_pricing(request)
                response_data = {
                    'success': True,
                    'message': 'Product removed from cart successfully.',
                    'cartQuantity': cart_item.quantity if cart_item.quantity > 0 else 0,
                }
                return JsonResponse(response_data)
            except (Customer.DoesNotExist, Cart.DoesNotExist, CartProduct.DoesNotExist):
                # Handle the case where the user or cart does not exist, or the product is not in the cart
                response_data = {
                    'success': False,
                    'message': 'Error: Unable to remove product from cart.',
                }
                return JsonResponse(response_data, status=400)
        else:
            # Handle the case where the user is not logged in
            response_data = {
                'success': False,
                'message': 'Error: User not logged in.',
            }
            return JsonResponse(response_data, status=400)


def cleanCart() :
    zero_quantity_cart_items = CartProduct.objects.filter(quantity=0)

    for cart_item in zero_quantity_cart_items:

        cart_item.clean_up()


def add_to_wishlist(request, product_id):
    user_id = request.session.get("customer_id") 
    if not user_id:
        return JsonResponse({'success': False, 'msg': "User not logged in"})
    else:
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

def profile(req):
    customer_id = req.session.get('customer_id')
    if req.method == "GET":
        if customer_id:
            customer = Customer.objects.filter(id=customer_id).first()
            user_orders = Order.objects.filter(customer=customer)
            for order in user_orders:
                total_price = sum(item.product.price * item.quantity for item in order.orderitem_set.all())
                order.total_price = total_price
            return render(req,'profile.html',{"user":customer, 'user_orders': user_orders})
        else:
            return redirect("loginUser")
    else:
        uname = req.POST.get('user_name')
        fname = req.POST.get('first_name')
        lname = req.POST.get('last_name')
        email = req.POST.get('email')
        # password = req.POST['password']
        if Customer.objects.filter(user_name=uname).exclude(id=customer_id).exists():
            messages.error(req, 'Username is already taken. Please choose a different username.')
            return redirect('profile')
        customer_id = req.session.get('customer_id')
        customer = Customer.objects.filter(id=customer_id).update(user_name=uname,first_name = fname, last_name = lname)
        messages.success(req,"Your Profile has been updated successfully!")
        return redirect('profile')

def reset_password(req):
    if req.method == "GET":
        return render(req, "forgot_password.html")
    elif req.method == "POST":
        email = req.POST.get('email')
        otp = req.POST.get('otp')
        session_otp = req.session.get('otp')
        session_email = req.session.get('email')
        if session_otp and session_email:
            if session_otp == otp and session_email == email:
                del req.session['otp']
                del req.session['email']
                user = Customer.objects.get(email = email)
                user.password = make_password(req.POST.get("password"))
                user.save()
                messages.success(req, f"The user {user.user_name}'s password has been changed successfully")
                return redirect('loginUser')
            else:
                messages.error(req, "The entered otp is incorrect")
                return redirect('reset_password')
        else:
            messages.error(req, "OTP or email not found.")
            return redirect('reset_password')

        
        


def deleteUser(req):
    if req.method == 'POST':
        pswd = req.POST.get('password')
        customer_id = req.session.get('customer_id')
        customer = Customer.objects.filter(id=customer_id).first()
        if customer.password == pswd:
            customer.delete()
            req.session.clear()
            return JsonResponse({"success": True, "msg": "User deleted successfully"})
        else:
            return JsonResponse({"success": False, "msg": "Password is incorrect"})
    else:
        return JsonResponse({"success": False, "msg": "Invalid request method"})    

def get_top_products(request):
    filter_term = request.GET.get('filter', '')
    top_products = Products.objects.filter(name__icontains=filter_term)[:5]
    top_products_data = [{'id': product.id, 'name': product.name} for product in top_products]
    return JsonResponse(top_products_data, safe=False)

def brand_details(req, brand_id):
    brand = Brand.objects.get(id=brand_id)
    products = Products.objects.filter(brand=brand)
    for product in products:
            first_image = product.images.first()
            product.image = first_image.image if first_image else None
    navmode = ""
    logomode = ""
    if brand.dark_background == True:
        navmode="navbar-ligh"
        logomode = "-inverted"
    return render(req, 'brand_detail.html', {'brand': brand, 'products_list': products, 'navbarmode': navmode, "logoInverted":logomode})

# Checkout

def get_user_location(ip_address):
    # Use ipstack API to get geolocation information
    ipstack_access_key = '96cca56bb0a73cc28523a414c620da59'
    api_url = f'http://api.ipstack.com/{ip_address}?access_key={ipstack_access_key}'
    response = requests.get(api_url)
    data = response.json()
    return data.get('city', 'Unknown City'), data.get('region_name', 'Unknown Region'), data.get('country_name', 'Unknown Country')

# views.py or a utility module
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip, None 


def checkout(request):
    user = request.session.get("customer_id")
    customer = Customer.objects.get(id=user)

    name = customer.user_name
    fname = customer.first_name
    lname = customer.last_name
    email = customer.email

    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown User Agent')
    client_ip, is_routable = get_client_ip(request)

    city, region, country = get_user_location(client_ip)
    current_site = Site.objects.get_current()
    website_name = current_site.name
    website_url = request.build_absolute_uri('/')

    products_and_quantities = []
    cart = Cart.objects.get(customer=user)
    cart_items = CartProduct.objects.filter(cart=cart)

    shippingcharge = ShippingCharge.objects.get(country = "India").charge
    order = Order.objects.create(customer=customer, total_price=cart.total_price, offer = cart.offer, discounted_price = cart.discounted_price, shippingcharge = int(shippingcharge))

    for cart_item in cart_items:
        product = cart_item.product
        quantity = cart_item.quantity
        price = cart_item.product.price
        totalProductPrice = price * quantity
        products_and_quantities.append((product.name, quantity, price, totalProductPrice))
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
    order.save()
    table_rows = ""
    for item in products_and_quantities:
        product, quantity, price, totalProductPrice = item
        table_rows += f"<tr><td>{product}</td><td>{quantity}</td><td>{price}</td><td>{totalProductPrice}</td></tr>"

    # Include location details in the context
    html_message = render_to_string('checkout_email.html', {
        'username': name,
        'name': fname + " " + lname,
        'email': email,
        'user_agent': user_agent,
        'client_ip': client_ip,
        'website_name': website_name,
        'website_url': website_url,
        'city': city,
        'region': region,
        'country': country,
        'table_rows': table_rows,
    })

    subject = 'Checkout Request'
    from_email = 'aryaanand053@gmail.com'
    recipient_email = 'aryaanand050@gmail.com'
    send_mail(subject, '', from_email, [recipient_email], html_message=html_message)
    remove_coupon(request)
    update_cart_pricing(request)
    empty_cart(request)

    return render(request, 'checkout_success.html', {"products_list": products_and_quantities, "order": order})

def remove_coupon(request):
    try:
        user = request.session.get("customer_id")
        customer = Customer.objects.get(id=user)
        cart = Cart.objects.get(customer=customer)
        cart.offer = None
        cart.save()
        update_cart_pricing(request)
        return JsonResponse({'success': True, 'message': 'Offer is removed'})

    except:
        return JsonResponse({'success': False, 'message': 'Offer is not removed'})
    

@require_POST
def apply_offer(request):
    offer_code = request.POST.get('offer_code')
    print(offer_code)
    try:
        offer = Offer.objects.get(code=offer_code)
    except Offer.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid offer code'})
    user = request.session.get("customer_id")
    cart = Cart.objects.get(customer=user)
    cart.offer = offer
    update_cart_pricing(request)
    cart.save()
    return JsonResponse({'success': True, 'message': 'Offer applied successfully'})