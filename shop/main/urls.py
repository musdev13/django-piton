from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('mods/<int:mod_id>/', views.mod_detail, name='mod_detail'),
]
