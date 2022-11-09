from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from codepen import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('profiles.urls')),
    path('', include('home.urls')),
    path('', include('user.urls')),
    path('', include('dashboard.urls')),
    path('', include('pen.urls')),
    path('', include('setting.urls')),
    path('404/', views.url_not_found, name='404'),
    path('search/', views.search, name='search'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'codepen.views.error_404'
