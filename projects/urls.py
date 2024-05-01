from django.urls import path
from . import views

urlpatterns = [
    path('test_route/', views.test_route, name='testroute'),
    path('test_route1/<str:pk>', views.test_route1, name='param'),
]