from django.urls import path
from .views import SendOrderEmailAPIView

urlpatterns = [
    path('send-email/', SendOrderEmailAPIView.as_view(), name='send-email'),
]