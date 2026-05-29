from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('verify/', views.verify_file, name='verify_file'),
    path('history/', views.hash_history, name='hash_history'),
]
