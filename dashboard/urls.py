from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard_url"),
    path('dashboard/pens/', views.dashboard_pen, name='dashboard_pen'),
    path('dashboard/comments/', views.dashboard_comments, name='dashboard_comments'),
    path('dashboard/media/', views.dashboard_media, name='dashboard_media'),
    path('dashboard/profile/', views.dashboard_profile, name='dashboard_profile'),
    path('dashboard/upload-file/', views.upload_file, name='upload_file'),
    path('dashboard/activities/', views.activities, name="activities")
]
