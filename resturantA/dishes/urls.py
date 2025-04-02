from django.urls import path
from .views import MenuListView , MenuItemsAPIView


urlpatterns = [
    path('Resturant/menu/', MenuListView.as_view(), name='menu-list'),
    path('Resturant/menu-items/', MenuItemsAPIView.as_view(), name='menu-items'),
]
