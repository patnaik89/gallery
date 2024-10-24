from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.home, name="home"),
    path('create/', views.create, name="create"),
    path('edit/<str:pk>', views.edit, name="edit"),
    path('delete/<str:pk>', views.delete, name="delete"),
    path('list/', views.image_list, name="image_list"),
    path('gallery/', views.gallery, name="gallery"),


]