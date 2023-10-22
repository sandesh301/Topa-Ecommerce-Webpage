from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product_Category),
admin.site.register(Product),
admin.site.register(ProductCollection),

admin.site.register(ProductSize),
admin.site.register(ProductTag),
admin.site.register(BlogTags),
admin.site.register(Blog)