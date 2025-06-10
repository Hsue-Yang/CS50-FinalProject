from django.urls import path

from . import views
urlpatterns = [
    path('home/', views.home),
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
]