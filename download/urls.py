from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='form-page'),
    path('download/', views.result, name='download-page'),
]
