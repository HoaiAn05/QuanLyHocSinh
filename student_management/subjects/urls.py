from django.urls import path
from . import views

urlpatterns = [
    path('monhoc/', views.monhoc_list, name="monhoc_list"),
    path('monhoc/create/', views.monhoc_create, name="monhoc_create"),
    path('monhoc/<int:pk>/edit/', views.monhoc_update, name="monhoc_update"),
    path('monhoc/<int:pk>/delete/', views.monhoc_delete, name="monhoc_delete"),
]
