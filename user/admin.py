from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User, UserLogs


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'user_trail', 'user_status',
                  'user_activation_key', 'user_verification_code', 'is_superuser', 'is_staff', 'is_active']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_type', 'user_trail', 'user_status',
                  'user_activation_key', 'user_verification_code', 'is_superuser', 'is_staff', 'is_active']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'user_trail', 'user_status',
                    'user_activation_key', 'user_verification_code', 'is_superuser', 'is_staff', 'is_active']
    fieldsets = [
        ("User Auth Info", {
            "classes": ["wide", "extrapretty"],
            "fields": ['username', "email", "password", 'user_activation_key', 'user_verification_code']
        }),
        ("Personal info", {
            "classes": ["wide", "extrapretty"],
            "fields": ['first_name', 'last_name']}
         ),
        ("Permission info", {
            "classes": ["collapse", "extrapretty"],
            "fields": ['is_superuser', 'is_staff', 'is_active']
        }),
        ("Other info", {
            "classes": ["collapse", "extrapretty"],
            "fields": ['user_type', 'user_trail', 'user_status']
        })
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        ("User Auth Info", {
            "classes": ["wide", "extrapretty"],
            "fields": ['username', "email", "password", 'user_activation_key', 'user_verification_code']
        }),
        ("Personal info", {
            "classes": ["wide", "extrapretty"],
            "fields": ['first_name', 'last_name']}
         ),
        ("Permission info", {
            "classes": ["collapse", "extrapretty"],
            "fields": ['is_superuser', 'is_staff', 'is_active']
        }),
        ("Other info", {
            "classes": ["collapse", "extrapretty"],
            "fields": ['user_type', 'user_trail', 'user_status']
        })
    ]

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
