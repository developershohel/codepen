from django.urls import path

from . import views

app_name = 'setting'
urlpatterns = [
    path('dashboard/setting/profile/', views.profile_setting, name='setting_profile'),
    path('dashboard/setting/pen/', views.pen_setting, name='setting_pen'),
    path('dashboard/setting/account/', views.account_setting, name='setting_account'),
    path('dashboard/setting/billing/', views.billing_setting, name='setting_billing'),
    path('dashboard/setting/appearance/', views.appearance_setting, name='setting_appearance'),
    path('dashboard/setting/notification/', views.notification_setting, name='setting_notification'),
    path('dashboard/setting/security/', views.security_setting, name='setting_security'),
    path('dashboard/setting/block-user/', views.block_user_setting, name='setting_block_user'),
]
