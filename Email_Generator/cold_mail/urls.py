from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('generate_email/', views.generate_email, name='generate_email'),
]