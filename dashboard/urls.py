from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard_url"),
    path('dashboard/pens/', views.dashboard_pen, name='dashboard_pen'),
    path('dashboard/comments/', views.dashboard_comments, name='dashboard_comments'),
    path('dashboard/media/', views.dashboard_media, name='dashboard_media'),
    path('dashboard/profile/', views.dashboard_profile, name='dashboard_profile'),
    path('dashboard/followers/', views.dashboard_profile, name='dashboard_followers'),
    path('dashboard/following/', views.dashboard_profile, name='dashboard_following'),
    path('dashboard/profile/', views.dashboard_profile, name='dashboard_profile'),
    path('dashboard/profile/pen/', views.dashboard_profile, name='dashboard_profile_pens'),
    path('dashboard/profile/project/', views.dashboard_profile, name='dashboard_profile_project'),
    path('dashboard/profile/collection/', views.dashboard_profile, name='dashboard_profile_collection'),
    path('dashboard/upload-file/', views.upload_file, name='upload_file'),
    path('dashboard/activities/', views.activities, name="activities")
]
