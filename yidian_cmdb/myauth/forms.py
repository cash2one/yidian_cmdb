# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-27
from django import forms
from models import MyUser
from django.contrib.auth.models import Group
from django.contrib.auth.forms import (
    AuthenticationForm, ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm, PasswordChangeForm,
    AdminPasswordChangeForm
)
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _


class MyAuthenticationForm(AuthenticationForm):
    """
    登录表单
    """
    username = forms.CharField(label=_("Username"), max_length=254, widget=forms.TextInput(
        attrs={"id": "login_username", "class": "form-control", "placeholder": "用户名"}
    )
                               )
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={"id": "login_password", "class": "form-control", "placeholder": "Password"}
    )
                               )


class MyUserCreationForm(UserCreationForm):
    """
    创建用户表单
    """
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = MyUser
        fields = ("username",)
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
        }


class MyUserUpdateForm(UserChangeForm):
    """
    更新用户表单
    """
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"./password-reset/\">this form</a>."
        ),
    )

    class Meta:
        model = MyUser
        exclude = ('date_joined', 'last_login')
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "job_number": forms.TextInput(attrs={'class': 'form-control'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "dingding": forms.TextInput(attrs={'class': 'form-control'}),
            "groups": forms.SelectMultiple(attrs={'class': 'form-control'}),
            "user_permissions": forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class UserPwdUpdateForm(PasswordChangeForm):
    """
    用户修改密码表单
    """
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                   )
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                    )
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                    )


class MyAdminPasswordChangeForm(AdminPasswordChangeForm):
    """
    管理员重置用户密码
    """
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )


class GroupForm(forms.ModelForm):
    """
    用户组表单
    """
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
