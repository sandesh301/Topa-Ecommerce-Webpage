from django.db import models
from django.contrib.auth.models import User
from admin_panel.models import Product


# CART MODEL

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.cart_id:
            cart, _ = Cart.objects.get_or_create(user=self.product.user)
            self.cart = cart
        super(CartItem, self).save(*args, **kwargs)


# WISHLIST MODEL
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('admin_panel.Product')

    def __str__(self):
        return f'Wishlist of {self.user.username}'


# Delivery Address Model
class DeliveryAddress(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    phone = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    zip_postalcode = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.full_name
