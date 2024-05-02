from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='index'),
    path('project/<str:pk>', views.project, name='project'),
]