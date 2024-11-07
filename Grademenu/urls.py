from django.urls import path
from . import views

urlpatterns = [
    path('Grademenu/', views.Grademenu, name='Grademenu'),
]
