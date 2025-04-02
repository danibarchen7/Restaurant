from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MenuItem
from .MenuItemSerializer import MenuItemSerializer

# class MenuListView(APIView):
#     def get(self, request):
#         menu_items = MenuItem.objects.all()
#         serializer = MenuItemSerializer(menu_items, many=True)
#         return Response(serializer.data)
    
# views.py
class MenuListView(APIView):
    def get(self, request):
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(
            menu_items, 
            many=True,
            context={'request': request}  # Required for absolute URLs
        )
        return Response(serializer.data)

# views.py (Django)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MenuItem

class MenuItemsAPIView(APIView):
    def get(self, request):
        items = MenuItem.objects.all().values('id', 'name')
        return Response(items)
