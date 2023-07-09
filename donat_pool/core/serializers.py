from rest_framework import serializers
from .models import SiteSettings, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'background',]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name',]

class SiteSettingsSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = SiteSettings
        fields = ['id', 'name', 'categories', 'tags',]
