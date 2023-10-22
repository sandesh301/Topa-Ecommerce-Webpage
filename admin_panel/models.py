from django.db import models


# Product Model

class Product_Category(models.Model):
    categoryname = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.categoryname

    class Meta:
        db_table = "ProductCategory"


class ProductTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductCollection(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    Product_name = models.CharField(max_length=100)
    Product_quantity = models.PositiveIntegerField(default=0)
    Product_desc = models.TextField(
        default="Product description not available")
    Product_image = models.ImageField(upload_to='product_images/', blank=True)
    Product_Category = models.ForeignKey(
        Product_Category, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(ProductTag, blank=True)
    collection = models.ForeignKey(
        ProductCollection, on_delete=models.SET_NULL, null=True, blank=True)
    sizes = models.ManyToManyField(ProductSize, blank=True)
    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.Product_name

    @property
    def get_discounted_price(self):
        if self.discount_percentage > 0:
            discount_amount = (self.original_price *
                               self.discount_percentage) / 100
            discounted_price = self.original_price - discount_amount
            return discounted_price
        return self.original_price

    class Meta:
        db_table = "Product"

# Blog Model


class BlogTags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    Title = models.CharField(max_length=500)
    Author = models.CharField(max_length=200)
    Tags = models.ManyToManyField(BlogTags)
    Content = models.TextField(default="Content not available")
    Pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title

    class Meta:
        db_table = "Blog"
