from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('', views.profiles, name='profiles'),
    path('user-profile/<str:pk>', views.user_profile, name='user_profile'),
    path('user-account/', views.user_account, name='user_account'),
    path('edit-account/', views.edit_account, name='edit_account'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('update-skill/<str:pk>', views.update_skill, name='update_skill'),
    path('delete-skill/<str:pk>', views.delete_skill, name='delete_skill'),
    path('inbox', views.inbox, name='inbox'),
    path('view-message/<str:pk>', views.view_message, name='view_message'),
    path('send-message/<str:pk>', views.send_message, name='send_message')
]