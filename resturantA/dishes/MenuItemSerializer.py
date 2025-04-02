# serializers.py
from rest_framework import serializers
from .models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        
    def get_image_url(self, obj):
        if obj.image_url:
            return self.context['request'].build_absolute_uri(obj.image_url.url)
        return None