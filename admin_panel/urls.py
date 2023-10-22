from django import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from admin_panel import views
urlpatterns = [
    path('admin_login', views.admin_login, name='admin_login'),
    path('panel/', views.AdminPanelView, name='AdminPanel'),
    # Product path
    path('manageprod', views.manageProduct, name='manage-product'),
    path('editProduct/<int:id>', views.editProduct, name="edit-product"),
    path('updateProduct/<int:id>', views.updateProduct, name="update-product"),
    path('delete/<int:id>', views.deleteProduct, name="delete-product"),

    # Blog path
    path('manageblog', views.manageBlog, name='manage-blog'),
    path('editBlog/<int:id>', views.editBlog, name="edit-blog"),
    path('updateBlog/<int:id>', views.updateBlog, name="update-blog"),
    path('deleteBlog/<int:id>', views.deleteBlog, name="delete-blog"),

    # Api path
    path('products/', ProductListAPIView.as_view(), name='Product-list'),
    path('Collection/', ProductCollectionAPIView.as_view(),
         name='Product-Collection'),
    path('Size/', ProductSizeAPIView.as_view(), name='Product-Size'),

    # path('product/<int:pk>/', ProductDetailAPIVIew.as_view(), name='product-detail'),
    path('blogs/', BlogListAPIView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogDetailAPIView.as_view(), name='blog-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
