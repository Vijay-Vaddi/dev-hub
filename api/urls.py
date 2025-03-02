from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('remove-tag/', views.delete_tags, name='remove_tag'),
    path('', views.get_routes, name='get_routes'),
    path('projects/',views.get_projects, name='get_projects'),
    path('projects/<str:pk>/',views.get_project, name='get_projects'),
    path('projects/<str:pk>/vote/',views.project_vote, name='project_vote'),
]

