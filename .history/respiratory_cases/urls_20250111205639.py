from django.urls import path
from .views import predict_view

urlpatterns = [
  path('', predict_view, name='predict_RS'),
  path('clustering', clustering_RS, name='clustering_RS'),
]