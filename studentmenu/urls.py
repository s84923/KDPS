from django.urls import path
from . import views

urlpatterns = [
    path('studentmenu/', views.studentmenu, name='studentmenu'),
]
