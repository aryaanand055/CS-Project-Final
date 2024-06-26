from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.products , name='products'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('signup', views.signupUser , name='signupUser'),
    path('login', views.loginUser , name='loginUser'),
    path('logout', views.logoutUser , name='logoutUser'),
    path('cart', views.view_cart , name='view_cart'),
    path('wishlist', views.view_wishlist , name='view_wishlist'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart , name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart1 , name='remove_from_cart1'),
    path('remove_all_from_cart/<int:product_id>/', views.remove_all_from_cart , name='remove_all_from_cart'),
    path('empty_cart', views.empty_cart , name='empty_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('update_cart1/<int:product_id>/<int:quantity>', views.update_cart1, name='update_cart1'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('termsandconditions', views.tac , name='tac'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist , name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist , name='remove_from_wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('deleteUser/', views.deleteUser, name='deleteUser'),
    path('get_top_products/', views.get_top_products, name='get_top_products'),
    path('brand/<int:brand_id>', views.brand_details, name='brand_details'),
    path('apply_offer/', views.apply_offer, name='apply_offer'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon/'),
    path('send-otp/<str:email>', views.send_otp_view, name='send_otp'),
    path('verify-otp/<str:otp>', views.verify_otp_view, name='verify_otp'),
    path('change_email/', views.change_email, name='change_email'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('verifyUser/<str:email>', views.verifyUser, name='verifyUser'),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)