from django.urls import path
from . import views

urlpatterns = [
    path('', views.FormPageView.as_view(), name='form-page'),
    path('download/', views.DownloadPageView.as_view(), name='download-page'),
]
