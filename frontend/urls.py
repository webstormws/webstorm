from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('loyihalar/', views.projects_all, name='projects'),
    path('api/contact/', views.contact_send, name='contact_send'),
]
