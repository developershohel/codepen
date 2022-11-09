from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'pen'
urlpatterns = [
    path('<slug:username>/pen/', views.pen, name='pen'),
    path('<slug:username>/pen/<slug:slug>/', views.single_pen, name='single_pen'),
    path('<slug:username>/pen/edit/', views.pen_edit, name="pen_edit"),
    path('<slug:username>/pen/delete/', views.pen_delete, name="pen_edit"),
    path('tag/<slug:tag_name>/', views.tag, name="tag")
]
