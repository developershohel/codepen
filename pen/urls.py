from django.urls import path
from . import views

app_name = 'pen'
urlpatterns = [
    path('new-pen/', views.new_pen, name='new_pen'),
    path('<slug:username>/pen/<slug:pen_slug>/', views.single_pen, name='single_pen'),
    path('<slug:username>/pen/edit/', views.pen_edit, name="pen_edit"),
    path('<slug:username>/pen/delete/', views.pen_delete, name="pen_delete"),
    path('pen-filter/', views.pen_filter, name="pen_filter"),
    path('tag/<slug:tag_name>/', views.tag, name="tag"),
    path('pen/save/', views.vms_save_pen, name="save_pen"),
    path('pen/live-edit/', views.vms_live_edit, name="live_edit"),
    path('<slug:username>/pen/full/<slug:pen_slug>/', views.single_pen_full, name='single_pen'),
]
