from rest_framework import serializers
from catalog.models import Item

class ItemSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'title', 'url', 'snippet', 'published_at', 'source_name', 'category_name']