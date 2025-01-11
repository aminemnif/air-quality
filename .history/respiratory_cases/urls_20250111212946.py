from django.urls import path
from .views import predict_view,clustering_RS,associationRule_RS

urlpatterns = [
  path('', predict_view, name='predict_RS'),
  path('clustering', clustering_RS, name='clustering_RS'),
  path('associationRule', associationRule_RS, name='associationRule_RS'),
]