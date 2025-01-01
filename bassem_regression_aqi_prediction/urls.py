from django.urls import path
from . import views

urlpatterns = [
  path('test_form', views.predict, name='predict_test_form'),
]