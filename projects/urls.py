from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_route, name='index'),
    path('test_route1/<str:pk>', views.test_route1, name='param'),
]