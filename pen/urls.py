from django.urls import path
from . import views

app_name = 'pen'
urlpatterns = [
    path('new-pen/', views.new_pen, name='new_pen'),
    path('<slug:username>/pen/<slug:slug>/', views.single_pen, name='single_pen'),
    path('<slug:username>/pen/edit/', views.pen_edit, name="pen_edit"),
    path('<slug:username>/pen/delete/', views.pen_delete, name="pen_delete"),
    path('tag/<slug:tag_name>/', views.tag, name="tag")
]
