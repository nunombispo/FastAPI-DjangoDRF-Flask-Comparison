from django.urls import path
from .views import ItemViewSet

# Create explicit URL patterns to avoid router issues
urlpatterns = [
    path('items/', ItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='item-list'),
    path('items/<int:pk>/', ItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='item-detail'),
]