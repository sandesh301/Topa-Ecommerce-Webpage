from django.urls import path
from .views import *
from topaMain import views

urlpatterns = [
    path('home', views.home, name='topa-home'),
    path('user_home/', views.user_home, name='user_home'),

    path('register', views.register, name='user_register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='logout'),
    path('check_authentication/', views.check_authentication,
         name='check_authentication'),
    path('shop', views.shop, name='shop'),
    path('shop/<int:product_id>/', views.shop, name='shop-detail'),
    path('product_detail', views.product_detail, name='Product Detail'),
    path('product_detail/<int:product_id>/',
         views.product_detail, name='product-detail'),
    path('collection', views.collection, name='collection'),
    path('collection/<int:collection_id>/',
         views.collection, name='collection-by-id'),
    path('get_sizes/', views.get_sizes, name='get-sizes'),
    path('get_products_by_size/<int:size_id>/',
         views.get_products_by_size, name='get-products-by-size'),


    path('about_us', views.about_us, name='About us'),
    path('about1', views.about1, name='about1'),
    path('learn', views.learn, name='learn'),
    path('privacy', views.privacy, name='privacy'),
    path('sustainability', views.sustainability, name='sustainability'),
    path('terms', views.terms, name='terms'),
    path('values', views.values, name='values'),

]
