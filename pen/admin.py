from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import Group
from django import forms
from django.db import models
from django.forms import CheckboxSelectMultiple, Select, CheckboxInput
from django.forms.widgets import ChoiceWidget, RadioSelect

from .models import Pen, PenData, PenSetting, Assets, Comment


# class CustomLabel(forms.ModelMultipleChoiceField):
#     def label_from_instance(self, user):
#         return f'{user.username}'


# class PenCreationForm(forms.ModelForm):
#     class Meta:
#         model = Pen
#         fields = "__all__"
#         labels = {
#             'user': 'Author'
#         }


class PenChangeForm(forms.ModelForm):
    class Meta:
        model = Pen
        fields = "__all__"


@admin.register(Pen)
class PenAdmin(admin.ModelAdmin):
    # form = PenCreationForm
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
        models.ForeignKey: {'widget': RadioSelect}
    }

    list_display = ['pen_user', 'pen_title', 'pen_description', 'pen_slug', 'get_pen_tag', 'pen_thumbnail',
                    'pen_status',
                    'pen_platform', 'pen_comments', 'pen_published', 'pen_modified']
    fieldsets = [
        ("Pen Info", {
            "classes": ["wide", "extrapretty"],
            "fields": ['pen_title', 'pen_description', 'pen_slug', 'pen_tag', 'pen_thumbnail', 'pen_status',
                       'pen_platform']
        }),
        ("User Info", {
            "classes": ["wide", "extrapretty"],
            "fields": ['user', 'pen_love', 'pen_view']
        })
    ]
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        ("Pen Info", {
            "classes": ["wide", "extrapretty"],
            "fields": ['user', 'pen_title', 'pen_description', 'pen_slug', 'pen_tag', 'pen_thumbnail', 'pen_status',
                       'pen_platform', 'pen_love', 'pen_view']
        })
    ]

    search_fields = ["pen_title"]
    filter_horizontal = []

    def pen_user(self, obj):
        return f'{obj.user.username}'

    def get_pen_tag(self, obj):
        return ", ".join(o.name for o in obj.pen_tag.all())

    def get_form(self, request, obj=None, **kwargs):
        form = super(PenAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].label_from_instance = lambda inst: f'{inst.username}'
        form.base_fields['pen_love'].label_from_instance = lambda inst: f'{inst.username}'
        form.base_fields['pen_view'].label_from_instance = lambda inst: f'{inst.username}'
        return form
# admin.site.unregister(Group)

#
# # Register your models here.
# class PenList(admin.ModelAdmin, ChangeList):
#     list_display = ('id', 'username', 'pen_title', 'pen_status', 'pen_modified', 'pen_published')
#
#
class PenDataList(admin.ModelAdmin):
    list_display = ('username', 'pen_title')


class PenAssetsList(admin.ModelAdmin):
    list_display = ('username', 'pen_title')


class PenSettingList(admin.ModelAdmin):
    list_display = ('user', 'theme')


class PenCommentsList(admin.ModelAdmin):
    list_display = ('id', 'pen_id', 'user_id', 'commenter_id', 'comment_published', 'comment_modified', 'change_button',
                    'delete_button')


class PenLoveList(admin.ModelAdmin):
    list_display = ('id', 'pen_id', 'pen_user')


class PenViewList(admin.ModelAdmin):
    list_display = ('id', 'pen_id', 'ipaddress')


# admin.site.register(Pen, PenList)
admin.site.register(PenData, PenDataList)
admin.site.register(Assets, PenAssetsList)
admin.site.register(PenSetting, PenSettingList)
admin.site.register(Comment, PenCommentsList)
# admin.site.register(PenLove, PenLoveList)
# admin.site.register(PenView, PenViewList)
