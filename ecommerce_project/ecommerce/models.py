from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories(): 
        return Category.objects.all()    
    
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self): 
        return self.name 
    
class Customer(models.Model): 
    user_name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=100) 
  
    def register(self): 
        self.save() 

    def __str__(self):
        return self.user_name
    
    @staticmethod
    def get_customer_by_email(email): 
        try: 
            return Customer.objects.get(email=email) 
        except: 
            return False
  
    def isExists(self): 
        if Customer.objects.filter(email=self.email): 
            return True
        return False
    

class ProductImage(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products/')
    def __str__(self):
        return f'{self.product.name} - {self.image.name.split("/")[2]}'

class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.FileField(upload_to="uploads/brands/logos", blank=True, null=True)
    poster = models.FileField(upload_to="uploads/brands/posters", blank=True, null=True, help_text="High res backgound image. landscape.")
    dark_background = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tagline = models.CharField(max_length=75, null=True)

    def get_all_brands():
        return Brand.objects.all()

    def __str__(self): 
        return self.name 

@receiver(post_save, sender=ProductImage)
def associate_image_with_product(sender, instance, created, **kwargs):
    if created:
        instance.product.images.add(instance)

class Products(models.Model): 
    name = models.CharField(max_length=60) 
    price = models.IntegerField(default=0) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    tagline = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField( 
        max_length=500, default='', blank=True, null=True) 
    images = models.ManyToManyField(ProductImage, blank=True)
  
    @staticmethod
    def get_products_by_id(ids): 
        return Products.objects.filter(id__in=ids) 
  
    @staticmethod
    def get_product_by_id(id): 
        return Products.objects.filter(id=id)[0] 
  
    @staticmethod
    def get_all_products(): 
        return Products.objects.all() 
  
    @staticmethod
    def get_all_products_by_categoryid(category_id): 
        if category_id: 
            return Products.objects.filter(category=category_id) 
        else: 
            return Products.get_all_products()

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through='CartProduct')

    def __str__(self):
        return f"{self.customer.user_name}"
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,validators=[MaxValueValidator(9)])

    def __str__(self):
        return f"{self.product.name} in Cart for {self.cart.customer.user_name}"
    
    def clean_up(self):
        if self.quantity == 0:
            self.delete()

class Wishlist(models.Model):
    user = models.OneToOneField('Customer',on_delete=models.SET_NULL ,null=True )
    product = models.ManyToManyField(Products)

    def add_to_wishlist(self, product):
        self.products.add(product)

    def remove_from_wishlist(self, product):
        self.products.remove(product)

    def clear_wishlist(self):
        self.products.clear()

    def get_wishlist_items(self):
        return self.product.all()

    def is_in_wishlist(self, product):
        return product in self.products.all()

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order Id: #{self.id} - User: {self.customer.user_name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


from django.contrib import admin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'display_products', 'created_at']
    list_filter = ['created_at']  # Optional: Add a filter for the created_at field

    def display_products(self, obj):
        return ", ".join([item.product.name for item in obj.orderitem_set.all()])
    display_products.short_description = 'Products'

    inlines = [OrderItemInline]
admin.site.register(Order, OrderAdmin)




