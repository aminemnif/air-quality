from django.urls import path
from . import views

urlpatterns = [
  path('classify_aqi_bucket', views.predict, name='classify_aqi_bucket'),
]