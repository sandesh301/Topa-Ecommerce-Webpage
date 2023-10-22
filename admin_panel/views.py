from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from .models import Product
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


def admin_login(request):
    return LoginView.as_view(template_name='admin_panel/login.html')(request)


@login_required
def AdminPanelView(request):
    product = Product.objects.all()
    all_blog = Blog.objects.all()

    return render(request, 'admin_panel/index.html', {'product': product, 'all_blog': all_blog})


def manageProduct(request):
    products = Product.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect("/manageprod")
            except:
                pass
    else:
        form = ProductForm()

    return render(request, 'admin_panel/manage_product.html', {'form': form, 'products': products})


def editProduct(request, id):
    product = Product.objects.get(id=id)
    categories = Product_Category.objects.all()
    return render(request, 'admin_panel/editProduct.html', {'product': product, 'categories': categories})


def updateProduct(request, id):
    product = Product.objects.get(id=id)
    categories = Product_Category.objects.all()
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
        form.save()
        return redirect('/manageprod')
    return render(request, 'admin_panel/manage_product.html', {'product': product, 'categories': categories})


def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('/manageprod')

# for blog


def manageBlog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect("/manageblog")
            except:
                pass
    else:
        form = BlogForm()

    all_blog = Blog.objects.all()

    return render(request, 'admin_panel/manage_Blog.html', {'form': form, 'all_blog': all_blog})


def editBlog(request, id):
    blog = Blog.objects.get(id=id)
    all_tags = BlogTags.objects.all()
    selected_tags = blog.Tags.all()
    return render(request, 'admin_panel/editBlog.html', {'blog': blog, 'all_tags': all_tags, 'selected_tags': selected_tags})


def updateBlog(request, id):
    blog = Blog.objects.get(id=id)
    form = BlogForm(request.POST, request.FILES, instance=blog)
    if form.is_valid():
        form.save()
        return redirect('/manageblog')
    return render(request, 'admin_panel/manage_Blog.html', {'blog': blog})


def deleteBlog(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect('/manageblog')


# API views for Product model

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductCollectionAPIView(generics.ListCreateAPIView):
    queryset = ProductCollection.objects.all()
    serializer_class = ProductCollectionSerializers


class ProductSizeAPIView(generics.ListCreateAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializers


class ProductDetailAPIVIew(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


# API views for Blog model
class BlogListAPIView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
