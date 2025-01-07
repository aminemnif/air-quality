from django.urls import path
from . import views

urlpatterns = [
  path('prediction_form', views.predict, name='prediction_form'),
  path('clustering-detail/', views.clustering_detail, name='clustering_detail'),
  path('association-detail/', views.association_detail, name='association_detail'),
]