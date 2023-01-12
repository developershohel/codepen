from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'home'
urlpatterns = [
    path('', views.index, name='home'),
    path('cookies/', views.work_with_cookies),
    path('check-email-sent', views.check_sent_email, name="email-sent")
]
