from rest_framework import serializers
from .models import *


class ProductCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Category
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductCollection
        fields = '__all__'


class ProductSizeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'


class BlogTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTags
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    Tags = BlogTagsSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'
