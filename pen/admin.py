from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from .models import *


# Register your models here.
class PenList(admin.ModelAdmin, ChangeList):
    list_display = ('id', 'username', 'pen_title', 'pen_status', 'pen_modified', 'pen_published')


class PenDataList(admin.ModelAdmin):
    list_display = ('username', 'pen_title')


class PenAssetsList(admin.ModelAdmin):
    list_display = ('username', 'pen_title')


class PenSettingList(admin.ModelAdmin):
    list_display = ('user', 'theme')


class PenCommentsList(admin.ModelAdmin):
    list_display = ('id', 'pen_id', 'user_id', 'commenter_id', 'comment_published', 'comment_modified', 'change_button', 'delete_button')


class PenLoveList(admin.ModelAdmin):
    list_display = ('id', 'pen_id', 'pen_user')


class PenViewList(admin.ModelAdmin):
    list_display = ('id', 'pen_id', 'ipaddress')


admin.site.register(Pen, PenList)
admin.site.register(PenData, PenDataList)
admin.site.register(Assets, PenAssetsList)
admin.site.register(PenSetting, PenSettingList)
admin.site.register(Comment, PenCommentsList)
# admin.site.register(PenLove, PenLoveList)
# admin.site.register(PenView, PenViewList)
