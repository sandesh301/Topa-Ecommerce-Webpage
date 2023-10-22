from django.urls import path
from .views import *
from topa_payment import views


urlpatterns = [
    # CART URL
    path('cart_View', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity/<int:cart_item_id>/',
         views.update_quantity, name='update_quantity'),

    # WISLIST URL
    path('wishlist_view', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/',
         views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/',
         views.remove_from_wishlist, name='remove_from_wishlist'),

    # CHECKOUT URL
    path('checkout1', views.checkout, name='checkout'),
    path('delivery_form/', views.delivery_form,
         name='delivery_form'),
    path('Delivery_Address/', DeliveryAddressAPI.as_view(),
         name='Delivery-Address'),

    # STRIPE PAYMENT
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failure/', views.payment_failure, name='payment_failure'),

    # KLARNA PAYMENT
    path('Klarnacheckout/', views.klarna_checkout, name='klarna_checkout'),
]
