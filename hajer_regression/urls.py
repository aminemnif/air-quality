from django.urls import path
from . import views

urlpatterns = [
  path('', views.regression_concentration, name='regression_concentration'),
]