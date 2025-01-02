

from django.urls import path
from . import views

urlpatterns = [
  path('prediction_form', views.predict, name='predict_test_form'),
]